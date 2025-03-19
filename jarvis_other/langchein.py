from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

os.environ['LANGCHAIN_TRACING_V2'] = "true"
os.environ['LANGCHAIN_API_KEY'] = "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"
os.environ['TAVILY_API_KEY'] = "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"

# search = TavilySearchResults()

# result = search.invoke("Какая погода в Москве?")

loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)
vector = FAISS.from_documents(documents, OpenAIEmbeddings(api_key='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'))
retriever = vector.as_retriever()

print(retriever.invoke("how to upload a dataset")[0])

