from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from google.generativeai.types import HarmCategory, HarmBlockThreshold

llm = GoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    }
    )
prompt_template = """
Please write a short story on the following topic: {user_input}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)
output_parser = StrOutputParser()

chain = (
    {"user_input": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

while True:
    line = input("llm>> ")
    if line == "":
        break
    result = chain.invoke(line)
    print(result)
