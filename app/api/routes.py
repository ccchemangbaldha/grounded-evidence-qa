from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.db.retrieval import get_relevant_chunks
from app.injest.processor import process_content_string
from app.llm.gemini import get_gemini_model
from app.core.config import TOP_K, SIMILARITY_THRESHOLD

router = APIRouter()

class AskRequest(BaseModel):
    documentId: int
    question: str

@router.get("/")
async def hello():
    return {"success":True, "message":"Hello Wolrd!"}

@router.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(400, "Only .txt files allowed")

    content = (await file.read()).decode("utf-8")
    return process_content_string(file.filename, content)

@router.post("/ask")
def ask(payload: AskRequest):
    chunks = get_relevant_chunks(
        payload.documentId,
        payload.question,
        TOP_K,
        SIMILARITY_THRESHOLD
    )

    if not chunks:
        return {
            "question": payload.question,
            "answer": "I don’t know based on the provided context.",
            "confidence": 0.0,
            "evidence": []
        }

    context = "\n".join(c["text"] for c in chunks)

    prompt = f"""
Answer ONLY from the chunks below.
If insufficient, say: "I don’t know based on the provided context."

Chunks:
{context}

Question:
{payload.question}
"""

    model = get_gemini_model()
    response = model.generate_content(prompt)

    raw_conf = max(c["similarity"] for c in chunks)
    confidence = max(0.0, min(1.0, (raw_conf + 1) / 2))

    return {
        "question": payload.question,
        "answer": response.text,
        "confidence": confidence,
        "evidence": chunks
    }
