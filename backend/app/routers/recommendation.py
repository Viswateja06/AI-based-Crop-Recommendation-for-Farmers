from fastapi import APIRouter, HTTPException
import joblib
import pandas as pd
import os
from app.schemas import SoilData, RecommendationResponse

router = APIRouter()

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../ml_models/crop_rf_model.pkl')

def get_fertilizer_suggestion(crop: str) -> str:
    """Mock fertilizer lookup."""
    fertilizers = {
        "rice": "Urea and DAP",
        "wheat": "NPK 12:32:16",
        "apple": "Ammonium Sulphate",
        "grapes": "Potassium Nitrate"
    }
    return fertilizers.get(crop.lower(), "Standard NPK mix based on soil test.")

@router.post("/", response_model=RecommendationResponse)
async def recommend_crop(data: SoilData):
    """
    Accepts soil and environment data, returning a crop recommendation.
    """
    if not os.path.exists(MODEL_PATH):
        raise HTTPException(status_code=500, detail="ML Model not found. Did you run the training script?")
    
    model = joblib.load(MODEL_PATH)
    
    # Needs to match the feature list: ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    input_data = pd.DataFrame([{
        'N': data.N,
        'P': data.P,
        'K': data.K,
        'temperature': data.temperature,
        'humidity': data.humidity,
        'ph': data.ph,
        'rainfall': data.rainfall
    }])

    prediction = model.predict(input_data)[0]
    fertilizer = get_fertilizer_suggestion(prediction)

    return {
        "recommended_crop": prediction.capitalize(),
        "fertilizer_suggestion": fertilizer
    }
