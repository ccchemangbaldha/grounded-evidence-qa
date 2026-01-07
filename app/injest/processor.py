import re
import numpy as np
from sentence_transformers import SentenceTransformer
from app.embeddings.similarity import cosine_similarity
from app.db.operations import save_document_with_chunks

_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def _split_sentences(text: str):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def _semantic_chunk(sentences, threshold=0.70):
    embeddings = _model.encode(sentences)

    chunks = []
    current = [sentences[0]]
    centroid = embeddings[0]

    for i in range(1, len(sentences)):
        sim = cosine_similarity(centroid, embeddings[i])
        if sim < threshold:
            chunks.append(" ".join(current))
            current = [sentences[i]]
            centroid = embeddings[i]
        else:
            current.append(sentences[i])
            centroid = np.mean([centroid, embeddings[i]], axis=0)

    chunks.append(" ".join(current))
    return chunks

def process_content_string(filename: str, content: str):
    sentences = _split_sentences(content)
    if not sentences:
        raise ValueError("Empty document")

    chunks = _semantic_chunk(sentences)

    records = []
    for idx, text in enumerate(chunks):
        embedding = _model.encode(text).tolist()
        records.append({
            "chunk_id": idx,
            "chunk_text": text,
            "embedding": embedding
        })

    document_id = save_document_with_chunks(filename, records)

    return {
        "success": True,
        "data": {
            "document_id": document_id,
            "chunks_saved": len(records)
        },
        "message": "File processed successfully"
    }
