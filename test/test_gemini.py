from app.llm.gemini import get_gemini_model

try:
    model = get_gemini_model()
    prompt = (
        "Hello GEMiNI!"
    )
    response = model.generate_content(
        prompt,
        request_options={"timeout": 60}
    )
    if not response or not response.text:
        raise RuntimeError("No response from Gemini")
    print("Response:")
    print(response.text)
except Exception as e:
    print("Error:", str(e))