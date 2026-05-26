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
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/upload", files=files)
                    
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Document processed successfully!"))
                    else:
                        st.error("Failed to process document.")
                except Exception as e:
                    st.error(f"Connection error: {e}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your documents:"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    payload = {
        "message": prompt,
        "history": st.session_state.messages
    }
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{BACKEND_URL}/chat", json=payload)
                if response.status_code == 200:
                    bot_reply = response.json()["response"]
                    st.markdown(bot_reply)
                    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
                else:
                    st.error("Error communicating with backend server.")
            except Exception as e:
                st.error(f"Connection error: {e}")