from fastapi import APIRouter
from .endpoints import moderation

api_router = APIRouter()
api_router.include_router(moderation.router, tags=["moderation"])