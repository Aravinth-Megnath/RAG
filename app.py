import streamlit as st

from services.agent import AgentService


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Hotel Reservation Assistant",
    page_icon="🏨",
    layout="wide"
)


# ---------------------------------------------------
# Agent
# ---------------------------------------------------

@st.cache_resource
def load_agent():
    return AgentService()


agent = load_agent()


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("🏨 Hotel Assistant")

    st.markdown("---")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.info(
        "You can ask questions about the hotel "
        "or manage your reservation."
    )


# ---------------------------------------------------
# Main UI
# ---------------------------------------------------

st.title("🏨 Hotel Reservation Assistant")

st.caption(
    "Ask about the hotel, create a reservation, "
    "view your reservation, or cancel it."
)


# ---------------------------------------------------
# Display Chat History
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ---------------------------------------------------
# User Input
# ---------------------------------------------------

user_message = st.chat_input(
    "Ask something about the hotel..."
)


if user_message:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    with st.chat_message("user"):
        st.markdown(user_message)

    # Agent response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = agent.run(user_message, chat_history=st.session_state.messages)

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:

                st.error(
                    "Sorry, something went wrong. "
                    "Please try again."
                )

                print(e)