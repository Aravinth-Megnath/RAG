import streamlit as st
from services.agent import AgentService

# Page Setup
st.set_page_config(page_title="Hotel Reservation Assistant", page_icon="🏨", layout="wide")


# Cache Agent Initialization
@st.cache_resource
def get_agent():
    return AgentService()


agent = get_agent()

# Initialize Chat Session History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Controls
with st.sidebar:
    st.title("🏨 Hotel Assistant")
    st.markdown("---")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")
    st.info("Ask questions about hotel policies, check-in times, or manage your reservation.")

# Main Interface Header
st.title("🏨 Hotel Reservation Assistant")
st.caption("Ask about the hotel, create a reservation, view your booking, or cancel it.")

# Render Chat History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Chat Input Handler
if prompt := st.chat_input("Ask something about the hotel..."):
    # Display user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent.run(prompt, chat_history=st.session_state.messages)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("Sorry, something went wrong. Please try again.")
                print(f"App error: {e}")