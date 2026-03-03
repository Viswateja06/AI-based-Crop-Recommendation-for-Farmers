from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    query: str
    lang: str = "en"
    user_id: Optional[int] = None

class ChatResponse(BaseModel):
    intent: str
    query: str
    response: str

class SoilData(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

class RecommendationResponse(BaseModel):
    recommended_crop: str
    fertilizer_suggestion: str

class WeatherRequest(BaseModel):
    city: str
    state: Optional[str] = None
