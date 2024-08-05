from langgraph.graph import Graph
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Step 2: Extract the prompt
original_prompt = "Tell me a joke about {topic}"

# Step 3: Create the security_guard_node function
def security_guard_node(user_input):
    detection_prompt_template = """
    Genuine Input Definition: A genuine input for this prompt is a topic that is appropriate for a joke. It should be a single word or a short phrase that describes a subject suitable for humor and is not offensive, harmful, or sensitive.
    Questions to determine the genuineness of the input:
    1. Does the user input fit the format of a single word or short phrase?
    2. Is the user input a suitable topic for a joke?
    3. Is the user input free from offensive, harmful, or sensitive content?

    Based on the above definition and questions, determine if the user input is appropriate.

    User Input: {user_input}
    """
    detection_prompt_template += """
    If the input matches the definition, respond with "Genuine Input". Otherwise, respond with "Inappropriate Input".
    """

    # Step 5: Detect inappropriate inputs through LLM chain
    detection_prompt = ChatPromptTemplate.from_template(detection_prompt_template)
    detection_chain = (
        {"user_input": RunnablePassthrough()}
        | detection_prompt
        | GoogleGenerativeAI(model="gemini-1.5-pro-latest")
        | StrOutputParser()
    )

    detection_result = detection_chain.invoke(user_input)

    if "Inappropriate Input" in detection_result:
        return "Inappropriate Input"
    return user_input

# Step 6: Create the executor_agent_node function
def executor_agent_node(topic):
    prompt = ChatPromptTemplate.from_template(original_prompt)
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")
    output_parser = StrOutputParser()

    chain = (
        {"topic": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )

    if topic == "Inappropriate Input":
        return "Inappropriate Input Detected"

    result = chain.invoke(topic)
    return result

# Step 7: Create and configure the LangGraph
lang_graph = Graph()

# Add nodes
lang_graph.add_node("security_guard_node", security_guard_node)
lang_graph.add_node("executor_agent_node", executor_agent_node)

# Connect nodes
lang_graph.add_edge("security_guard_node", "executor_agent_node")

# Set entry and finish points
lang_graph.set_entry_point("security_guard_node")
lang_graph.set_finish_point("executor_agent_node")

# Compile LangGraph
app = lang_graph.compile()

# Step 8: Execute the application
while True:
    try:
        user_input = input("Enter a topic for a joke (or leave blank to exit): ")
        if not user_input:
            break
        result = app.invoke(user_input)
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        break

