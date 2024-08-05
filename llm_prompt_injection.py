from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.messages import SystemMessage
from langchain_core.prompts import HumanMessagePromptTemplate
from operator import itemgetter
llm = GoogleGenerativeAI(model = "gemini-pro", temperature = 0)

def input_validation(topic):
    topic_splits = topic.split()
    print(topic_splits)
    malicious = ["forget", "remove", "prompt", "instructions", "instruction"]
    for i in topic_splits:
        i = i.lower()
        if i in malicious:
            print("Suspicious activity!")
            topic = "Detected suspicious activity."
    print(topic)
    return topic

prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=(
                    "You are a helpful assistant who knows all about jokes. You will create a joke out of the user's topic."
                )
            ),
            HumanMessagePromptTemplate.from_template("{topic}")
        ]
)
output_parser = StrOutputParser()

chain = (
        {"topic": itemgetter("topic") | RunnableLambda(input_validation)}
        | prompt
        | llm
        | output_parser
)

while True:
    try:
        line = input("llm>>")
        if line:
            print(chain.invoke({"topic": line}))
        else:
            break
    except Exception as e:
        print(e)
