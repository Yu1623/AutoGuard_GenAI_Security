import random

def random_prompts():
    filename = input("Which file do you want to get the prompts from? ")
    start_point = input("How much data from this file did you use for training? ")
    f = open(f'{filename}.txt', 'r')
    prompts = f.read().split('\n~~~~~~~~~~~~~~~~~~~\n')[int(start_point):]
    random_list = random.sample(range(0, len(prompts)), 5)
    for random_number in random_list:
        random_prompt = prompts[random_number]
        print(random_prompt)
    return

random_prompts()