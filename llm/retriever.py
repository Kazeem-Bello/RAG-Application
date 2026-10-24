from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from core.config import settings


class Retriever:
    
    def __init__(self, user_input: str):
        self.user_input = user_input
        
        
    def get_vector_db(self):
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY       
        )
        vector_db = QdrantVectorStore.from_existing_collection(
            collection_name="RAG_Application",
            embedding=embeddings,
            url=settings.QDRANT_BASE_URL
        )
        return vector_db
    
    
    def similarity_search(self):
        vector_db = self.get_vector_db() 
        context = vector_db.similarity_search(
            query=self.user_input, 
            k=2
        )
    