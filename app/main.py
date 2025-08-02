
from fastapi import FastAPI, Request, HTTPException
from .api import api_router
from .core.config import DOT_NET_API_KEY


app = FastAPI(
    title="Content Moderation API",
    description="An API for moderating text using custom rules.",
    version="1.0.0",
)

# --- API Key Security Middleware ---

@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.url.path == "/": 
        return await call_next(request)
    if request.headers.get("X-API-Key") != DOT_NET_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid or missing API key.")
    return await call_next(request)


app.include_router(api_router)


@app.get("/")
def read_root():
    return {"status": "API is running"}

# To run: uvicorn app.main:app --reload