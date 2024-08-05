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
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
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

load_urls(vectorstore, ["https://www.nwf.org/Educational-Resources/Wildlife-Guide/Understanding-Conservation", "https://nhpbs.org/natureworks/nwep16b.htm", "https://defenders.org/blog/2023/06/what-habitat-restoration-and-why-it-important", "https://www.wcs.org/about-us", "https://defenders.org/our-work", "https://defenders.org/blog/2024/01/top-takeaways-national-climate-assessment", "https://www.nwf.org/Our-Work", "https://www.nhm.ac.uk/discover/news/2022/october/wildlife-populations-crashed-by-69-within-less-than-a-lifetime.html"])


retriever = vectorstore.as_retriever()
document_data_sources = set()
for document_metadata in retriever.vectorstore.get()['metadatas']:
    document_data_sources.add(document_metadata['source'])

#Build model
llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0)
output_parser = StrOutputParser()

def wildlife_conservationist(message):
    prompt = PromptTemplate.from_template("You are a wildlife expert on question-answer tasks. Use ONLY the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Question: {message} Context: {context} Answer:"
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
