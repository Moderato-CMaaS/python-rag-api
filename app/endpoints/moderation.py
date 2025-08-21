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

@router.delete("/delete-rule/{rule_id}/")
def delete_rule(rule_id: str, user_id: str):
    """Delete a specific moderation rule"""
    result = services.delete_rule(rule_id, user_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": result["message"]}

@router.get("/rules/{user_id}/")
def get_user_rules(user_id: str):
    """Get all moderation rules for a user"""
    result = services.get_user_rules(user_id)
    if not result["success"]:
        raise HTTPException(status_code=500, detail=result["message"])
    return {"rules": result["rules"], "message": result["message"]}

@router.put("/update-rule/{rule_id}/")
def update_rule(rule_id: str, updated_rule: schemas.UpdateRule):
    """Update an existing moderation rule"""
    result = services.update_rule(rule_id, updated_rule.rule_text, updated_rule.user_id)
    if not result["success"]:
        raise HTTPException(status_code=404, detail=result["message"])
    return {"message": result["message"]}

@router.post("/moderate/", response_model=schemas.ModerationResponse)
def moderate(request: schemas.ModerationRequest):
    """Moderate text against user's rules using Gemini AI"""
    result = services.check_moderation(request.text_to_moderate, request.user_id)
    if result["is_violation"] is None:
        raise HTTPException(status_code=500, detail=result["reason"])
    return schemas.ModerationResponse(
        is_violation=result["is_violation"],
        reason=result["reason"]
    )