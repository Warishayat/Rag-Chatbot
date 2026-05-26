import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("📂 Conversational RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Document Management")
    uploaded_file = st.file_uploader("Upload reference documents", type=["pdf", "docx", "txt"])
    
    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Analyzing and vectorizing document..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{BACKEND_URL}/upload", files=files)
                
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error("Failed to process document.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your documents:"):
    st.chat_message("user").markdown(prompt)
    
    # Store history matching the Backend Schema format
    payload = {
        "message": prompt,
        "history": st.session_state.messages
    }
    
    # Append user question to local state
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(f"{BACKEND_URL}/chat", json=payload)
            if response.status_code == 200:
                bot_reply = response.json()["response"]
                st.markdown(bot_reply)
                st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            else:
                st.error("Error communicating with backend server.")