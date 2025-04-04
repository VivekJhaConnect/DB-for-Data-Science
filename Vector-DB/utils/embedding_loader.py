from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
import numpy as np

# Custom embedding classes
class CustomOpenAIEmbeddings(OpenAIEmbeddings):
    def embed_documents(self, texts):
        # Get embeddings from OpenAI
        embeddings_list = super().embed_documents(texts)
        
        # Truncate each embedding to 1024 dimensions
        truncated_embeddings = []
        for emb in embeddings_list:
            # Take only the first 1024 dimensions
            truncated_emb = emb[:1024]
            truncated_embeddings.append(truncated_emb)
        
        return truncated_embeddings


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
