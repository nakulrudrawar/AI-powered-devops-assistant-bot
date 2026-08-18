"""
generate.py
Step 3 of the RAG pipeline for DevOps Assistant Bot.

What this script does:
1. Takes a question
2. Retrieves relevant chunks from ChromaDB (using retrieve.py)
3. Sends the question + chunks to an LLM via OpenRouter
4. Prints a clear, generated answer

Before running, create a .env file in this folder with:
    OPENROUTER_API_KEY=your_key_here

Run this to test end-to-end:
    python generate.py
"""

import os
import requests
from dotenv import load_dotenv
from retrieve import load_vector_store, retrieve_chunks

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "dots-studio/dots-3-note-preview:free"


def build_prompt(question, chunks):
    """Combine the retrieved chunks and the question into one prompt for the LLM."""
    context_text = "\n\n---\n\n".join(
        f"Source: {doc.metadata.get('source', 'unknown')}\n{doc.page_content.strip()}"
        for doc in chunks
    )

    prompt = f"""You are a helpful DevOps assistant. Answer the question using ONLY the context below.
If the context does not contain enough information, say so honestly instead of guessing.

Context:
{context_text}

Question: {question}

Answer clearly and concisely, in a few sentences or a short numbered list if steps are involved."""
    return prompt


def ask_llm(prompt):
    """Send the prompt to the OpenRouter model and return the answer."""
    if not OPENROUTER_API_KEY:
        return "Error: OPENROUTER_API_KEY not found. Check your .env file."

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
    except requests.exceptions.Timeout:
        return "Sorry, the request timed out. OpenRouter may be slow right now — please try again."
    except requests.exceptions.ConnectionError:
        return "Sorry, could not connect to OpenRouter. Check your internet connection and try again."
    except requests.exceptions.RequestException as e:
        return f"Sorry, something went wrong while contacting the LLM: {e}"

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    try:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError, ValueError):
        return "Sorry, received an unexpected response from the LLM. Please try again."


def answer_question(vector_store, question):
    """Full pipeline: retrieve chunks, build prompt, get LLM answer."""
    chunks = retrieve_chunks(vector_store, question)
    if not chunks:
        return "No relevant information found in the knowledge base."

    prompt = build_prompt(question, chunks)
    answer = ask_llm(prompt)
    return answer


def main():
    vector_store = load_vector_store()

    print("DevOps Assistant Bot (type 'exit' to quit)\n")
    while True:
        question = input("Your question: ").strip()
        if question.lower() == "exit":
            break
        if not question:
            continue

        answer = answer_question(vector_store, question)
        print("\n--- Answer ---")
        print(answer)
        print()


if __name__ == "__main__":
    main()