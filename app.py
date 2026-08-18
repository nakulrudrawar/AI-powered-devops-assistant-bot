"""
app.py
Day 6: Streamlit UI for DevOps Assistant Bot.

What this does:
- Shows a chat-style interface in the browser
- Takes your question, runs it through the RAG pipeline (retrieve + LLM)
- Displays the answer AND which source documents it came from

Run with:
    streamlit run app.py
"""

import streamlit as st
from retrieve import load_vector_store, retrieve_chunks
from generate import build_prompt, ask_llm

st.set_page_config(page_title="DevOps Assistant Bot", page_icon="🛠️")

st.title("🛠️ Ai Powered DevOps Assistant Bot")
st.caption("Ask questions about your AWS setup, runbooks, and logs.")


@st.cache_resource
def get_vector_store():
    """Load the vector store once and reuse it across questions."""
    return load_vector_store()


vector_store = get_vector_store()

# Keep chat history for this session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources used"):
                for source in msg["sources"]:
                    st.markdown(f"- `{source}`")

# Chat input box
question = st.chat_input("Ask a DevOps question...")

if question:
    # Show the user's question
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Run the RAG pipeline
    with st.chat_message("assistant"):
        with st.spinner("Searching docs and thinking..."):
            chunks = retrieve_chunks(vector_store, question)

            if not chunks:
                answer = "No relevant information found in the knowledge base."
                sources = []
            else:
                prompt = build_prompt(question, chunks)
                answer = ask_llm(prompt)
                sources = list({doc.metadata.get("source", "unknown") for doc in chunks})

            st.markdown(answer)
            if sources:
                with st.expander("Sources used"):
                    for source in sources:
                        st.markdown(f"- `{source}`")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )