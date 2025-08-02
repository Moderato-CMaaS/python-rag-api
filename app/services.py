
import chromadb
import openai
from .core.config import OPENAI_API_KEY


openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="moderation_rules")

def add_new_rule(rule_id: str, rule_text: str, user_id: str):
    # ... logic to add rule to collection ...
    pass

def check_moderation(text: str, user_id: str):
    # ... logic to query ChromaDB and call OpenAI ...
    pass