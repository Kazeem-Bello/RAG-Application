from llm.model import RAGPipeline


file_paths = [
    "files/City_Insider_Guide.pdf",
    "files/GrandStay_Amenities_Guide.pdf",
    "files/GrandStay_Policies_Handbook.pdf",
    "files/GrandStay_Staff_SOP.pdf",
    "files/grandstay_hotel_knowledge_base.json"
]


RAGPipeline(file_paths).start_ingestion()