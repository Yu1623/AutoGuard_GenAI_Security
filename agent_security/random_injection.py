import random

print("Prompt Injections")
f = open('prompt_injections.txt', 'r')

prompts = f.read().split('\n~~~~~~~~~~~~~~~~~~~\n')[100:]
print(prompts[0])
print(len(prompts))
random_list = random.sample(range(0, len(prompts)), 5)
for i in range(len(random_list)):
    random_number = random_list[i]
    random_prompt = prompts[random_number]
    print(f'{i+1}. {random_prompt}')

print("Story Prompts")

f = open('story_prompt.txt', 'r')

prompts = f.read().split('\n~~~~~~~~~~~~~~~~~~~\n')[100:]
print(prompts[0])
print(len(prompts))
random_list = random.sample(range(0, len(prompts)), 5)

for i in range(len(random_list)):
    random_number = random_list[i]
    random_prompt = prompts[random_number]
    print(f'{i+1}. {random_prompt}')


