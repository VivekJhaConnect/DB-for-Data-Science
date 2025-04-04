from dotenv import load_dotenv
import os

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from utils.embedding_loader import CustomOpenAIEmbeddings

from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


load_dotenv(dotenv_path="C:/Users/ADMIN/Documents/venv/.env")


if __name__ == "__main__":
    print("Retrieving data from the database...")
    embeddings = CustomOpenAIEmbeddings(model="text-embedding-3-small")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    query = "What is Pinecone in machine learning?"
    chain = PromptTemplate.from_template(template=query) | llm
    # result = chain.invoke(input={})
    # print(result.content)

    # Verify environment variables
    pinecone_key = os.environ.get("PINECONE_API_KEY")
    pinecone_index = "learnwithvivek"  # Using the correct index name

    if not pinecone_key:
        raise ValueError("Missing Pinecone API key. Please check your .env file.")

    print("Starting data ingestion...")
    try:
        vectorstore = PineconeVectorStore(
            index_name=pinecone_index,
            embedding=embeddings,
            pinecone_api_key=pinecone_key,
        )
    except Exception as e:
        print(f"Error creating PineconeVectorStore: {e}")
        raise
    
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)
    retrieval_qa_chain = create_retrieval_chain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=combine_docs_chain,
    )
    
    result = retrieval_qa_chain.invoke(input={"input": query})
    print(result)
    
    print("Data ingestion complete.")
