import json
import numpy as np
from app.db.connection import get_connection
from app.embeddings.hf import get_embedding
from app.embeddings.similarity import cosine_similarity

def get_relevant_chunks(
    document_id: int,
    question: str,
    top_k: int,
    min_similarity: float
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM documents WHERE rowid = ?",
        (document_id,)
    )
    doc = cursor.fetchone()
    if not doc:
        conn.close()
        return []

    document_name = doc[0]

    cursor.execute(
        """
        SELECT rowid, chunk_index, text, embedding
        FROM chunks
        WHERE document_id = ?
        """,
        (document_id,)
    )
    rows = cursor.fetchall()
    conn.close()

    query_embedding = get_embedding(question)

    scored = []
    for rowid, idx, text, blob in rows:
        embedding = np.array(
            json.loads(blob.decode("utf-8")),
            dtype=float
        )
        sim = cosine_similarity(query_embedding, embedding)

        if sim >= min_similarity:
            scored.append({
                "chunk_id": rowid,
                "text": text,
                "similarity": sim,
                "document": document_name
            })

    scored.sort(key=lambda x: x["similarity"], reverse=True)
    return scored[:top_k]
