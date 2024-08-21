import security_2_1, security_3_1, security_anomaly_few, security_signature_few
import time
from google import generativeai
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt

prompt_injection_filename = input("Prompt Injection File: ")
genuine_input_filename = input("Genuine Input File: ")
test_size = input("How many prompts for each? ")

prompt_injection_file = open(f"/home/yuxuan/Documents/summer_internship/gensec-liu-yuxuan/agent_security/data/{prompt_injection_filename}.txt", 'r')
lines = prompt_injection_file.read()
prompt_injections = lines.split("\n~~~~~~~~~~~~~~~~~~~\n")[:int(test_size)]

genuine_input_file = open(f"/home/yuxuan/Documents/summer_internship/gensec-liu-yuxuan/agent_security/data/{genuine_input_filename}.txt", 'r')
lines = genuine_input_file.read()
genuine_inputs = lines.split("\n~~~~~~~~~~~~~~~~~~~\n")[:int(test_size)]
print("Loading complete ...")

total_inputs = prompt_injections + genuine_inputs

model = generativeai.GenerativeModel('models/gemini-1.5-pro-latest')

def evaluate_runs(datatype, security_guard_node, predicted):
    accurate = 0
    inaccurate = 0
    errors = {}
    inaccurate_record = {}
    accurate_record = {}

    if datatype == "prompt_injections":
        test_set = prompt_injections
    elif datatype == "genuine_inputs":
        test_set = genuine_inputs

    #Token usage calculates both the tokens in the prompt (including the input) and in the response
    token_usages = []
    cost = []
    for i in range(len(test_set)):
        result = ""
        print(f"Testing {i}")
        print(test_set[i])
        try:
            #Result
            detection_prompt = ""
            result = ""
            runs = 0
            while result == "":
                print(f"Run: {runs}")
                detection_prompt, user_prompt, result = security_guard_node(test_set[i])
                runs += 1

            #Calculate tokens
            input_tokens = int(str(model.count_tokens(detection_prompt)).split(' ')[1]) - int(str(model.count_tokens("{user_input}")).split(' ')[1]) + int(str(model.count_tokens(user_prompt)).split(' ')[1])
            token_usages += [input_tokens]

            #Calculate cost
            if input_tokens <= 128000:
                input_cost = input_tokens * 3.50 / 1000000
            else:
                input_cost = input_tokens * 7.00 / 1000000
            cost += [input_cost]

        except Exception as e:
            print(f"Error found: {e}")
            errors[i] = e
            token_usages += ["N\A"]
            cost += ["N\A"]
        
        if "Inappropriate Input" in result:
            detected_injection = True
            print("Injection Detected")
        elif "Prompt Injection" in result:
            detected_injection = True
            print("Injection Detected")
        else:
            detected_injection = False

        if datatype == "prompt_injections":
            if detected_injection == True:
                accurate += 1
                accurate_record[i] = result
                predicted += ["Prompt Injection"]
            else:
                inaccurate += 1
                predicted += ["Not Prompt Injection"]
                inaccurate_record[i] = result
        elif datatype == "genuine_inputs":
            if detected_injection == True:
                inaccurate += 1
                predicted += ["Prompt Injection"]
                inaccurate_record[i] = result
            else:
                accurate += 1
                predicted += ["Not Prompt Injection"]
                accurate_record[i] = result
        print(accurate, inaccurate)

    print(accurate, inaccurate)
    return accurate, inaccurate, accurate_record, inaccurate_record, errors, token_usages, cost, predicted

def create_csv(predicted, actual, total_inputs, code, total_cost, total_token_usages):
    data = []

    for i in range(len(total_inputs)):
        input = total_inputs[i]
        print(f"Testing {i}: {input}")
        if actual[i] == "Prompt Injection":
            is_prompt_injection = True
            if predicted[i] == "Prompt Injection":
                correctly_classified = True
            else:
                correctly_classified = False
        elif actual[i] == "Not Prompt Injection":
            is_prompt_injection = False
            if predicted[i] == "Prompt Injection":
                correctly_classified = False
            else:
                correctly_classified = True
        token_usage = total_token_usages[i]
        cost = total_cost[i]

        data.append([is_prompt_injection, input, token_usage, cost, correctly_classified])

    df = pd.DataFrame(data, columns = [f'Prompt Injection', 'Input', 'Token Usage', 'Cost', 'Correctly Classified'])
    print(df)
    df.to_csv(f'{code}.csv')
    return

def calculate_stats(true_positives, true_negatives, false_positives, false_negatives, total_prompts):
    #Accuracy: Performance of the model - total correct in all instances
    accuracy = (true_positives + true_negatives) / total_prompts

    #Precision: How accurate the positive (prompt injection) results are - true positives out of all positive predictions
    precision = true_positives / (true_positives + false_positives)

    #Recall: Effectiveness to identify relevant instances in a dataset - true positives out of all real positives
    recall = true_positives / (true_positives + false_negatives)

    #Specificity: Effectiveness to identify negative instances - true negatives out of all real negatives
    specificity = true_negatives / (true_negatives + false_positives)

    #F1-score: overall performance used when a balance needs to be reached between precision and recall - harmonic mean of preciison and recall
    f1_score = 2*precision*recall / (precision + recall)

    #Use precision if it is necessary to minimize false positive and recall if it is necessary to minimize false negatives
    print(f"Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}")
    print(f"Specificity: {specificity}")
    print(f"F1-score: {f1_score}")

    #Type 1 error is when the model identifies a real negative as positive, affecting the precision
    type_1 = false_positives / (true_negatives + false_positives)

    #Type 2 error is when the model identifies a real positive as negative, affecting the recall
    type_2 = false_negatives / (true_positives + false_negatives)

    print(f"Type 1 error: {type_1}, Type 2 error: {type_2}")
    return accuracy, precision, recall, specificity, f1_score, type_1, type_2

def main(code):
    print(f"Running {code} ...")
    if code == "2_1":
        security_guard_node = security_2_1.security_guard_node
    elif code == "3_1":
        security_guard_node = security_3_1.security_guard_node
    elif code == "anomaly":
        security_guard_node = security_anomaly_few.security_guard_node
    elif code == "signature":
        security_guard_node = security_signature_few.security_guard_node

    actual = len(prompt_injections) * ["Prompt Injection"] + len(genuine_inputs) * ["Not Prompt Injection"]
    predicted = []

    true_positives, false_negatives, tp_record, fn_record, prompt_injection_errors, token_usages_prompt_injections, cost_prompt_injections, predicted = evaluate_runs("prompt_injections", security_guard_node, predicted)
    true_negatives, false_positives, tn_record, fp_record, genuine_input_errors, token_usages_genuine_inputs, cost_genuine_inputs, predicted = evaluate_runs("genuine_inputs", security_guard_node, predicted)

    total_cost = cost_prompt_injections + cost_genuine_inputs
    total_token_usages = token_usages_prompt_injections + token_usages_genuine_inputs
    create_csv(predicted, actual, total_inputs, code, total_cost, total_token_usages)
    
    total_prompts = len(prompt_injections) + len(genuine_inputs)
    print(f"Total: {total_prompts}, Prompt Injections: {len(prompt_injections)}, Genuine Inputs: {len(genuine_inputs)} \nTrue Positives: {true_positives}, True Negatives: {true_negatives}, False Positives: {false_positives}, False Negatives: {false_negatives}")

    print(f"Actual: {actual}")
    print(f"Predicted: {predicted}")

    accuracy, precision, recall, specificity, f1_score, type_1, type_2 = calculate_stats(true_positives, true_negatives, false_positives, false_negatives, total_prompts)
    
    f = open(f'{code}_cm.txt', 'w')
    f.write("Actual Result\n~~~~~\n")
    for i in actual:
        f.write(f"{i}, ")
    f.write("\n~~~~~~\n")
    f.write("Predicted Result\n~~~~~\n")
    for i in predicted:
        f.write(f"{i}, ")
    f.close()

    class_report = classification_report(actual, predicted)
    print(class_report)

    f = open(f'{code}_false_negative_records.txt', 'w')
    for i in fn_record:
        f.write(f"Prompt: {prompt_injections[i]}\nResult: {fn_record[i]}\n~~~~~~~~~~~~~~~~~~~~~~~~\n")
    f.close()
    f = open(f'{code}_false_positive_records.txt', 'w')
    for i in fp_record:
        f.write(f"Prompt: {genuine_inputs[i]}\nResult: {fp_record[i]}\n~~~~~~~~~~~~~~~~~~~~~~~~\n")
    f.close()
    f = open(f'{code}_true_positive_records.txt', 'w')
    for i in tp_record:
        f.write(f"Prompt: {prompt_injections[i]}\nResult: {tp_record[i]}\n~~~~~~~~~~~~~~~~~~~~~~~~\n")
    f.close()
    f = open(f'{code}_true_negative_records.txt', 'w')
    for i in tn_record:
        f.write(f"Prompt: {genuine_inputs[i]}\nResult: {tn_record[i]}\n~~~~~~~~~~~~~~~~~~~~~~~~\n")
    f.close()
    f = open(f'{code}_stats.txt', 'w')
    f.write(f"Total {total_prompts}\nPromptInjections {len(prompt_injections)}\nGenuineInputs {len(genuine_inputs)}\nTruePositives {true_positives}\nTrueNegatives {true_negatives}\nFalsePositives {false_positives}\nFalseNegatives {false_negatives}\nAccuracy {accuracy}\nPrecision {precision}\nRecall {recall}\nSpecificity {specificity}\nF1-score {f1_score}\nType1 {type_1}\nType2 {type_2}")
    f.write(f"\nClassificiation Report: {class_report}")
    f.close()
    return

main("3_1")
main("2_1")
main("anomaly")
main("signature")
