import security_2_1
import security_2_2
import security_2_5
import security_2_10
import security_2_20
import security_3_1
import security_4_2
import security_4_5
import security_4_10
import security_4_20

import security_anomaly_few, security_signature_few

import time
from google import generativeai
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt

prompt_injection_file = open("prompt_injections.txt", 'r')
lines = prompt_injection_file.read()
prompt_injections = lines.split("\n~~~~~~~~~~~~~~~~~~~\n")

story_prompt_file = open("story_prompt.txt", 'r')
lines = story_prompt_file.read()
story_prompts = lines.split("\n~~~~~~~~~~~~~~~~~~~\n")[:20]

print("Loading complete ...")
model = generativeai.GenerativeModel('models/gemini-1.5-pro-latest')

def test_effectiveness(code):
    print(f"Running {code} ...")
    if code == "2_1":
        security_guard_node = security_2_1.security_guard_node
    elif code == "2_2":
        security_guard_node = security_2_2.security_guard_node
    elif code == "2_5":
        security_guard_node = security_2_5.security_guard_node
    elif code == "2_10":
        security_guard_node = security_2_10.security_guard_node
    elif code == "2_20":
        security_guard_node = security_2_20.security_guard_node
    elif code == "3_1":
        security_guard_node = security_3_1.security_guard_node
    elif code == "4_2":
        security_guard_node = security_4_2.security_guard_node
    elif code == "4_5":
        security_guard_node = security_4_5.security_guard_node
    elif code == "4_10":
        security_guard_node = security_4_10.security_guard_node
    elif code == "4_20":
        security_guard_node = security_4_20.security_guard_node
    elif code == "anomaly":
        security_guard_node = security_anomaly_few.security_guard_node
    elif code == "signature":
        security_guard_node = security_signature_few.security_guard_node

    actual = len(prompt_injections) * ["Prompt Injection"] + len(story_prompts) * ["Not Prompt Injection"]
    predicted = []

    true_positives = 0
    prompt_injection_errors = {}
    fn_record = {}
    tp_record = {}
    time_elapses_prompt_injections = {}
    #Token usage calculates both the tokens in the prompt (including the input) and in the response
    token_usages_prompt_injections = {}
    cost_prompt_injections = {}
    for i in range(len(prompt_injections)):
        result = ""
        print(f"Testing injection {i}")
        print(prompt_injections[i])
        try:
            #Result
            detection_prompt = ""
            result = ""
            runs = 0
            while result == "":
                print(f"Run: {runs}")
                detection_prompt, user_prompt, result = security_guard_node(prompt_injections[i])
                runs += 1

            #Calculate tokens
            input_tokens = int(str(model.count_tokens(detection_prompt)).split(' ')[1]) - int(str(model.count_tokens("{user_input}")).split(' ')[1]) + int(str(model.count_tokens(user_prompt)).split(' ')[1])
            token_usages_prompt_injections[i] = input_tokens

            #Calculate cost
            if input_tokens <= 128000:
                input_cost = input_tokens * 3.50 / 1000000
            else:
                input_cost = input_tokens * 7.00 / 1000000
            cost_prompt_injections[i] = input_cost
        except Exception as e:
            print(f"Error found: {e}")
            prompt_injection_errors[i] = e
            token_usages_prompt_injections[i] = "N\A"
            cost_prompt_injections[i] = "N\A"
        if "Inappropriate Input" in result:
            true_positives += 1
            print("Inappropriate Input detected")
            predicted += ["Prompt Injection"]
            tp_record[i] = result
        else:
            fn_record[i] = result
            predicted += ["Not Prompt Injection"]
    false_negatives = len(prompt_injections) - true_positives
    print(time_elapses_prompt_injections)
    data = []
    for i in range(len(prompt_injections)):
        prompt_injection = prompt_injections[i]
        print(f"Loading {i}")
        if predicted[i] == "Prompt Injection":
            injection_detected = "True"
        else:
            injection_detected = "False"
        token_usage = token_usages_prompt_injections[i]
        cost = cost_prompt_injections[i]

        data.append([prompt_injection, token_usage, cost, injection_detected])

    df_prompt_injections = pd.DataFrame(data, columns = ['Prompt Injection', 'Token Usage', 'Cost', 'Injection Detected'])
    print(df_prompt_injections)
    df_prompt_injections.to_csv(f'prompt_injections_{code}.csv')


    false_positives = 0
    fp_record = {}
    tn_record = {}
    story_prompt_errors = {}
    time_elapses_story_prompts = {}
    #Token usage calculates both the tokens in the prompt (including the input) and in the response
    token_usages_story_prompts = {}
    cost_story_prompts = {}

    for i in range(len(story_prompts)):
        result = ""
        print(f"Testing prompt {i}")
        story_prompt = story_prompts[i]
        try:
            #Result
            detection_prompt = ""
            result = ""
            runs = 0
            while result == "":
                print(f"Run: {runs}")
                detection_prompt, user_prompt, result = security_guard_node(story_prompt)
                runs += 1

            #Calculate tokens
            input_tokens = int(str(model.count_tokens(detection_prompt)).split(' ')[1]) - int(str(model.count_tokens("{user_input}")).split(' ')[1]) + int(str(model.count_tokens(user_prompt)).split(' ')[1])
            print(input_tokens)
            token_usages_story_prompts[i] = input_tokens

            #Calculate cost
            if input_tokens <= 128000:
                input_cost = input_tokens * 3.50 / 1000000
            else:
                input_cost = input_tokens * 7.00 / 1000000
            cost_story_prompts[i] = input_cost
        except Exception as e:
            print(f"Error found: {e}")
            story_prompt_errors[i] = e
            token_usages_story_prompts[i] = "N\A"
            cost_story_prompts[i] = "N\A"
        if "Inappropriate Input" in result:
            print("Inappropriate Input Detected")
            false_positives += 1
            fp_record[i] = result
            predicted += ["Prompt Injection"]
        else:
            tn_record[i] = result
            predicted += ["Not Prompt Injection"]
    true_negatives = len(story_prompts) - false_positives

    data = []
    for i in range(len(story_prompts)):
        story_prompt = story_prompts[i]
        print(f"Loading {i}")
        if predicted[len(prompt_injections) + i] == "Prompt Injection":
            injection_detected = "True"
        else:
            injection_detected = "False"
        token_usage = token_usages_story_prompts[i]
        cost = cost_story_prompts[i]

        data.append([story_prompt, token_usage, cost, injection_detected])

    df_story_prompts = pd.DataFrame(data, columns = ['Story Prompt', 'Token Usage', 'Cost', 'Injection Detected'])
    print(df_story_prompts)
    df_story_prompts.to_csv(f'story_prompts_{code}.csv')

    #Create CSV file for true positives, true negatives, false negatives and false positives
    #Include details for false negatives and false positives to determine why they are not identified accurately

    total_prompts = len(prompt_injections) + len(story_prompts)
    print(f"Total: {total_prompts}, Prompt Injections: {len(prompt_injections)}, Story Prompts: {len(story_prompts)} \nTrue Positives: {true_positives}, True Negatives: {true_negatives}, False Positives: {false_positives}, False Negatives: {false_negatives}")

    print(f"Actual: {actual}")
    print(f"Predicted: {predicted}")

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
        f.write(f"Prompt: {story_prompts[i]}\nResult: {fp_record[i]}\n~~~~~~~~~~~~~~~~~~~~~~~~\n")
    f.close()
    f = open(f'{code}_true_positive_records.txt', 'w')
    for i in tp_record:
        f.write(f"Prompt: {prompt_injections[i]}\nResult: {tp_record[i]}\n~~~~~~~~~~~~~~~~~~~~~~~~\n")
    f.close()
    f = open(f'{code}_true_negative_records.txt', 'w')
    for i in tn_record:
        f.write(f"Prompt: {story_prompts[i]}\nResult: {tn_record[i]}\n~~~~~~~~~~~~~~~~~~~~~~~~\n")
    f.close()
    f = open(f'{code}_stats.txt', 'w')
    f.write(f"Total {total_prompts}\nPromptInjections {len(prompt_injections)}\nStoryPrompts {len(story_prompts)}\nTruePositives {true_positives}\nTrueNegatives {true_negatives}\nFalsePositives {false_positives}\nFalseNegatives {false_negatives}\nAccuracy {accuracy}\nPrecision {precision}\nRecall {recall}\nSpecificity {specificity}\nF1-score {f1_score}\nType1 {type_1}\nType2 {type_2}")
    f.write(f"\nClassificiation Report: {class_report}")
    f.close()
    return

#test_effectiveness("3_1")
#test_effectiveness("2_1")
test_effectiveness("anomaly")
test_effectiveness("signature")
