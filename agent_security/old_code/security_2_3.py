from langgraph.graph import Graph
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Original Prompt
original_prompt = "Write me a short story using the given prompt: {story_prompt}"

# LLM Initialization
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest")

def security_guard_node(user_input):
    Genuine_Input_Definition = (
        "A genuine user input for this application should be a clear and concise prompt for a short story. "
        "It should describe a scenario, setting, or characters that the story will be based on. "
        "Inappropriate inputs include, but are not limited to, offensive language, irrelevant topics, "
        "or any content that does not fit the purpose of generating a short story."
    )

    detection_prompt_template = (
        f"Genuine Input Definition: {Genuine_Input_Definition}\n"
        f"User input: {user_input}\n"
        "Questions:\n"
        "1. What does the original prompt mean?\n"
        "2. What does the original prompt want to get from the user?\n"
        "3. What does the user input mean?\n"
        "4. Does the user input match what the original prompt is expecting?\n"
        "Response:\n"
        "If the user input matches the intent of the original prompt, respond with 'Genuine Input'. "
        "Otherwise, respond with 'Inappropriate Input'. Provide a detailed explanation for your decision."
    )

    detection_prompt = ChatPromptTemplate.from_template(detection_prompt_template)

    detection_chain = (
        {"user_input": RunnablePassthrough()}
        | detection_prompt
        | llm
        | StrOutputParser()
    )

    detection_result = detection_chain.invoke(user_input)

    return detection_prompt_template, detection_result
