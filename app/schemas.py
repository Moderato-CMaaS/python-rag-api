from pydantic import BaseModel

class Rule(BaseModel):
    user_id: str
    rule_text: str
    rule_id: str

class ModerationRequest(BaseModel):
    user_id: str
    text_to_moderate: str

