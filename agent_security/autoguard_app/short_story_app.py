from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from google.generativeai.types import HarmCategory, HarmBlockThreshold

''' Set the LLM with security settings turned off '''
llm = GoogleGenerativeAI(
    model="gemini-1.5-pro-latest",
    safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    }
    )

''' Create the prompt '''
prompt_template = """
Please write a short story on the following topic: {user_input}
"""
prompt = ChatPromptTemplate.from_template(prompt_template)

''' Set the output parser '''
output_parser = StrOutputParser()

''' Create the LLM LangChain '''
chain = (
    {"user_input": RunnablePassthrough()}
    | prompt
    | llm
    | output_parser
)

''' Execute the LLM application '''
while True:
    line = input("llm>> ")
    if line == "":
        break
    result = chain.invoke(line)
    print(result)
