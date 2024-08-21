"""
Load datasets from Hugginface
"""
#Here is the Huggingface dataset used to obtain the final results: karmat314/writingprompts-story
#Here is a well-crafted dataset of generic prompt injections, please note that this is not used for the final results: synapsecai/synthetic-prompt-injections

from datasets import load_dataset

def load_data():
    dataset_name = input("Dataset from Huggingface: ")
    dataset_type = input("Prompt Injection or Genuine Input: ")
    dataset_type = dataset_type.replace(' ', '_')
    max_length = input("Please set the maximum length of the input: ")

    ds = load_dataset(dataset_name)
    data = []
    for data_type in ds:
        dataset = ds[data_type]
        columns = dataset.column_names
        for column in columns:
            print(f"Example of Category {column}: {dataset[column][0]}")
        category = input("Which category to use? ")
        if "label" in columns:
            for i in range(len(dataset["label"])):
                label = dataset["label"][i]
                text = dataset[category][i]
                if label == 1:
                    if len(text) < int(max_length):
                        data += [text]
        else:
            for i in range(len(dataset)):
                text = dataset[category][i]
                if len(text) < int(max_length):
                    data += [text]
                
    f = open(f'{dataset_type}.txt', 'w')
    for text in data:
        f.write(f'{text}\n~~~~~~~~~~~~~~~~~~~\n')
    f.close()
    return

load_data()