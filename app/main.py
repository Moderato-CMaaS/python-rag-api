
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
    # Allow unauthenticated access to root and documentation endpoints
    open_paths = {"/", "/docs", "/redoc", "/openapi.json"}
    if request.url.path in open_paths:
        response = await call_next(request)
    else:
        if request.headers.get("X-API-Key") != DOT_NET_API_KEY:
            raise HTTPException(status_code=403, detail="Forbidden: Invalid or missing API key.")
        response = await call_next(request)
    
    # Add CORS headers
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

@app.options("/{path:path}")
async def options_handler(path: str):
    """Handle preflight OPTIONS requests"""
    from fastapi import Response
    response = Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response


app.include_router(api_router)


@app.get("/")
def read_root():
    return {"status": "API is running"}

# To run: uvicorn app.main:app --reload