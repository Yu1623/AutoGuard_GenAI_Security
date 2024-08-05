from datasets import load_dataset
"""
ds = load_dataset("deepset/prompt-injections")

data = []

for data_name in ds:
    dataset = ds[data_name]
    for i in range(len(dataset["label"])):
        label = dataset["label"][i]
        if label == 1:
            text = dataset["text"][i]
            data += [text]

f = open("prompt_injections.txt", "w")
for text in data:
    f.write(f"{text}\n~~~~~~~~~~~~~~~~~~~\n")
f.close()
"""
ds = load_dataset("synapsecai/synthetic-prompt-injections")
data = []

for data_name in ds:
    dataset = ds[data_name]
    data = []
    i = 0
    while len(data) < 400:
        label = dataset['label'][i]
        text = dataset['text'][i]
        if label == '1':
            data += [text]
            print(f"Prompt added {len(data)}: {text}")
        i += 1
f = open('prompt_injections.txt', 'w')
for text in data:
    f.write(f"{text}\n~~~~~~~~~~~~~~~~~~~\n")
f.close()
"""
ds = load_dataset("karmat314/writingprompts-story")

dataset = ds["train"]

data = []
for story_prompt in dataset["prompt"]:
    if len(story_prompt) < 300:
        data += [story_prompt]

f = open("story_prompt.txt", "w")
for story_prompt in data:
    f.write(f"{story_prompt}\n~~~~~~~~~~~~~~~~~~~\n")
f.close()
"""
