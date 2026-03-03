from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI App
app = FastAPI(
    title="AI-Based Farmer Query Support and Advisory System",
    description="Backend API for Agricultural Advisory Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from .routers import chatbot, disease, weather, recommendation

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Based Farmer Query Support and Advisory System API"}

app.include_router(chatbot.router, prefix="/api/chat", tags=["chatbot"])
app.include_router(disease.router, prefix="/api/disease", tags=["disease"])
app.include_router(weather.router, prefix="/api/weather", tags=["weather"])
app.include_router(recommendation.router, prefix="/api/recommend", tags=["recommendation"])

