import requests
import json

# API base URL (adjust if needed)
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test the moderation API endpoints"""
    
    # Test data
    user_id = "test_user_123"
    rule_id = "rule_001_test"
    rule_text = "No political discussions or mentions of specific political figures."
    text_to_moderate = "We really need to discuss the prime minister's latest policy."
    
    print(" Testing RAG Moderation API with Gemini...")
    
    # Test 1: Add a rule
    print("\n1. Testing add rule endpoint...")
    add_rule_data = {
        "user_id": user_id,
        "rule_id": rule_id,
        "rule_text": rule_text
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/add-rule/",
            json=add_rule_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 201:
            print(" Rule added successfully")
            print(f"Response: {response.json()}")
        else:
            print(f" Failed to add rule. Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f" Error adding rule: {e}")
    
    # Test 2: Moderate text-----
    print("\n2. Testing moderation endpoint...")
    moderation_data = {
        "user_id": user_id,
        "text_to_moderate": text_to_moderate
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/moderate/",
            json=moderation_data,
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            result = response.json()
            print(" Moderation check completed")
            print(f"Is Violation: {result['is_violation']}")
            print(f"Reason: {result['reason']}")
        else:
            print(f" Moderation failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f" Error during moderation: {e}")

if __name__ == "__main__":
    print("Make sure your API is running with: uvicorn app.main:app --reload")
    print("Then run this test script.")
    input("Press Enter to continue...")
    test_api_endpoints()
