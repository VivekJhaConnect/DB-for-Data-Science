import os
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_pinecone import Pinecone
from dotenv import load_dotenv
import numpy as np
from utils.embedding_loader import CustomHuggingFaceEmbeddings

load_dotenv(dotenv_path="C:/Users/ADMIN/Documents/venv/.env")

class CustomHuggingFaceEmbeddings(HuggingFaceEmbeddings):
    def embed_documents(self, texts):
        # Get embeddings from the parent class
        embeddings_list = super().embed_documents(texts)
        
        # Pad each embedding to 1024 dimensions
        padded_embeddings = []
        for emb in embeddings_list:
            # Pad with zeros to reach 1024 dimensions
            padded_emb = np.pad(emb, (0, 1024 - len(emb)), mode='constant')
            padded_embeddings.append(padded_emb.tolist())
        
        return padded_embeddings

if __name__ == "__main__":
    # Verify environment variables
    pinecone_key = os.environ.get("PINECONE_API_KEY")
    pinecone_index = "learnwithvivek"  # Using the correct index name

    if not pinecone_key:
        raise ValueError("Missing Pinecone API key. Please check your .env file.")

    print("Starting data ingestion...")
    try:
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

        print("Ingesting to Pinecone...")
        Pinecone.from_documents(chunks, embeddings, index_name=pinecone_index)
        print("Ingestion complete!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    

