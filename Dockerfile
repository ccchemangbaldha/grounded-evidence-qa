FROM python:3.11-slim

WORKDIR /app

# Install system deps (optional for sentence-transformers)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy everything
COPY . /app

# Install python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for huggingface
EXPOSE 7860

# Run uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
