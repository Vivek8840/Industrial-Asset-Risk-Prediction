
from fastapi import FastAPI

from app.schemas.prediction import (
    PredictionResponse,
    SensorReadings,
)
from app.services.model_service import model_service


app = FastAPI(
    title="P_227 Industrial Asset Risk API",
    description=(
        "Predictive maintenance prototype using "
        "an XGBoost model trained on the AI4I dataset."
    ),
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_service.model is not None,
    }


@app.get("/model-info")
def model_info():
    return {
        "project": model_service.metadata["project"],
        "algorithm": model_service.metadata["algorithm"],
        "features": model_service.features,
        "decision_threshold": model_service.threshold,
        "status": model_service.metadata.get("status"),
        "limitations": model_service.metadata.get(
            "limitations", []
        ),
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(readings: SensorReadings):
    model_input = readings.to_model_input()
    result = model_service.predict(model_input)
    return result
