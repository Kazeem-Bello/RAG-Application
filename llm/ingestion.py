from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from core.config import settings
from langchain_qdrant import QdrantVectorStore
from langchain_core.documents import Document
import json




class Ingestion:
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        # self.embeddings = None
            
    # load each file to memory 
    def load_pdf_file(self):
        loader = PDFPlumberLoader(self.file_path)
        return loader.load()
    
    def load_json_file(self):
        with open(self.file_path, "r") as file:
            data = json.load(file)
        
        documents = []
        for knowledge_graph in data["hotel_knowledge_base"]:
            doc = Document(
                page_content=(
                    f"category: {knowledge_graph["category"]}\n"
                    f"title: {knowledge_graph["title"]}\n"
                    f"content: {knowledge_graph["content"]}"
                ),
                metadata={
                    "source": self.file_path
                }
            )
            documents.append(doc)
        return documents          
         
    # split each documents into chunks
    def chunking(self, pages):
        splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", " ", ""],
            chunk_size=1500,
            chunk_overlap=150
        )
        return splitter.split_documents(pages)
    
    
    def save_to_vector_store(self, docs):
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            api_key=settings.OPENAI_API_KEY       
        )        
        vector_store = QdrantVectorStore.from_documents(
            documents=docs,
            embedding=embeddings,
            url=settings.QDRANT_BASE_URL,
            collection_name="RAG_Application"
        )
        return "Documents had been successfully uploaded to vector store"
        