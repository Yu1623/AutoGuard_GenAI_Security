"""
The security guard node using anomaly few-shot.
Modified to return the detection LLM"s classification.
"""

from langgraph.graph import Graph
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from google.generativeai.types import HarmCategory, HarmBlockThreshold

def security_guard_node(user_input: str) -> str:
    llm = GoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        }
    )
    
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
    Answer whether the input is "Genuine Input" or "Inappropriate Input" and provide a detailed explanation.
    """
    
    detection_prompt = ChatPromptTemplate.from_template(detection_prompt_template)
    
    chain = (
        {'user_input': RunnablePassthrough()}
        | detection_prompt
        | llm
        | StrOutputParser()
    )
    
    detection_result = chain.invoke(user_input)

    return detection_prompt_template, user_input, detection_result
