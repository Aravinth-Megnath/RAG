from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from services.llm import LLM
from services.guardrails import Guardrails
from tools.reservation_tools import (
    create_reservation,
    get_reservation,
    cancel_reservation
)
from tools.rag_tools import search_hotel_information

class AgentService:

    def __init__(self):
        self.llm = LLM.load()

        self.tools = [
            create_reservation,
            get_reservation,
            cancel_reservation,
            search_hotel_information
        ]

        self.tool_map = {
            tool.name: tool for tool in self.tools
        }

        self.llm_with_tools = self.llm.bind_tools(self.tools)

    def is_reservation_request(self, message: str) -> bool:
        message = message.lower()

        reservation_keywords = [
            "book",
            "booking",
            "reserve",
            "reservation",
            "room",
            "cancel my reservation",
            "my reservation",
            "reservation status"
        ]

        return any(keyword in message for keyword in reservation_keywords)

    def run(self, user_message: str,chat_history = None):
        try:
            allowed, message = Guardrails.validate_query(user_message)
            if not allowed:
                return message
            
            if chat_history is None:
                chat_history = []

            messages = [
                SystemMessage(
                    content=(
                        "You are a hotel reservation assistant. "
                        "Use tools when appropriate. "
                        "Never invent missing information. "
                        "If required information is missing, ask the user for it. "
                        "Do not expose unnecessary personal information."
                    )
                )
            ]

            # Add previous conversation
            for msg in chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(
                        HumanMessage(content=f"Assistant: {msg['content']}")
                    )

            # Current user message
            messages.append(HumanMessage(content=user_message))

            # response = self.llm_with_tools.invoke(messages)
            #1.Ask Groq to decide what to do
            response = self.llm_with_tools.invoke([SystemMessage(
                                content="""
                        You are a Hotel Reservation Assistant.

                        You can ONLY help with:
                        - Information contained in the hotel document.
                        - Creating hotel reservations.
                        - Viewing a user's own reservation.
                        - Cancelling a user's own reservation.

                        IMPORTANT:
                        - For ANY question about the hotel, ALWAYS use the
                        search_hotel_information tool.
                        - Do NOT answer hotel questions using your own knowledge.
                        - For reservation requests, use the appropriate reservation tool.
                        - If required reservation information is missing, ask the user for it.
                        - For questions unrelated to the hotel or reservations,
                        do NOT answer using your general knowledge.
                        Politely say that you can only help with hotel information
                        and reservations.
                        - Never expose another guest's reservation or personal information.
                        """
                            ),
                            HumanMessage(content=user_message)
                        ])

            #2. No tool required
            # 2. No tool selected
            if not response.tool_calls:

                if self.is_reservation_request(user_message):
                    return (
                        "Sure, I can help you with the reservation. "
                        "Please provide your check-in date, check-out date, "
                        "guest name, email address, and room preference."
                    )

                return (
                    "I can only help with hotel information and reservations."
                )

            #3. Execute the selected tool
            tool_messages = []
            for tool_call in response.tool_calls:
                tool_name =tool_call['name']
                tool_args = tool_call['args']

                tool = self.tool_map.get(tool_name)

                if tool is None:
                    continue
                tool_result = tool.invoke(tool_args)

                tool_messages.append(
                    ToolMessage(
                        content=str(tool_result),
                        tool_call_id=tool_call['id']
                    )
                )

            if chat_history is None:
                chat_history = []
            #4.Ask Groq to generate final response
            final_response = self.llm.invoke([
                            SystemMessage(
                                content="""
                        You are a Hotel Reservation Assistant.

                        You can ONLY help with:

                        1. Information contained in the hotel document.
                        2. Creating hotel reservations.
                        3. Viewing a user's own reservation.
                        4. Cancelling a user's own reservation.

                        For hotel information questions:
                        - Use the search_hotel_information tool.
                        - Do not answer hotel questions using your own knowledge.

                        For reservation requests:
                        - Use the appropriate reservation tool.
                        - Never invent missing information.
                        - Ask the user for missing required information.

                        For questions unrelated to the hotel or reservations:
                        - Do not answer using your general knowledge.
                        - Politely explain that you can only help with hotel information
                        and reservations.

                        Never expose another guest's reservation or personal information.
                        """
                            ),
                            HumanMessage(content=user_message),
                            response,
                            *tool_messages
                        ])

            return final_response.content
        except Exception as e:
            print(f'Agent error: {e}')
            return(
                 'Sorry, something went wrong. Please try again.'
            )