import random

def random_prompts():
    # Randomly select inputs from the train datasets

    # Parameters:
    #       None

    # Returns:
    #       None
    
    filename = input("Which file do you want to get the prompts from? ")

    ''' Ensure that the inputs does not come from the test datasets '''
    start_point = input("How much data from this file did you use for training? ")
    f = open(f'/home/yuxuan/Documents/summer_internship/gensec-liu-yuxuan/agent_security/data/input_data/{filename}.txt', 'r')
    prompts = f.read().split('\n~~~~~~~~~~~~~~~~~~~\n')[int(start_point):]
    random_list = random.sample(range(0, len(prompts)), 5)
    for random_number in random_list:
        random_prompt = prompts[random_number]
        print(random_prompt)
    
    return

random_prompts()