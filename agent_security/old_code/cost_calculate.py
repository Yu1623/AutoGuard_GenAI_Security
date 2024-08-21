import pandas as pd

def load_csv(filename):
    df = pd.read_csv(f"/home/yuxuan/Documents/summer_internship/gensec-liu-yuxuan/agent_security//prompt_injections_{filename}.csv")
    sum = 0
    for i in range(len(df['Token Usage'])):
        sum += df["Token Usage"][i]
    average_cost = sum / len(df['Token Usage'])
    return average_cost
filename = input("Which document? ")
average_cost = load_csv(filename)
print(average_cost)