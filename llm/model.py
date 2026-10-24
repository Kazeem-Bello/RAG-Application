from langchain_openai import ChatOpenAI
from core.config import settings
from llm.ingestion import Ingestion
from pathlib import Path
from typing import List



llm = ChatOpenAI(
    model="gpt-5.4-mini",
    api_key=settings.OPENAI_API_KEY
)


file_path = [
    "files/City_Insider_Guide.pdf",
    "files/GrandStay_Amenities_Guide.pdf",
    "files/GrandStay_Policies_Handbook.pdf",
    "files/GrandStay_Staff_SOP.pdf",
    "files/grandstay_hotel_knowledge_base.json"
]
absolute_path = Path(__file__).parents[1]

class RAGPipeline:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        
    def start_ingestion(self):
        try: 
            documents = []
            for file_path in self.file_paths:
                ingestion = Ingestion(file_path=f"{absolute_path}/{file_path}")
                if Path(file_path).suffix == ".pdf":
                    pages = ingestion.load_pdf_file()
                    chunks = ingestion.chunking(pages)
                    documents.extend(chunks)
                if Path(file_path).suffix == ".json":
                    chunks = ingestion.load_json_file()
                    documents.extend(chunks)
            
            vector_store = ingestion.save_to_vector_store(documents)
            return vector_store
        except Exception as e:
            raise RuntimeError(f"Error ingestion data: {str(e)}") from e