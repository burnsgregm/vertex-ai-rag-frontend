
import streamlit as st
import requests
import json

# --- Hardcoded Configuration ---
API_URL = "https://rag-backend-api-lqgrtseknq-uc.a.run.app"

# --- App Setup ---
st.set_page_config(page_title="Medical RAG Assistant", page_icon="🩺")

st.title("🩺 General Surgery AI Assistant")
st.markdown("Ask questions based on the *Illustrative Handbook of General Surgery*.")

# --- Sidebar ---
with st.sidebar:
    st.header("System Status")
    st.success(f"Connected to Backend API")
    st.markdown(f"`{API_URL}`")
    st.divider()
    st.info("Frontend: Streamlit Cloud\nBackend: Google Cloud Functions (Vertex AI + FAISS)")

# --- Chat Logic ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
if prompt := st.chat_input("What are the complications of an appendectomy?"):
    # 1. Show User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Call Backend
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")

        try:
            # Call the Google Cloud Function
            response = requests.post(API_URL, json={"query": prompt})
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer returned.")
                placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                placeholder.error(f"Backend Error ({response.status_code}): {response.text}")
        
        except Exception as e:
            placeholder.error(f"Connection Error: {e}")
