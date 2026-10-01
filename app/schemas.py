from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class HomePlannerRequest(BaseModel):
    budget: float = Field(gt=0)
    location: str = "India"
    home_type: str = "Apartment"
    rooms: int = Field(default=2, ge=1, le=10)
    style: str = "Modern"
    priorities: List[str] = []


class PartyPlannerRequest(BaseModel):
    budget: float = Field(gt=0)
    location: str = "India"
    occasion: str = "Birthday"
    guests: int = Field(default=10, ge=1, le=1000)
    food_preference: str = "Mixed"
    venue_preference: str = "Home"
    theme: str = "Simple"


class JewelryPlannerRequest(BaseModel):
    budget: float = Field(gt=0)
    occasion: str = "Casual"
    jewelry_type: str = "Necklace"
    metal: str = "Any"
    style: str = "Minimal"
    outfit_color: str = "Any"


class RecommendationItem(BaseModel):
    name: str
    category: str
    price: float
    reason: str
    platform: Optional[str] = None
    url: Optional[str] = None


class RecommendationResponse(BaseModel):
    recommendation_id: Optional[int] = None
    planner_type: str
    title: str
    summary: str
    estimated_total: float
    items: List[RecommendationItem]
    tips: List[str] = []
    source: str = "mock"


class SessionInfo(BaseModel):
    authenticated: bool
    user: Optional[Dict[str, Any]] = None