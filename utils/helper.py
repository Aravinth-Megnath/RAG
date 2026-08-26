import os

from loaders.pdf_loader import load_pdf

from vectorstore.vector_store import create_vectorstore

from config import DB_PATH


def initialize_database():

    if not os.path.exists(DB_PATH):

        docs = load_pdf("data\hotel_rag_document_v2.pdf")

        create_vectorstore(docs)