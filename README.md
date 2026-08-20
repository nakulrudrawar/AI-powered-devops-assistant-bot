# AI-Powered DevOps Assistant Bot

A Streamlit chatbot that answers DevOps questions using local document retrieval and an LLM. It searches runbooks and sample CloudWatch-style logs, then generates an answer grounded in the retrieved context.

## How it works

1. `ingest.py` loads `.txt` and `.md` files from `data/`.
2. Documents are split into chunks and embedded with `all-MiniLM-L6-v2`.
3. ChromaDB stores the embeddings in the local `chroma_db/` directory.
4. `retrieve.py` finds the three most relevant chunks for a question.
5. `generate.py` sends the question and context to OpenRouter.
6. `app.py` provides the Streamlit chat interface and displays source files.

## Requirements

- Python 3.11 or later
- An OpenRouter API key
- Internet access on the first run to download packages and the embedding model

## Local setup

Run these commands from the repository root.

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_key_here
```

Keep this key private and never commit `.env`.

Build the local vector database:

```bash
python ingest.py
```

Run the web application:

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Other commands

Test document retrieval:

```bash
python retrieve.py
```

Run the complete assistant in the terminal:

```bash
python generate.py
```

Both interactive scripts use `exit` to quit. Rerun `python ingest.py` after changing the knowledge-base files. The current ingestion script supports only `.txt` and `.md`; Terraform (`.tf`) and YAML (`.yml`) files in `data/` are not indexed.

## Docker

The image builds the vector database during `docker build`.

```bash
docker build -t devops-assistant-bot .
docker run --rm -p 8501:8501 -e OPENROUTER_API_KEY=your_key_here devops-assistant-bot
```

Open `http://localhost:8501`. Docker builds require network access because dependencies and the embedding model are installed or downloaded during the build.

## CI/CD

`.github/workflows/ci.yml` builds the Docker image for pull requests and pushes to `main`. On pushes to `main`, it publishes the `latest` image to Docker Hub.

Configure these repository secrets for publishing:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Project structure

```text
app.py                 Streamlit chat interface
ingest.py              Build the ChromaDB vector store
retrieve.py            Retrieve relevant document chunks
generate.py            Generate answers through OpenRouter
data/                  Runbooks and sample logs
chroma_db/             Generated local vector database
Dockerfile             Container image definition
requirements.txt       Python dependencies
```

## Limitations

- Dependencies are not pinned, so installs may not be fully reproducible.
- There are no automated tests or production authentication features.
- OpenRouter availability, rate limits, and model behavior can affect responses.
- The local embedding model requires disk space, memory, and a first-run download.
- Repeated ingestion may add duplicate entries to the existing ChromaDB because the script does not reset the database.

