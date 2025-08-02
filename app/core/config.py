import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DOT_NET_API_KEY = os.getenv("DOT_NET_API_KEY")