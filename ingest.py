"""
ingest.py
Step 1 of the RAG pipeline for DevOps Assistant Bot.

What this script does:
1. Loads all .txt and .md files from the /data folder
2. Splits them into small chunks
3. Converts each chunk into an embedding (using a free local model)
4. Saves everything into a local ChromaDB vector database

Run this once whenever you add or change files in /data:
    python ingest.py
"""

import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ---- Settings ----
DATA_FOLDER = "./data"
CHROMA_FOLDER = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # small, free, runs locally


def load_documents():
    """Load every .txt and .md file from the data folder."""
    print(f"Loading documents from {DATA_FOLDER} ...")

    txt_loader = DirectoryLoader(
        DATA_FOLDER, glob="**/*.txt", loader_cls=TextLoader
    )
    md_loader = DirectoryLoader(
        DATA_FOLDER, glob="**/*.md", loader_cls=TextLoader
    )

    documents = txt_loader.load() + md_loader.load()
    print(f"Loaded {len(documents)} document(s).")
    return documents


def split_documents(documents):
    """Break documents into small overlapping chunks."""
    print("Splitting documents into chunks ...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunk(s).")
    return chunks


def build_vector_store(chunks):
    """Embed the chunks and save them into ChromaDB."""
    print("Loading embedding model (first run may take a minute to download) ...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    print("Creating embeddings and saving to ChromaDB ...")
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_FOLDER,
    )

    print(f"Done. Vector database saved to {CHROMA_FOLDER}")
    return vector_store


def main():
    if not os.path.exists(DATA_FOLDER):
        print(f"Error: {DATA_FOLDER} folder not found. Create it and add your files first.")
        return

    documents = load_documents()
    if not documents:
        print("No documents found in /data. Add some .txt or .md files first.")
        return

    chunks = split_documents(documents)
    build_vector_store(chunks)


if __name__ == "__main__":
    main()