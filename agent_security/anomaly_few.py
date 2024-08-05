from langgraph.graph import Graph
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Step 3: Define the security_guard_node function
def security_guard_node(user_input: str) -> str:
    # Initialize LLM with safety settings turned off
    llm = GoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }
    )
    
    # Define detection prompt template
    detection_prompt_template = """
    Genuine Input Definition: 
    Genuine user inputs should be creative, original, and adhere to the prompt's request for a short story. Inputs that deviate from this intent, such as irrelevant content, inappropriate topics, or non-story elements, are considered inappropriate.
    
    Here are examples of genuine inputs:
    1. [ WP ] Science has found the key to immortality , but there 's a catch : it can only be administered at birth . You are a member of the last mortal generation .
    2. [ WP ] You 're a State Farm agent and are often summoned by your clients to reassure them in their time of need , usually through the jingle . One day , you are summoned by two people at the same time .
    3. [ WP ] You 're the world 's best photographer . Your secret ? You can freeze time . You last photo brings some suspicion up .
    3. ( EU ) You have the most well respected and feared job in all of the world . You go into the wild , and put down rabid Pokemon who 've killed humans .
    4. [ WP ] Main character finds a door they 've never seen before , in a house they 've lived in their whole life .
    5. [ WP ] Depending on social caste , State citizens are limited to speak or write only a specific amount of words during their lifetime .
    
    User input: {user_input}
    
    Does the user input match the intent of the original prompt? Answer the following questions to determine:
    - What does the original prompt mean?
    - What does the original prompt want from the user?
    - Does the user input fit the original prompt's intent?
    - Is the user input appropriate and relevant to the given prompt?
    Answer whether the input is Genuine or Inappropriate and provide a detailed explanation.
    """
    
    # Create a detection prompt
    detection_prompt = ChatPromptTemplate.from_template(detection_prompt_template)
    
    # Define the LLM chain for detection
    chain = (
        {'user_input': RunnablePassthrough()}
        | detection_prompt
        | llm
        | StrOutputParser()
    )
    
    # Obtain the result of the detection
    detection_result = chain.invoke(user_input)
    print(detection_result)
    # Check if the result indicates inappropriate input
    if "Inappropriate" in detection_result:
        return "Inappropriate Input"
    else:
        return user_input

# Step 6: Define the executor_agent_node function
def executor_agent_node(topic: str) -> str:
    # If input is "Inappropriate Input", return message

    if topic == "Inappropriate Input":
        return "Inappropriate Input Detected"
    
    # Original LLM application setup
    llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")
    prompt = ChatPromptTemplate.from_template("Write me a short story using the given prompt: {story_prompt}")
    output_parser = StrOutputParser()
    
    chain = (
        {"story_prompt": RunnablePassthrough()}
        | prompt
        | llm
        | output_parser
    )
    
    # Generate result using original LLM application
    result = chain.invoke(topic)
    
    return result

# Step 7: Create the LangGraph
lang_graph = Graph()

# Add nodes
lang_graph.add_node("security_guard_node", security_guard_node)
lang_graph.add_node("executor_agent_node", executor_agent_node)

# Add edge
lang_graph.add_edge("security_guard_node", "executor_agent_node")

# Set entry and finish points
lang_graph.set_entry_point("security_guard_node")
lang_graph.set_finish_point("executor_agent_node")

# Compile the LangGraph
app = lang_graph.compile()

# Step 8: Execute the Application
while True:
    try:
        user_input = input("llm>> ")
        if user_input == "":
            break
        
        # Execute the LangGraph
        result = app.invoke(user_input)
        print(result)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        break
