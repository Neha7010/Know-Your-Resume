import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
from llama_index.core import VectorStoreIndex, Settings
from llama_index.readers.file import PDFReader
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import tempfile

# ── Set your Groq API key here ────────────────────────────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")   

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="KnowYourResume",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Sora', sans-serif !important; }

.stApp { background: #0b0f19; color: #e2e8f0; }

[data-testid="stSidebar"] {
    background: #141824 !important;
    border-right: 1px solid #1e2536;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

.stButton > button {
    background: linear-gradient(135deg, #7c6aff, #38bdf8) !important;
    border: none !important;
    border-radius: 10px !important;
    color: white !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important;
    width: 100%;
    padding: 0.6rem 1rem;
    transition: opacity 0.2s;
}
.stButton > button:hover { opacity: 0.85 !important; }

[data-testid="stChatMessage"] {
    background: #141824 !important;
    border: 1px solid #1e2536 !important;
    border-radius: 14px !important;
    margin-bottom: 0.5rem;
}

[data-testid="stChatInput"] textarea {
    background: #141824 !important;
    border: 1px solid #2a3349 !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
}

[data-testid="stFileUploader"] {
    background: #141824 !important;
    border: 2px dashed #2a3349 !important;
    border-radius: 12px !important;
}

.status-ok {
    background: #0d2818; border: 1px solid #34d399;
    border-radius: 10px; padding: 0.75rem 1rem;
    color: #34d399; font-size: 0.87rem;
}
.status-err {
    background: #2a0d0d; border: 1px solid #f87171;
    border-radius: 10px; padding: 0.75rem 1rem;
    color: #f87171; font-size: 0.87rem;
}
.status-warn {
    background: #2a1e0d; border: 1px solid #fbbf24;
    border-radius: 10px; padding: 0.75rem 1rem;
    color: #fbbf24; font-size: 0.87rem;
}

h1, h2, h3 { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "query_engine" not in st.session_state:
    st.session_state.query_engine = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📄 KnowYourResume")
    st.markdown("---")

    uploaded_file = st.file_uploader("📎 Upload PDF", type=["pdf"])
    index_btn = st.button("🔍 Index PDF", use_container_width=True)

    if index_btn:
        if uploaded_file is None:
            st.markdown('<div class="status-warn">⚠️ Upload a PDF first.</div>', unsafe_allow_html=True)
        else:
            with st.spinner("Indexing PDF..."):
                try:
                    # Groq LLM — free & fast!
                    Settings.llm = Groq(
                        model="llama-3.3-70b-versatile",
                        api_key=GROQ_API_KEY,
                    )
                    
                    # Free local embeddings — no OpenAI needed
                    Settings.embed_model = HuggingFaceEmbedding(
                        model_name="BAAI/bge-small-en-v1.5"
                    )

                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(uploaded_file.read())
                        tmp_path = tmp.name

                    reader = PDFReader()
                    documents = reader.load_data(file=tmp_path)
                    index = VectorStoreIndex.from_documents(documents)
                    st.session_state.query_engine = index.as_query_engine(
                        streaming=False, similarity_top_k=4
                    )
                    st.session_state.pdf_name = uploaded_file.name
                    st.session_state.messages = []
                    os.unlink(tmp_path)
                    st.markdown(
                        f'<div class="status-ok">✅ Indexed <b>{uploaded_file.name}</b> ({len(documents)} pages)</div>',
                        unsafe_allow_html=True,
                    )
                except Exception as e:
                    st.markdown(f'<div class="status-err">❌ {e}</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.session_state.pdf_name:
        st.markdown(f"**Active PDF:** `{st.session_state.pdf_name}`")
    else:
        st.markdown("_No PDF indexed yet._")

    st.markdown("---")
    st.markdown("""
**How it works**
1. Upload any PDF
2. Click **Index PDF**
3. Start chatting!

⚡ Powered by **Groq** (free & fast)
    """)

# ── Main chat area ────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center; background: linear-gradient(135deg,#7c6aff,#38bdf8,#34d399); "
    "-webkit-background-clip:text; -webkit-text-fill-color:transparent; font-size:2.2rem;'>"
    "📄KnowYourResume</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align:center; color:#64748b;'>Upload a PDF and ask anything about it</p>",
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    st.markdown("### 💡 Try asking:")
    cols = st.columns(2)
    examples = [
        "Summarize the key points of this document.",
        "What are the main skills and experience mentioned?",
        "List any certifications or education details.",
        "What projects or achievements are highlighted?",
    ]
    for i, ex in enumerate(examples):
        with cols[i % 2]:
            if st.button(ex, key=f"ex_{i}"):
                st.session_state.messages.append({"role": "user", "content": ex})
                if st.session_state.query_engine:
                    with st.spinner("Thinking..."):
                        response = st.session_state.query_engine.query(ex)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": str(response)}
                        )
                else:
                    st.session_state.messages.append(
                        {"role": "assistant", "content": "⚠️ Please index a PDF first."}
                    )
                st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask something about your PDF…"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if st.session_state.query_engine is None:
            reply = "⚠️ Please upload and index a PDF first (use the sidebar)."
        else:
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.query_engine.query(prompt)
                    reply = str(response)
                except Exception as e:
                    reply = f"❌ Error: {e}"
        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})