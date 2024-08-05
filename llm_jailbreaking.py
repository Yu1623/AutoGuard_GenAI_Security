from langchain_google_genai import GoogleGenerativeAI

llm = GoogleGenerativeAI(model = "gemini-pro", temperature = 0)

while True:
    try:
        message = input("llm>>")
        if message:
            print(llm.invoke(message))
        else:
            break
    except Exception as e:
        print(e)
