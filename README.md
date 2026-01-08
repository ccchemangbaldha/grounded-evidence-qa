---
license: mit
title: rag-app
sdk: docker
emoji: 🚀
colorFrom: green
colorTo: green
pinned: false
---
# **Grounded Evidence QA**

**Grounded Evidence QA** is a simple question-answering system that answers questions **only from uploaded documents**, always showing **evidence and confidence**.
If the answer is not supported by the document, the system clearly says **“I don’t know based on the provided context.”**

This project focuses on **truthfulness, explainability, and hallucination prevention**, not just generating fluent answers.

---

## 📌 What does *“Grounded Evidence QA”* mean?

* **Grounded** → Every answer must be supported by document content
* **Evidence** → The exact text chunks used for answering are returned
* **QA (Question Answering)** → Users can ask natural language questions

In short:

> *No guessing. No hallucination. Only evidence-backed answers.*

---

##  API Overview

The system exposes **three REST APIs** using **FastAPI**:

### **1. Health Check**

```
GET /health
```

Checks whether the service and database are working correctly.

---

### **2. Document Ingestion**

```
POST /ingest
```

* Accepts plain text files (`.txt`)
* Splits the document into semantic chunks
* Generates embeddings for each chunk
* Stores document, chunks, and embeddings in SQLite

---

### **3. Ask a Question**

```
POST /ask
```

Request body:

```json
{
  "documentId": 1,
  "question": "Your question here"
}
```

Response includes:

* Answer
* Confidence score
* Evidence (document name, chunk text, similarity)
---

## Run The Application
```
# Make virtual environment
python -m venv venv

# Activate it
source venv/Scripts/activate

# Install required packages
pip install -r requirements.txt

# Start the python app
uvicorn app.main:app --reload
```

---
## Chunking Strategy

The document is split using a **semantic sentence-based chunking strategy**:

* The text is first split into sentences
* Each sentence is embedded
* Consecutive sentences are grouped together **only if they are semantically similar**
* Cosine similarity is used to decide whether to merge or split chunks
---

## Embedding Choice

We use the Hugging Face model:

**`sentence-transformers/all-MiniLM-L6-v2`**

### Reasons for this choice:

* Free and lightweight
* Produces high-quality sentence embeddings
* Widely used and well-tested
* Fast enough for local execution
---

## Confidence Logic

Confidence is **computed**, not hardcoded.

### How confidence is calculated:

1. Retrieve the top-K most relevant chunks
2. Take the **highest cosine similarity score**
3. Normalize it from `[-1, 1]` to `[0, 1]`

### What confidence represents:

> *How strong the best supporting evidence is for the answer.*

---

## Hallucination Prevention

Hallucinations are prevented using **two layers**:

### **1. Retrieval Threshold**

* If no chunk crosses the similarity threshold, the LLM is **not called**

### **2. Evidence-Only Prompting**

The LLM is explicitly instructed:

> *“Answer using ONLY the provided chunks. else say I don’t know based on the provided context.”*

This ensures the system **refuses to guess**.

---

## Limitations

This project is intentionally simple and has known limitations:

* Works only with `.txt` files
* Uses SQLite (not designed for very large datasets)
* Confidence is based on similarity, not factual verification
* Designed for single-document querying per request

---

## Final Note

This is not a chatbot.
This is a **grounded evidence-based question answering system**.

If the document does not support the answer, the system will **honestly say so** - and that is the point.