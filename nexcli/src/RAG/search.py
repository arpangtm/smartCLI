from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_community.vectorstores import Chroma
# from langchain.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
import os
from os import getenv
from dotenv import load_dotenv

load_dotenv()

def RAG_Search(query):

  embeddings = OllamaEmbeddings(
      model="mxbai-embed-large:latest",
  )

  BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
  CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
  vector_store = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)

  # Retrieve top 5 most relevant documents
  results = vector_store.similarity_search(str(query), k=3)

  # Print the content of the results

  prompt_template = ChatPromptTemplate([
      ("system", "You are a helpful assistant. This is the context you have: {context}. You may or maynot require the context to answer the following questions. If you don't require the context, just answer the question as is. Don't say, based on your information. If used context, answer as if you knew it."),
      ("user", "{question}")
  ])


  llm = ChatOpenAI(
    api_key=getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    model="meta-llama/llama-3.3-70b-instruct:free",
  )

  llm_chain = prompt_template | llm
  res = llm_chain.invoke({"context":results, "question":query})
  return res.content



if __name__ == "__main__":
  query = "Where do I study?"
  print(RAG_Search(query))


  






