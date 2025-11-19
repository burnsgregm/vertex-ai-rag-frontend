
import streamlit as st
import requests
import json

# --- Configuration ---
st.set_page_config(page_title="Medical RAG Assistant", page_icon="🩺")

st.title("🩺 General Surgery AI Assistant")
st.markdown("Ask questions based on the *Illustrative Handbook of General Surgery*.")

# --- Sidebar & Secrets Handling ---
with st.sidebar:
    st.header("Configuration")
    
    # Try to get the URL from Streamlit Secrets first
    if "BACKEND_API_URL" in st.secrets:
        api_url = st.secrets["BACKEND_API_URL"]
        st.success("API Connected via Secrets ✅")
    else:
        api_url = st.text_input(
            "Backend API URL", 
            placeholder="https://rag-backend-api-....a.run.app",
            help="Paste the URI you received after deploying the Cloud Function."
        )
        st.warning("Enter API URL manually or set BACKEND_API_URL in Streamlit Secrets.")

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

    # 2. Validation
    if not api_url:
        st.error("Please configure the Backend API URL in the sidebar.")
        st.stop()

    # 3. Call Backend
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")

        try:
            # Call the Google Cloud Function
            response = requests.post(api_url, json={"query": prompt})
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get("answer", "No answer returned.")
                placeholder.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                placeholder.error(f"Backend Error ({response.status_code}): {response.text}")
        
        except Exception as e:
            placeholder.error(f"Connection Error: {e}")
