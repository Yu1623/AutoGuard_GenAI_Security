
from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-pro")
chunkList = []
for chunks in llm.stream("Write me a short poem about a rabbit"):
    print(chunks,end="--chunks--")
    chunkList += [chunks]
print(chunkList)
