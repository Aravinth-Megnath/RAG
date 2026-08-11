from services.vector_db import VectorDB
from services.rag import RAGService

db = VectorDB.load()

chain = RAGService.create_chain(db)

response = chain.invoke(
    {
        "input": "What is this document about?"
    }
)

print(response)