from services.vector_db import VectorDB

db = VectorDB.load()

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)

docs = retriever.invoke("What is this document about?")

for i, doc in enumerate(docs, 1):
    print("=" * 80)
    print(f"Chunk {i}")
    print(doc.page_content[:400])
    print(doc.metadata)