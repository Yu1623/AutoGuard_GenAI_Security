from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import WikipediaLoader
from langchain_community.document_loaders.async_html import AsyncHtmlLoader
from langchain_community.document_loaders.web_base import WebBaseLoader
from langsmith import Client
import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "LangSmith Introduction"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
client = Client()

#Document loading
vectorstore = Chroma(
        persist_directory="./rag_data/.chromadb",
        embedding_function=GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            task_type="retrieval_query"
        )
    )

def load_docs(vectorstore, docs):
    """
    Debugging code to see what is being loaded
    for doc in docs:
        print("Document: ", doc.page_content)
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
    splits = text_splitter.split_documents(docs)
    article_chunks = [i for i in range(len(splits)) if '<p>' in splits[i].page_content]
    new_splits = []
    for i in article_chunks:
        new_split = splits[i]
        new_splits += [new_split]
    vectorstore.add_documents(documents=new_splits)

def load_urls(vectorstore, urls):
    print(f"Documents waiting to be loaded: {urls}")
    docs = AsyncHtmlLoader(urls, trust_env = True, verify_ssl = False).load()
    print(f"Loading {urls} ...")
    load_docs(vectorstore, docs)
    print(f"{urls} loaded")

def load_wiki(vectorstore, query):
    """
    The size of the wikipedia pages is very large so not all of the content in the pages can be loaded
    """
    print(f"Documents waiting to be loaded: {query}")
    docs = WebBaseLoader(query).load_and_split()
    for doc in docs:
        print(doc)
    """
    Documents loaded using WikipediaLoader
    docs = WikipediaLoader(query=query, doc_content_chars_max = 12000).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
    splits = text_splitter.split_documents(docs)
    """
    print(f"Loading {query}")
    vectorstore.add_documents(documents = docs)
    print(f"{query} loaded")

def format_docs(docs):
    return "\n""\n".join(doc.page_content for doc in docs)

load_wiki(vectorstore, ["https://en.wikipedia.org/wiki/Ocean_acidification", "https://en.wikipedia.org/wiki/Wildlife_conservation", "https://en.wikipedia.org/wiki/Overexploitation"])
#load_wiki(vectorstore, ["Ocean Acidification", "Climate Change"])
load_urls(vectorstore, ["https://www.nwf.org/Educational-Resources/Wildlife-Guide/Understanding-Conservation", "https://awionline.org/content/list-endangered-species"])

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
document_data_sources = set()
for document_metadata in retriever.vectorstore.get()['metadatas']:
    document_data_sources.add(document_metadata['source'])

#Build model
llm = GoogleGenerativeAI(model="gemini-pro")
output_parser = StrOutputParser()

def wildlife_conservationist(message):
    prompt = PromptTemplate.from_template("You are an expert on wildlife conservation. You are eager to inform humans on wildlife conservation efforts around the world. You are eager to encourage humans to take actions to protect the environment and to provide them with ways to do so. Use information provided in {context}. If you don't know the answer, just say that you don't know. Message: {message}"
            )
    chain = (
            {"context": retriever | format_docs, "message": RunnablePassthrough()}
            | prompt
            | llm
            | output_parser
    )
    result=chain.invoke(message)
    return(result)

print("Welcome to wildlife conservation site. Please ask our expert on aspects of wildlife conservation and destruction covered in the sources listed below.")
for doc in document_data_sources:
    print(f"    {doc}")

while True:
    message=input("llm>>")
    if message:
        if message=="STOP":
            break
        else:
            print(wildlife_conservationist(message))
    else:
        print("If you want to end, enter 'STOP'")
