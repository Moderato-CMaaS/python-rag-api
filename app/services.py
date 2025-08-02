
import chromadb
import requests
import json
import re
from .core.config import GEMINI_API_KEY


chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="moderation_rules")

def add_new_rule(rule_id: str, rule_text: str, user_id: str):
    """Add a new moderation rule to ChromaDB"""
    try:
        collection.add(
            documents=[rule_text],
            metadatas=[{"user_id": user_id}],
            ids=[rule_id]
        )
        return {"success": True, "message": "Rule added successfully"}
    except Exception as e:
        return {"success": False, "message": f"Failed to add rule: {str(e)}"}

def extract_json(text):
    """Helper to extract JSON from text"""
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        return match.group(0)
    return text

def check_moderation(text: str, user_id: str):
    """Check if text violates user's moderation rules using Gemini API"""
    try:
        # Query ChromaDB for relevant rules
        results = collection.query(
            query_texts=[text],
            n_results=1,
            where={"user_id": user_id}
        )
        
        if not results['documents'] or not results['documents'][0]:
            return {
                "is_violation": False,
                "reason": "No moderation rules found for this user"
            }
        
        retrieved_rule = results['documents'][0][0]
        
        # Prepare prompt for Gemini
        prompt = f"""
You are a content moderation AI. Your task is to determine if a piece of text violates a specific user-defined rule.
You must respond ONLY with a valid JSON object with two keys: "is_violation" (boolean) and "reason" (a brief string explanation).

Rule: "{retrieved_rule}"
Text to Moderate: "{text}"

JSON Response:
"""
        
        # Call Gemini API
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
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
        
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        gemini_response = resp.json()
        result_json = gemini_response["candidates"][0]["content"]["parts"][0]["text"]
        
        # Parse JSON response
        json_str = extract_json(result_json)
        final_result = json.loads(json_str)
        
        return {
            "is_violation": final_result.get("is_violation", False),
            "reason": final_result.get("reason", "No reason provided")
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "is_violation": None,
            "reason": f"Gemini API call failed: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "is_violation": None,
            "reason": f"Failed to parse Gemini response as JSON: {str(e)}"
        }
    except Exception as e:
        return {
            "is_violation": None,
            "reason": f"Moderation check failed: {str(e)}"
        }