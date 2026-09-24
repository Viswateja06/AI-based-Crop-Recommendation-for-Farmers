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


def get_fertilizer_suggestion(crop: str) -> str:
    # your existing code
    ...


@router.post("/", response_model=RecommendationResponse)
async def recommend_crop(data: SoilData):

    if not os.path.exists(MODEL_PATH):
        raise HTTPException(
            status_code=500,
            detail="ML Model not found."
        )

    # 👇 CHANGE THIS PART
    try:
        print(f"Loading model from: {MODEL_PATH}")
        print(f"Model exists: {os.path.exists(MODEL_PATH)}")

        model = joblib.load(MODEL_PATH)

        print("Crop recommendation model loaded successfully.")

    except Exception as e:
        print(f"MODEL LOAD ERROR: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load crop recommendation model: {str(e)}"
        )

    # keep everything below unchanged
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
