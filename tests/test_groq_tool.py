from services.llm import LLM
from tools.reservation_tools import create_reservation, get_reservation, cancel_reservation
from tools.rag_tools import search_hotel_information
from langchain_core.messages import ToolMessage

llm = LLM.load()

tools = [create_reservation, get_reservation, cancel_reservation, search_hotel_information]
tool_map = {
    tool.name: tool for tool in tools
}

llm_with_tools = llm.bind_tools(tools)

user_message = (
    "What is the cancellation policy of the hotel?"
)
user_message = (
    "I would like to book a room from September 20, 2026 "
    "to September 22, 2026. "
    "My name is Aravinth and my email is "
    "aravinth.recruiting@gmail.com. "
    "I prefer a Deluxe room."
)
user_message = (
    "Please show me the details of my reservation with ID 6. "
    "My email is aravinth.recruiting@gmail.com."
)
user_message = (
    "I want to cancel my reservation with ID 6. "
    "My email is aravinth.recruiting@gmail.com."
)
# 1. Ask Groq
response = llm_with_tools.invoke(user_message)

print("TOOL CALL:")
print(response.tool_calls)

# 2. Execute the selected tool
tool_call = response.tool_calls[0]

tool = tool_map[tool_call["name"]]
tool_result = tool.invoke(tool_call["args"])

print("\nTOOL RESULT:")
print(tool_result)

# 3. Give result back to Groq
tool_message = ToolMessage(
    content=str(tool_result),
    tool_call_id=tool_call["id"]
)

final_response = llm.invoke([
    ("system", "Respond clearly to the user based on the tool result."),
    ("human", user_message),
    response,
    tool_message
])

print("\nFINAL RESPONSE:")
print(final_response.content)