# RAG Moderation API

A FastAPI-based content moderation system that uses ChromaDB for rule storage and Google's Gemini API for intelligent moderation decisions.

## Features

- Store custom moderation rules per user in ChromaDB //still local*
- Use RAG (Retrieval Augmented Generation) to find relevant rules
- Leverage Gemini AI for contextual moderation decisions
- REST API endpoints for adding rules and moderating content

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Gemini API key:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Start the API server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Add Rule
```
POST /add-rule/
```
Add a new moderation rule for a user.

**Body:**
```json
{
    "user_id": "user123",
    "rule_id": "rule001",
    "rule_text": "No political discussions or mentions of specific political figures."
}
```

### Moderate Content
```
POST /moderate/
```
Check if text violates user's moderation rules.

**Body:**
```json
{
    "user_id": "user123",
    "text_to_moderate": "We really need to discuss the prime minister's latest policy."
}
```

**Response:**
```json
{
    "is_violation": true,
    "reason": "The text mentions political figures which violates the rule."
}
```

## Testing

1. Test the Gemini API connection:
```bash
python test.py
```

2. Test the API endpoints:
```bash
python test_api.py
```

3. Run the POC script to see the complete workflow:
```bash
python poc.py
```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.
