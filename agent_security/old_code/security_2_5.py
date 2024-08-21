from langgraph.graph import Graph
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Step 2: Extract the prompt and initialize the LLM
original_prompt = "Write me a short story using the given prompt: {story_prompt}"
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")

# Step 3: Create the security_guard_node function
def security_guard_node(user_input):
    Genuine_Input_Definition = """
    A genuine input for this LLM application should be a creative and imaginative prompt for a short story. It should provide a scenario, characters, or plot ideas that the LLM can use to generate a coherent and engaging story.
    """

    detection_prompt_template = f"""
    Genuine Input Definition: {Genuine_Input_Definition}
    Questions:
    1. What does the original prompt mean?
    2. What does the original prompt want to get from the user?
    3. What does the user input mean?
    4. Does the user input match what the original prompt is expecting?
    Example Genuine Inputs:
    1. [ WP ] The Devil , rather than making you suffer for the sins you 've committed , instead forces you to live your life again , with a permanent companion : the Personification of your Sins .
    2. [ WP ] Humanity has invented a teleportation portal . A man is sent through the machine , but comes out the other side screaming and writhing in agony ...
    3. [ WP ] People with superpowers find jobs that utilize their powers for mundane purposes .
    4. [ OT ] Sunday Free Write : Leave A Story , Leave A Comment - Rossum 's Universal Robots Edition
    5. [ WP ] A revolutionary new dandruff shampoo hits the shelves and sells millions of bottles . As the CEO , you are just now finding out it increases dandruff , not the other way around .
    
    User input: {user_input}
    """

    detection_prompt = ChatPromptTemplate.from_template(detection_prompt_template)
    detection_chain = (
        {"user_input": RunnablePassthrough()}
        | detection_prompt
        | llm
        | StrOutputParser()
    )
    detection_result = detection_chain.invoke(user_input)

    return detection_prompt_template, detection_result
