import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import numpy as np
from utils.embedding_loader import CustomHuggingFaceEmbeddings
load_dotenv(dotenv_path="C:/Users/ADMIN/Documents/venv/.env")


if __name__ == "__main__":
    print("Starting data ingestion...")
    try:
        # Create a directory for the database if it doesn't exist
        db_directory = "db/faiss_db"
        if not os.path.exists(db_directory):
            os.makedirs(db_directory)

        loader = TextLoader("data\medinublog1.txt", encoding="utf-8")
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)
        print(f"Ingested {len(chunks)} chunks")

        # Initialize custom embeddings
        embeddings = CustomHuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
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
    

