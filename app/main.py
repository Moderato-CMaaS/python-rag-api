from fastapi import FastAPI
from .api import api_router

app = FastAPI(
    title="Content Moderation API",
    description="An API for moderating text using custom rules.",
    version="1.0.0",
)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"status": "API is running"}

# To run: uvicorn app.main:app --reload