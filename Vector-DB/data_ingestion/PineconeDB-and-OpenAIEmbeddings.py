import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import Pinecone
from dotenv import load_dotenv
import numpy as np
from utils.embedding_loader import CustomOpenAIEmbeddings

load_dotenv(dotenv_path="C:/Users/ADMIN/Documents/venv/.env")


if __name__ == "__main__":
    # Verify environment variables
    openai_key = os.environ.get("OPENAI_API_KEY")
    pinecone_key = os.environ.get("PINECONE_API_KEY")
    pinecone_index = "learnwithvivek"  # Using the correct index name

    if not all([openai_key, pinecone_key]):
        raise ValueError("Missing required environment variables. Please check your .env file.")

    print("Starting data ingestion...")
    try:
        loader = TextLoader("data\medinublog1.txt", encoding="utf-8")
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)
        print(f"Ingested {len(chunks)} chunks")

        # Initialize custom OpenAI embeddings
        embeddings = CustomOpenAIEmbeddings(
            api_key=openai_key,
            model="text-embedding-3-small"
        )

        print("Ingesting to Pinecone...")
        Pinecone.from_documents(chunks, embeddings, index_name=pinecone_index)
        print("Ingestion complete!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    

