from tools.rag_tools import search_hotel_information

result = search_hotel_information.invoke(
    {'query': 'What is the cancellation policy'}

)
print(result)