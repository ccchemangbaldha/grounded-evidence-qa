import sqlite3
from pathlib import Path

DB_PATH = Path("data/geqa.db")

def get_connection():
    return sqlite3.connect(DB_PATH)
