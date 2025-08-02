import os
import requests
from dotenv import load_dotenv

def test_gemini_api():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key
    }
    data = {
        "contents": [
            {
                "parts": [
                    {"text": "Explain how AI works in a few words"}
                ]
            }
        ]
    }
    try:
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        print("✅ Gemini API is working. Response:")
        print(resp.json())
    except Exception as e:
        print("❌ Gemini API test failed.")
        print(e)

if __name__ == "__main__":
    test_gemini_api()