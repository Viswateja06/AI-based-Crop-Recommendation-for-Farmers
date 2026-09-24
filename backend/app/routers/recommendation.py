import os
import joblib
import pandas as pd

from fastapi import APIRouter, HTTPException
from app.schemas import SoilData, RecommendationResponse

router = APIRouter()

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    '../../ml_models/crop_rf_model.pkl'
)

# Load model once when the application starts
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"ML model not found at: {MODEL_PATH}"
    )

model = joblib.load(MODEL_PATH)


def get_fertilizer_suggestion(crop: str) -> str:
    """Return fertilizer suggestion based on recommended crop."""

    fertilizers = {
        "rice": "Urea and DAP",
        "wheat": "NPK 12:32:16",
        "apple": "Ammonium Sulphate",
        "grapes": "Potassium Nitrate"
    }

    return fertilizers.get(
        crop.lower(),
        "Standard NPK mix based on soil test."
    )


@router.post("/", response_model=RecommendationResponse)
async def recommend_crop(data: SoilData):
    """
    Accepts soil and environmental data,
    returning a crop recommendation.
    """

    input_data = pd.DataFrame([{
        "N": data.N,
        "P": data.P,
        "K": data.K,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "ph": data.ph,
        "rainfall": data.rainfall
    }])

    prediction = model.predict(input_data)[0]

    fertilizer = get_fertilizer_suggestion(prediction)

    return {
        "recommended_crop": str(prediction).capitalize(),
        "fertilizer_suggestion": fertilizer
    }
