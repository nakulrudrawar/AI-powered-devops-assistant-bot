# DevOps Assistant Bot

A chatbot that answers questions about AWS infrastructure, runbooks, and CloudWatch-style logs using RAG (Retrieval-Augmented Generation) and an LLM. Built as a hands-on project combining AI/LLM skills with DevOps practices.

## What it does

Ask a question like *"Why is CPU utilization high?"* or *"How do I fix low disk space?"* and the bot:
1. Searches a local knowledge base of runbooks and logs for relevant information
2. Sends that information + your question to an LLM
3. Returns a grounded answer, along with the source documents used

If the answer isn't in the knowledge base, the bot says so honestly instead of making something up.

## Tech Stack

| Layer | Tool |
|---|---|
| LLM | Dots3-Note Preview (via OpenRouter, free tier) |
| RAG / Retrieval | LangChain + ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2, runs locally, free) |
| UI | Streamlit |
| Containerization | Docker *(coming in Week 2)* |
| CI/CD | GitHub Actions *(coming in Week 2)* |
| Cloud | AWS EC2 *(coming in Week 2)* |
| Monitoring | CloudWatch *(coming in Week 2)* |

## Project Structure

```
├── data/                      # Runbooks and sample logs (knowledge base source)
├── chroma_db/                 # Generated vector database (not committed to git)
├── ingest.py                  # Loads data, chunks it, creates embeddings, saves to ChromaDB
├── retrieve.py                # Searches ChromaDB for relevant chunks given a question
├── generate.py                # Sends question + retrieved chunks to the LLM via OpenRouter
├── app.py                     # Streamlit chat interface
└── requirements.txt
```

## Setup

1. Clone the repo:
   ```
   git clone <your-repo-url>
   cd AI-powered-devops-assistant-bot
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # Mac/Linux
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   OPENROUTER_API_KEY=your_key_here
   ```
   Get a free key at [openrouter.ai](https://openrouter.ai).

5. Build the vector database (run once, and again anytime you change files in `/data`):
   ```
   python ingest.py
   ```

6. Run the app:
   ```
   streamlit run app.py
   ```

## Testing retrieval or the LLM separately

- Test retrieval only: `python retrieve.py`
- Test the full pipeline in the terminal (no UI): `python generate.py`

## Known Limitations

- Answers are not perfectly deterministic — asking the same question twice may return slightly different wording, since LLMs generate text probabilistically by default.
- Retrieval quality depends on the size and specificity of the knowledge base — very short or vague questions (e.g. a single word) sometimes retrieve a plausible-but-not-ideal match rather than asking for clarification.
- Uses a free-tier "preview" model on OpenRouter, which may be rate-limited, slower, or replaced by the provider without much notice. The model name in `generate.py` can be swapped for any other OpenRouter-supported model with a one-line change.

## Roadmap

- [x] Build RAG pipeline (ingest, retrieve, generate)
- [x] Build Streamlit UI
- [x] Test and add error handling
- [ ] Dockerize the app
- [ ] Set up CI/CD with GitHub Actions
- [ ] Deploy to AWS EC2
- [ ] Add CloudWatch monitoring