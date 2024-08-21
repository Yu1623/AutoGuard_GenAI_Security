from langgraph.graph import Graph
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Step 2: Extract the prompt and LLM initialization
original_prompt = "Write me a short story using the given prompt: {story_prompt}"

# Initialize the LLM
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")

# Step 3, 4, and 5: Create security_guard_node function with detection prompt and LLM chain
def security_guard_node(user_input):
    detection_prompt_template = f"""
    Genuine Input Definition: A genuine input should be a coherent and creative prompt for generating a short story. It should not contain inappropriate, harmful, or unrelated content.
    Questions to determine if the input is genuine:
    1. What does "original_prompt" mean?
    2. What does "original_prompt" want to get from the user?
    3. What does "user_input" mean?
    4. Does "user_input" match what "original_prompt" is expecting?
    User input: {user_input}

    Examples of genuine inputs:
    1. [ WP ] Heaven doesn't know how you died, only that all souls fall into three categories: Homicide, Suicide, Natural Causes. Upon your arrival at the pearly gates, your name is incorrectly listed as a suicide.
    2. [ TT ] Choose one level from Super Mario Brothers on the NES and adapt it to a CYOA story.

    The response should be "Genuine Input" if "user_input" matches the intent of "original_prompt" and "Inappropriate Input" if not. Provide a detailed explanation for the decision.
    """
    detection_prompt = ChatPromptTemplate.from_template(detection_prompt_template)
    
    # Create the chain for detection
    detection_chain = (
        {"user_input": RunnablePassthrough()}
        | detection_prompt
        | llm
        | StrOutputParser()
    )
    
    # Obtain the result of the detection chain
    detection_result = detection_chain.invoke(user_input)
    
    return detection_prompt_template, detection_result
