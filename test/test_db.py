from app.database import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {tables}")
    
    conn.close()
except Exception as e:
    print(f"Error connecting to database: {e}")