import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_PATH = Path(os.getenv("DB_PATH"))
SIMILARITY_THRESHOLD = 0.45
TOP_K = 5
