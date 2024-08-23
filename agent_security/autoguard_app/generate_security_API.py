import anthropic
from langchain_core.prompts import PromptTemplate

client = anthropic.Anthropic()

llm = "claude-3-5-sonnet-20240620"
developer_instructions = "You are an experienced Python computer programmer who diligently obeys and follows the instructions of your user to the best of your ability. Skilled as you are in generating code, you always remembered to check your code for potential errors. You should only have the Python program in your response. You should not make any additional comments outside of the program."
max_tokens = 1500

def load_prompt_template(filename):
    f = open(f"/home/yuxuan/Documents/summer_internship/gensec-liu-yuxuan/agent_security/autoguard_app/{filename}.txt", 'r')
    prompt_template = f.read()
    return prompt_template

def load_user_llm_app(filename):
    f = open(f"/home/yuxuan/Documents/summer_internship/gensec-liu-yuxuan/agent_security/autoguard_app/{filename}.py", 'r')
    user_llm_app = f.read()
    return user_llm_app

def run_claude(prompt):
    message = client.messages.create(
        system = developer_instructions,
        temperature = 1,
        max_tokens = max_tokens,
        model = llm,
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )
    response = message.content[0].text
    return response

print("This is Autoguard, a LLM application that will automatically skill your LLM app from prompt injections.")

prompt_template = load_prompt_template("anomaly_few_automate")
user_llm_app = load_user_llm_app("short_story_app")
lines = prompt_template.split("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
prompt = lines[0] + user_llm_app + lines[1]
response = run_claude(prompt)
print(response)