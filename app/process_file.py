import re
import numpy as np
from sentence_transformers import SentenceTransformer
from app.embeddings.similarity import cosine_similarity
from app.db_operation import save_document_with_chunks

#modal loading
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def split_into_sentences(text: str):
    return re.split(r'(?<=[.!?])\s+', text.strip())

def semantic_chunk_sentences(sentences, threshold=0.70):
    embeddings = embedding_model.encode(sentences)

    chunks = []
    current_chunk = [sentences[0]]
    current_embedding = embeddings[0]

    for i in range(1, len(sentences)):
        similarity = cosine_similarity(
            current_embedding,
            embeddings[i]
        )

        if similarity < threshold:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentences[i]]
            current_embedding = embeddings[i]
        else:
            current_chunk.append(sentences[i])
            # update centroid embedding
            current_embedding = np.mean(
                [current_embedding, embeddings[i]],
                axis=0
            )

    chunks.append(" ".join(current_chunk))
    return chunks


def process_content_string(filename: str, content: str):
    try:
        sentences = split_into_sentences(content)

        if not sentences:
            raise ValueError("Empty document")

        chunks = semantic_chunk_sentences(sentences)

        records = []
        for idx, chunk_text in enumerate(chunks):
            embedding = embedding_model.encode(chunk_text)

            records.append({
                "document": filename,
                "chunk_id": idx,
                "chunk_text": chunk_text,
                "embedding": embedding.tolist()
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

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "data": None
        }
