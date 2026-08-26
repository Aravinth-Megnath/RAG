from loaders.pdf_loader import PDFLoader
from services.vector_db import VectorDB

docs = PDFLoader.load_pdf("data\hotel_rag_document_v2.pdf")

db = VectorDB.create(docs)

print("Database Created Successfully")