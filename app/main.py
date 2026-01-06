from fastapi import FastAPI, HTTPException, UploadFile, File
from app.db import get_connection
from app.process_file import process_content_string

app = FastAPI()

@app.get("/")
def read_root():
    return {"success":True,"message": "Welcome to the world OF AI"}

@app.get("/health")
def health():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()
        return {"success": True, "message": "database is connected and healthy."}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

@app.post("/ingest")
async def ingest_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        raise HTTPException(status_code=400, detail="Only .txt files are allowed")
    content_bytes = await file.read()
    content_string = content_bytes.decode("utf-8")
    result = process_content_string(file.filename, content_string)

    if result["success"] == False:
        raise HTTPException(status_code=500, detail=result["message"])

    return result