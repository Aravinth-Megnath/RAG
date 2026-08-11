from loaders.pdf_loader import PDFLoader
from services.vector_db import VectorDB

docs = PDFLoader.load_pdf(r"C:\Users\ARAVINTH\RAG\data\Aravinth Meganathan - Data Scientist.pdf")

db = VectorDB.create(docs)

print("Database Created Successfully")