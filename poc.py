import os
import json
import chromadb
import requests
from dotenv import load_dotenv


load_dotenv()

# local chroma
chroma_client = chromadb.Client()

# A "collection" in ChromaDB is like a table in a SQL database.
collection = chroma_client.get_or_create_collection(name="moderation_rules")

USER_RULE = "No political discussions or mentions of specific political figures."
USER_ID = "user_123" #for testing


collection.add(
    documents=[USER_RULE],
    metadatas=[{"user_id": USER_ID}],
    ids=["rule_001_for_user_123"]
)

print(f" Rule for '{USER_ID}' has been added to the database.")


TEXT_TO_MODERATE = "We really need to discuss the prime minister's latest policy."

results = collection.query(
    query_texts=[TEXT_TO_MODERATE],
    n_results=1, #return one most relevant rule
    where={"user_id": USER_ID}
)

retrieved_rule = results['documents'][0][0]


prompt = f"""
You are a content moderation AI. Your task is to determine if a piece of text violates a specific user-defined rule.
You must respond ONLY with a valid JSON object with two keys: "is_violation" (boolean) and "reason" (a brief string explanation).

Rule: "{retrieved_rule}"
Text to Moderate: "{TEXT_TO_MODERATE}"

JSON Response:
"""

# Call the Gemini API
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
                {"text": prompt}
            ]
        }
    ]
}
try:
    resp = requests.post(url, headers=headers, json=data)
    resp.raise_for_status()
    gemini_response = resp.json()
    result_json = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
except Exception as e:
    print("❌ Gemini API call failed.")
    print(e)
    result_json = '{"is_violation": null, "reason": "Gemini API call failed."}'




# Helper to extract JSON from text
import re
def extract_json(text):
    # Try to find the first {...} JSON object in the text
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        return match.group(0)
    return text  # fallback: return as-is

# Convert the JSON string into a Python dictionary
try:
    json_str = extract_json(result_json)
    final_result = json.loads(json_str)
except Exception as e:
    print("Failed to parse Gemini response as JSON.")
    print(e)
    final_result = {"is_violation": None, "reason": "Failed to parse Gemini response as JSON."}

print("\n--- MODERATION RESULT ---")
print(f"Violation Detected: {final_result.get('is_violation')}")
print(f"Reason: {final_result.get('reason')}")
print("-------------------------\n")