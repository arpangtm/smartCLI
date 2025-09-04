from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OllamaEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
import chromadb
import click
import os

## Embedding and DB setup
def RAG_Setup(folder_path):  
    if not os.path.isdir(folder_path):
        click.secho("Error: " + folder_path + " is not a folder", fg='red')
        return
    embeddings = OllamaEmbeddings(
        model="mxbai-embed-large:latest",
    )
    chroma_client = chromadb.Client()


    ## Text Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )

    loader = DirectoryLoader(
        folder_path,
        glob="**/*.txt"  # recursively find all txt files
    )
    documents = loader.load()

    ## Split documents into chunks
    splitted_docs = text_splitter.split_documents(documents)

    script_path = os.path.abspath(__file__)
    vector_store = Chroma.from_documents(
        documents=splitted_docs,
        embedding=embeddings,
        persist_directory=os.path.join(os.path.dirname(script_path), "chroma_db")
    )

if __name__ == "__main__":
    RAG_Setup("/Users/arpangautam/Developer/code/python/nexcli/src/RAG/sample_data")
    print("RAG Setup Complete")


