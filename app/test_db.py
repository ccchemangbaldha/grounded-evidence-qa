from app.db import get_connection

def main():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO documents (name) VALUES (?)",
        ("sample.txt",)
    )

    conn.commit()
    conn.close()
    print("Document inserted successfully")

if __name__ == "__main__":
    main()
