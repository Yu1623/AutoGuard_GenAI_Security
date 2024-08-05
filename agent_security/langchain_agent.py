from langchain_google_genai import GoogleGenerativeAI
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
import readline
from langchain.agents.load_tools import load_tools

llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest",temperature=0)
tools = load_tools(["pubmed"], llm = llm)
instructions = """You are an agent designed to search and summarize information to
answer the user's questions. You have access to a Pubmed tool, which you can use to
search for information.  You might know the answer without
running any code, but you should still run the code to get the answer.  If it does
not seem like you can write code to answer the question, just return "I don't know"
as the answer.
"""
base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions=instructions)

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print(f"Welcome to my application.  I am configured with these tools")
for tool in tools:
  print(f'  Tool: {tool.name} = {tool.description}')

while True:
  line = input("llm>> ")
  if line == "":
    break
  else:
    try:
      result = agent_executor.invoke({"input": line})
      print(result)
    except Exception as e:
      print(e)
      break
