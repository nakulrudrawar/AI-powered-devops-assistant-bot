"""
retrieve.py
Step 2 of the RAG pipeline for DevOps Assistant Bot.

What this script does:
1. Connects to the ChromaDB you already built with ingest.py
2. Takes a question as input
3. Returns the most relevant chunks from your data

Run this to test retrieval:
    python retrieve.py
"""

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ---- Settings (must match ingest.py) ----
CHROMA_FOLDER = "./chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3  # how many chunks to retrieve per question


def load_vector_store():
    """Connect to the existing ChromaDB (does not recreate it)."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_store = Chroma(
        persist_directory=CHROMA_FOLDER,
        embedding_function=embeddings,
    )
    return vector_store


def retrieve_chunks(vector_store, question, top_k=TOP_K):
    """Find the top_k most relevant chunks for a given question."""
    results = vector_store.similarity_search(question, k=top_k)
    return results


def print_results(question, results):
    print("\n" + "=" * 60)
    print(f"QUESTION: {question}")
    print("=" * 60)
    if not results:
        print("No relevant chunks found.")
        return
    for i, doc in enumerate(results, start=1):
        source = doc.metadata.get("source", "unknown")
        print(f"\n--- Chunk {i} (source: {source}) ---")
        print(doc.page_content.strip())


def main():
    vector_store = load_vector_store()

    # Sample test questions - edit these or add your own
    test_questions = [
        "What do I do if CPU usage is high?",
        "Why was an instance terminated?",
        "How do I fix low disk space?",
        "What happened with the security group?",
    ]

    for question in test_questions:
        results = retrieve_chunks(vector_store, question)
        print_results(question, results)

    print("\n" + "=" * 60)
    print("Try your own question below (type 'exit' to quit)")
    print("=" * 60)
    while True:
        question = input("\nYour question: ").strip()
        if question.lower() == "exit":
            break
        if not question:
            continue
        results = retrieve_chunks(vector_store, question)
        print_results(question, results)


if __name__ == "__main__":
    main()