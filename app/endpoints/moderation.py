from fastapi import APIRouter, HTTPException
from .. import schemas, services

router = APIRouter()

@router.post("/add-rule/", status_code=201)
def add_rule(rule: schemas.Rule):
    """Add a new moderation rule"""
    result = services.add_new_rule(rule.rule_id, rule.rule_text, rule.user_id)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    return {"message": result["message"]}

@router.post("/moderate/", response_model=schemas.ModerationResponse)
def moderate(request: schemas.ModerationRequest):
    """Moderate text against user's rules using Gemini API"""
    result = services.check_moderation(request.text_to_moderate, request.user_id)
    if result["is_violation"] is None:
        raise HTTPException(status_code=500, detail=result["reason"])
    return schemas.ModerationResponse(
        is_violation=result["is_violation"],
        reason=result["reason"]
    )