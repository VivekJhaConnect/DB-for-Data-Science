import streamlit as st
import os
from langchain_community.vectorstores import FAISS, Chroma, Pinecone
from utils.embedding_loader import CustomOpenAIEmbeddings, CustomHuggingFaceEmbeddings
from dotenv import load_dotenv
import numpy as np

# Load environment variables
load_dotenv(dotenv_path="C:/Users/ADMIN/Documents/venv/.env")

# Initialize embeddings
@st.cache_resource
def get_embeddings(embedding_type):
    if embedding_type == "OpenAI":
        return CustomOpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY"),
            model="text-embedding-3-small"
        )
    else:
        return CustomHuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

# Load vector store
@st.cache_resource
def load_vector_store(db_type, embedding_type):
    embeddings = get_embeddings(embedding_type)
    if db_type == "FAISS":
        return FAISS.load_local("db/faiss_db", embeddings)
    elif db_type == "ChromaDB":
        return Chroma(
            persist_directory="db/chroma_db",
            embedding_function=embeddings,
            collection_name="medinublog"
        )
    elif db_type == "PineconeDB":
        return Pinecone.from_existing_index(
            index_name="learnwithvivek",
            embedding=embeddings
        )
    return None

def main():
    st.set_page_config(
        page_title="Vector Database Search",
        page_icon="🔍",
        layout="wide"
    )

    st.title("🔍 Vector Database Search")
    st.markdown("""
    This application allows you to search through the vector database using semantic similarity.
    Choose your preferred vector database and embedding model, then enter your search query.
    """)

    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        db_type = st.selectbox(
            "Select Vector Database",
            ["FAISS", "ChromaDB", "PineconeDB"],
            help="Choose the vector database to search from"
        )
        
        embedding_type = st.selectbox(
            "Select Embedding Model",
            ["OpenAI", "HuggingFace"],
            help="Choose the embedding model to use"
        )
        
        num_results = st.slider(
            "Number of Results",
            min_value=1,
            max_value=10,
            value=3,
            help="Number of similar documents to retrieve"
        )

    # Main search interface
    search_query = st.text_input(
        "Enter your search query",
        placeholder="Type your question here...",
        help="Enter the text you want to search for"
    )

    if search_query:
        try:
            # Load the vector store
            vectordb = load_vector_store(db_type, embedding_type)
            
            if vectordb:
                # Perform the search
                results = vectordb.similarity_search(search_query, k=num_results)
                
                # Display results
                st.subheader("Search Results")
                for i, doc in enumerate(results, 1):
                    with st.expander(f"Result {i}", expanded=True):
                        st.markdown(doc.page_content)
                        st.markdown("---")
            else:
                st.error("Failed to load the vector database. Please check if the database exists.")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Please enter a search query to begin.")

if __name__ == "__main__":
    main() 