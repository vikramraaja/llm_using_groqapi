import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://127.0.0.1:8000/chat"

# Streamlit UI setup
st.set_page_config(page_title="Groq AI Chat", layout="wide")
st.title("🤖 Groq AI Chatbot")
st.write("Chat with a powerful language model using the Groq API.")

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous chat messages
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_input = st.chat_input("Ask me something...")

if user_input:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send request to FastAPI backend
    response = requests.post(API_URL, json={"prompt": user_input})
    
    if response.status_code == 200:
        bot_reply = response.json()["response"]
    else:
        bot_reply = "Error: Unable to fetch response."

    # Add bot response to chat history
    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

    # Display bot response
    with st.chat_message("assistant"):
        st.markdown(bot_reply)
