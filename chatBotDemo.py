import streamlit as st
import os
from dotenv import load_dotenv

# LangChain
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="C++ Nexus AI",
    page_icon="🤖",
    layout="wide", # Wider layout for a modern feel
    initial_sidebar_state="expanded",
)

# ----------------------------
# CYBER-MODERN THEME (CSS)
# ----------------------------
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    :root {
        --primary: #00f2fe;
        --secondary: #4facfe;
        --bg-dark: #0a0b10;
        --glass: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
        --text-main: #e0e6ed;
    }

    /* Background and Font */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1e2a4a, #0a0b10);
        font-family: 'Inter', sans-serif;
        color: var(--text-main);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 11, 16, 0.95) !important;
        border-right: 1px solid var(--glass-border);
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem !important;
        max-width: 1000px;
    }

    /* Glass Cards */
    .nexus-card {
        background: var(--glass);
        backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }

    /* Gradient Title */
    .nexus-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #00f2fe, #4facfe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        border-radius: 15px;
        margin-bottom: 15px;
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid var(--glass-border) !important;
    }

    /* Status Indicator */
    .status-tag {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 50px;
        background: rgba(0, 242, 254, 0.1);
        color: #00f2fe;
        font-size: 0.8rem;
        font-weight: 600;
        border: 1px solid rgba(0, 242, 254, 0.3);
        margin-bottom: 10px;
    }

    /* Custom Input */
    .stChatInputContainer textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--glass-border) !important;
        color: white !important;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 10px;
        background: linear-gradient(45deg, #00f2fe, #4facfe);
        color: black;
        font-weight: 700;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
    }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# LOGIC & DATA
# ----------------------------
load_dotenv()
FILE_PATH = "C++_Introduction.txt"

@st.cache_resource
def build_vectorstore():
    loader = TextLoader(FILE_PATH, encoding="utf-8")
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=180)
    chunks = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-miniLM-L6-v2")
    return FAISS.from_documents(chunks, embeddings)

if not os.path.exists(FILE_PATH):
    st.error(f"🚨 Missing knowledge file: {FILE_PATH}")
    st.stop()

vectorstore = build_vectorstore()

# ----------------------------
# HEADER UI
# ----------------------------
with st.container():
    st.markdown('<span class="status-tag">● SYSTEM ACTIVE</span>', unsafe_allow_html=True)
    st.markdown('<div class="nexus-title">C++ NEXUS AI</div>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 1.1rem;">Instant documentation retrieval for C++ Core Concepts.</p>', unsafe_allow_html=True)

# ----------------------------
# SIDEBAR
# ----------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6132/6132222.png", width=80)
    st.markdown("### 🛠 Configuration")
    
    k_val = st.slider("Context Density (K)", 1, 10, 3)
    show_sources = st.checkbox("Show Reference Chunks", value=True)
    
    st.markdown("---")
    st.markdown("### 📁 Active File")
    st.info(f"`{FILE_PATH}`")
    
    if st.button("Clear Neural Links (Reset)"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------
# CHAT INTERFACE
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Layout for chat and info
col1, col2 = st.columns([2, 1])

with col1:
    # Message Display
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_query = st.chat_input("Ask about Classes, Pointers, or Memory Management...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Retrieval Logic
        retriever = vectorstore.as_retriever(search_kwargs={"k": k_val})
        docs = retriever.invoke(user_query)

        if not docs:
            answer = "⚠️ No matching data found in the local C++ Nexus."
        else:
            extracted = "\n\n".join([f"🔹 {d.page_content.strip()}" for d in docs])
            answer = f"**Retrieval Success:**\n\n{extracted}"
            
            if show_sources:
                sources_text = "\n".join([f"- Fragment from: `{d.metadata.get('source')}`" for d in docs])
                answer += f"\n\n---\n**Data Sources:**\n{sources_text}"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

with col2:
    st.markdown("""
    <div class="nexus-card">
        <h4>⚡ Quick Tips</h4>
        <ul style="font-size: 0.9rem; color: #94a3b8;">
            <li>Ask specific questions like "How do destructors work?"</li>
            <li>Use the slider to get more or less detail.</li>
            <li>This tool is <b>offline-first</b> (No LLM).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
