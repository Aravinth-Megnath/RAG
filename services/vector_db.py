from langchain_chroma import Chroma
from services.embeddings import EmbeddingModel
from config import DB_DIRECTORY

class VectorDB:
    """Manages ChromaDB vector store creation and loading."""

    @classmethod
    def create(cls, docs) -> Chroma:
        embeddings = EmbeddingModel.load_embeddings()
        db = Chroma.from_documents(
            documents=docs,
            embedding=embeddings,
            persist_directory=DB_DIRECTORY
        )
        print(f"[VectorDB] Created database with {len(docs)} chunks at '{DB_DIRECTORY}'.")
        return db

    @classmethod
    def load(cls) -> Chroma:
        embeddings = EmbeddingModel.load_embeddings()
        return Chroma(
            persist_directory=DB_DIRECTORY,
            embedding_function=embeddings
        )