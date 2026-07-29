from config.llm import client

models_to_try = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3-flash-preview",
    "gemini-2.0-flash",
    "gemini-flash-latest",
]

for model in models_to_try:
    print(f"\nTesting: {model}")
    try:
        response = client.models.generate_content(
            model=model,
            contents="Reply with only the word: SUCCESS"
        )
        print("✅ WORKS")
        print(response.text)
        break

    except Exception as e:
        print("❌ FAILED")
        print(type(e).__name__)
        print(e)