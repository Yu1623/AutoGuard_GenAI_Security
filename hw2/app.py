import requests
from bs4 import BeautifulSoup
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.agents.load_tools import load_tools
from langchain.tools import tool
from langchain_google_genai import GoogleGenerativeAI, HarmCategory, HarmBlockThreshold
import os
from langsmith import Client

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"LangSmith Introduction"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
client = Client()

llm = GoogleGenerativeAI(
        model = "gemini-pro",
        temperature = 0,
        safety_settings = {HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE}
)

@tool
def CDC_autism_list(query):
    """Useful when you are looking for list of information from CDC on autism. Returns a list of urls of information sites of autism"""
    url = requests.get("https://www.cdc.gov/autism/site.html")
    soup = BeautifulSoup(url.text, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        if 'autism' in link.get('href'):
            if link.get('href') in urls:
                continue
            else:
                urls += [link.get('href')]
    urls.remove('/autism/index.html')
    return urls

@tool
def load_content(url):
    """Useful when you want to get the information from a CDC url. Takes an url as an argument."""
    if "https://www.cdc.gov" in url:
        page = requests.get(url)
    else:
        page = requests.get(f"https://www.cdc.gov{url}")
    soup = BeautifulSoup(page.text, 'html.parser')
    doc_content = []
    for content in soup.find_all('p'):
        doc_content += [content]
    return doc_content


tools = load_tools(["serpapi", "terminal", "llm-math", "pubmed"], llm=llm, allow_dangerous_tools = True)
tools.extend([CDC_autism_list, load_content])
base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions = "Answer the user's requests using at most 8 tool calls")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose = True)

print("Welcome to the medical and science application. I am configured with the following tools:")
for tool in tools:
    print(f"Tool: {tool.name} = {tool.description}\n")

while True:
    try:
        user_input = input("llm>>")
        if user_input:
            print(agent_executor.invoke({"input": user_input}))
        else:
            break
    except Exception as e:
        print(e)
