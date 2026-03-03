from fastapi import APIRouter, File, UploadFile
from typing import Dict
from ml_models.disease_detection import predict_disease

router = APIRouter()

@router.post("/detect")
async def detect_disease(file: UploadFile = File(...)) -> Dict:
    """
    Accepts an uploaded crop image, runs the leaf-check heuristic, and returns a disease prediction.
    """
    # Read the file contents into memory
    file_bytes = await file.read()
    
    # Pass the bytes to the mock model
    result = predict_disease(file_bytes)
    return {
        "filename": file.filename,
        "disease": result["name"],
        "treatment": result["treatment"],
        "pesticide": result["pesticide"]
    }
