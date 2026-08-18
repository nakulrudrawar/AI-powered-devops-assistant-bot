# Use a slim official Python image to keep the image size down
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy dependency file first (better caching - only reinstalls if requirements change)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Build the vector database at image build time, so the container
# starts ready-to-use without needing to run ingest.py manually.
RUN python ingest.py

# Streamlit's default port
EXPOSE 8501

# Run the app. --server.address=0.0.0.0 is required so it's reachable
# from outside the container.
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]