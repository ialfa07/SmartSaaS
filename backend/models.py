from pydantic import BaseModel
from typing import Optional

class PromptRequest(BaseModel):
    prompt: str

class User(BaseModel):
    email: str

class PaymentRequest(BaseModel):
    plan_id: str

class ImageRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"
    quality: str = "standard"

class MarketingRequest(BaseModel):
    business_type: str
    target_audience: str
    platform: str

class CalendarRequest(BaseModel):
    business_type: str
    duration_days: int = 30

class TokenReward(BaseModel):
    action: str
    tokens: int

class ReferralRequest(BaseModel):
    referred_email: str

class TokenTransfer(BaseModel):
    to_email: str
    amount: int
