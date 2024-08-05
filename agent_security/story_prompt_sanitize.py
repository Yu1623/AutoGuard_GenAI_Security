from security_2_1 import *

f = open("story_prompt.txt", 'r')

prompts = f.read().split("\n~~~~~~~~~~~~~~~~~~~\n")

for i in range(len(prompts)):
    print(f"Checking {i}")
    prompt = prompts[i]
    detection_prompt, result = security_guard_node(prompt)
    if "Inappropriate Input" in result:
        print(f"Prompt: {prompt}\nResult: {result}")

