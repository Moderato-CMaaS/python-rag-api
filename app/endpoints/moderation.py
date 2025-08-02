from fastapi import APIRouter, HTTPException
from .. import schemas, services

router = APIRouter()

@router.post("/add-rule/", status_code=201)
def add_rule(rule: schemas.Rule):
    # ... call services.add_new_rule(...) ...
    return {"message": "Rule added successfully"}

@router.post("/moderate/", response_model=schemas.ModerationResponse)
def moderate(request: schemas.ModerationRequest):
    # ... call services.check_moderation(...) ...
    result = services.check_moderation(request.text_to_moderate, request.user_id)
    return result