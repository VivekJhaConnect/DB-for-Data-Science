import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import numpy as np
from utils.embedding_loader import CustomOpenAIEmbeddings

load_dotenv(dotenv_path="C:/Users/ADMIN/Documents/venv/.env")



if __name__ == "__main__":
    # Verify environment variables
    openai_key = os.environ.get("OPENAI_API_KEY")

    if not openai_key:
        raise ValueError("Missing OpenAI API key. Please check your .env file.")

    print("Starting data ingestion...")
    try:
        # Create a directory for the database if it doesn't exist
        db_directory = "db/faiss_db_openai"
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)

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

        print("Creating FAISS database...")
        # Create FAISS vector store
        vectordb = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )
        
        # Save the FAISS index and documents
        vectordb.save_local(db_directory)
        print("Database created and saved successfully!")
        
        # Print some information about the database
        print(f"Number of documents in the database: {len(chunks)}")
        print(f"Database location: {os.path.abspath(db_directory)}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")