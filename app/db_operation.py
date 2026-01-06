import sqlite3
from app.db import get_connection
import json 

def save_document_with_chunks(filename: str, chunk_records: list):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO documents (name) VALUES (?)",
            (filename,)
        )
        document_id = cursor.lastrowid

        for record in chunk_records:
            cursor.execute(
                "INSERT INTO chunks (document_id, chunk_index, text, embedding) VALUES (?, ?, ?, ?)",
                (
                    document_id,
                    record["chunk_id"],
                    record["chunk_text"],
                    sqlite3.Binary(json.dumps(record["embedding"]).encode("utf-8"))
                )
            )

        conn.commit()
        return document_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()
