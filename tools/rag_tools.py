from langchain_core.tools import tool
from services.vector_db import VectorDB
from services.rag import RAGService

@tool
def search_hotel_information(query: str) -> str:
    """
    Search the hotel document and answer questions using only 
    the information available in the hotel pdf.

    Use this tool for questions about hotel facilities,dining,
    hygiene, location, policies, check-in/check-out times, and other hotel-related information.
    """
    try:
        db = VectorDB.load()
        chain = RAGService.create_chain(db)

        response = chain.invoke({
            'input':query
        })

        return response['answer']
    except Exception:
        return 'Unable to retrieve information from the hotel document. Please try again later.'