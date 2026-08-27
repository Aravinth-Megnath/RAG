from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
from services.llm import LLM
from services.guardrails import Guardrails
from tools.reservation_tools import create_reservation, get_reservation, cancel_reservation
from tools.rag_tools import search_hotel_information

SYSTEM_PROMPT = """You are a Hotel Reservation Assistant.

You can ONLY help with:
1. Information contained in the hotel document.
2. Creating hotel reservations.
3. Viewing a user's own reservation.
4. Cancelling a user's own reservation.

IMPORTANT:
- For ANY question about the hotel, ALWAYS use the search_hotel_information tool.
- Do NOT answer hotel questions using your own knowledge.
- For reservation requests, use the appropriate reservation tool.
- If required reservation information is missing, ask the user for it.
- For questions unrelated to the hotel or reservations, do NOT answer using your general knowledge. Politely say that you can only help with hotel information and reservations.
- Never expose another guest's reservation or personal information.
"""

RESERVATION_KEYWORDS = {"book", "booking", "reserve", "reservation", "room", "cancel my reservation", "my reservation", "reservation status"}

class AgentService:
    def __init__(self):
        self.llm = LLM.load()
        self.tools = [create_reservation, get_reservation, cancel_reservation, search_hotel_information]
        self.tool_map = {tool.name: tool for tool in self.tools}
        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def is_reservation_request(self, message: str) -> bool:
        msg_lower = message.lower()
        return any(kw in msg_lower for kw in RESERVATION_KEYWORDS)

    def _format_history(self, chat_history):
        messages = []
        for msg in chat_history or []:
            content = msg["content"]
            messages.append(HumanMessage(content=content) if msg["role"] == "user" else AIMessage(content=content))
        return messages

    def run(self, user_message: str, chat_history=None) -> str:
        try:
            allowed, guard_msg = Guardrails.validate_query(user_message)
            if not allowed:
                return guard_msg

            system_msg = SystemMessage(content=SYSTEM_PROMPT)
            history_msgs = self._format_history(chat_history)
            current_user_msg = HumanMessage(content=user_message)

            # 1. LLM Tool Selection Call
            prompt_messages = [system_msg] + history_msgs + [current_user_msg]
            response = self.llm_with_tools.invoke(prompt_messages)

            # 2. Handle Case with No Tool Calls
            if not response.tool_calls:
                if self.is_reservation_request(user_message):
                    return (
                        "Sure, I can help you with the reservation. "
                        "Please provide your check-in date, check-out date, "
                        "guest name, email address, and room preference."
                    )
                return "I can only help with hotel information and reservations."

            # 3. Execute Selected Tools
            tool_messages = [
                ToolMessage(content=str(self.tool_map[call["name"]].invoke(call["args"])), tool_call_id=call["id"])
                for call in response.tool_calls if call["name"] in self.tool_map
            ]

            # 4. Generate Final Response with Tool Results
            final_messages = prompt_messages + [response] + tool_messages
            final_response = self.llm.invoke(final_messages)

            return final_response.content

        except Exception as e:
            print(f"Agent error: {e}")
            return "Sorry, something went wrong. Please try again."