from datasets import load_dataset

def load_data():
    # Download test datasets from Hugginface

    # Parameters:
    #       None

    # Returns:
    #       None

    ''' Ask the user for the dataset that they want to download as well as its type (either prompt injection or genuine input) and the maximum length of the inputs that the security guard will process '''
    dataset_name = input("Dataset from Huggingface: ")
    dataset_type = input("Prompt Injection or Genuine Input: ")
    dataset_type = dataset_type.replace(' ', '_')
    max_length = input("Please set the maximum length of the input: ")

    ''' Filter and retrieve the inputs based on the user's answers above '''
    ds = load_dataset(dataset_name)
    data = []
    for data_type in ds:
        dataset = ds[data_type]
        columns = dataset.column_names
        for column in columns:
            print(f"Example of Category {column}: {dataset[column][0]}")
        ''' The Hugginface dataset likely has numerous columns of data, each for a different category '''
        category = input("Which category to use? ")

        ''' Prompt Injection datasets normally have a "label" category that indicates if the input is a prompt injection or not '''
        if "label" in columns:
            for i in range(len(dataset["label"])):
                label = dataset["label"][i]
                text = dataset[category][i]
                ''' Inputs with label 1 are prompt injections '''
                if label == 1:
                    if len(text) < int(max_length):
                        data += [text]
        else:
            for i in range(len(dataset)):
                text = dataset[category][i]
                if len(text) < int(max_length):
                    data += [text]

    ''' Load the retrieved inputs into txt files '''
    f = open(f'/home/yuxuan/Documents/summer_internship/gensec-liu-yuxuan/agent_security/data/input_data/{dataset_type}.txt', 'w')
    for text in data:
        f.write(f'{text}\n~~~~~~~~~~~~~~~~~~~\n')
    f.close()
    return

load_data()