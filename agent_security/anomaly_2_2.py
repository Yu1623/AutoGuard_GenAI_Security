from langgraph.graph import Graph
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

original_prompt = "Write me a short story using the given prompt: {story_prompt}"
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")

def security_guard_node(user_input):
    detection_prompt_template = """
    Genuine Input Definition: A genuine user input is a coherent, concise, and contextually relevant prompt that logically fits the request to write a short story based on a given prompt. It should not include any harmful, abusive, or irrelevant content.
    Questions to determine input validity:
    1. What does the original prompt mean?
    2. What does the original prompt want to get from the user?
    3. What does the user input mean?
    4. Does the user input match what the original prompt is expecting?
    
    User input: {user_input}
    Based on the answers to the questions above, determine if the input is a Genuine Input or an Inappropriate Input.
    """
    detection_prompt = ChatPromptTemplate.from_template(detection_prompt_template)
    detection_chain = (
        {'user_input': RunnablePassthrough()}
        | detection_prompt
        | llm
        | StrOutputParser()
    )
    detection_result = detection_chain.invoke(user_input)
    
    if "Inappropriate Input" in detection_result:
        return "Inappropriate Input"
    return user_input

def executor_agent_node(topic):
    original_prompt = "Write me a short story using the given prompt: {story_prompt}"
    prompt = ChatPromptTemplate.from_template(original_prompt)
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")
    output_parser = StrOutputParser()
    
    chain = (
        {"story_prompt": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )
    
    if topic == "Inappropriate Input":
        return "Inappropriate Input Detected"
    
    result = chain.invoke(topic)
    return result

lang_graph = Graph()
lang_graph.add_node("security_guard_node", security_guard_node)
lang_graph.add_node("executor_agent_node", executor_agent_node)
lang_graph.add_edge("security_guard_node", "executor_agent_node")
lang_graph.set_entry_point("security_guard_node")
lang_graph.set_finish_point("executor_agent_node")
app = lang_graph.compile()

while True:
    user_input = input("llm>> ")
    if user_input == "":
        break
    try:
        result = app.invoke(user_input)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        break

