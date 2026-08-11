from loaders.pdf_loader import PDFLoader

docs = PDFLoader.load_pdf(r"C:\Users\ARAVINTH\RAG\data\Aravinth Meganathan - Data Scientist.pdf")

print(f"Pages Loaded : {len(docs)}")

print(docs[0].page_content[:500])