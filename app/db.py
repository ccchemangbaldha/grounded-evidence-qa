import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_ENV_PATH = os.getenv("DB_PATH")
DB_PATH = Path(DB_ENV_PATH)

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)