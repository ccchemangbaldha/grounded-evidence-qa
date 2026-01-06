def process_content_string(filename: str, content: str):
    print(f"\n--- FILE CONTENT START: {filename} ---")
    print(content)
    print(f"--- FILE CONTENT END: {filename} ---\n")

    try:
        return {
            "success": True,
            "data": filename,
            "message": "file processing done."
        }
    except Exception as e:
        return {"success": False, "message": str(e), "data": None}