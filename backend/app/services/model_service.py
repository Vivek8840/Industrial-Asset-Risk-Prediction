
import json
from pathlib import Path

import joblib
import pandas as pd


# Project root: P_227/
PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = PROJECT_ROOT / "models" / "p227_xgboost_pipeline.joblib"
METADATA_PATH = PROJECT_ROOT / "models" / "model_metadata.json"


class ModelService:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

        if not METADATA_PATH.exists():
            raise FileNotFoundError(
                f"Model metadata not found: {METADATA_PATH}"
            )

        self.model = joblib.load(MODEL_PATH)

        with METADATA_PATH.open("r", encoding="utf-8") as file:
            self.metadata = json.load(file)

        self.threshold = float(
            self.metadata["decision_threshold"]
        )
        self.features = self.metadata["features"]

    def predict(self, readings: dict) -> dict:
        # Keep the exact feature names and order from training.
        input_df = pd.DataFrame(
            [{feature: readings[feature] for feature in self.features}]
        )

        probability = float(
            self.model.predict_proba(input_df)[0][1]
        )

        predicted_failure = probability >= self.threshold

        # Initial display bands; these are UI conventions, not
        # independently validated industrial risk categories.
        if predicted_failure:
            risk_level = "HIGH"
        elif probability >= self.threshold * 0.5:
            risk_level = "ELEVATED"
        else:
            risk_level = "LOW"

        return {
            "failure_probability": probability,
            "decision_threshold": self.threshold,
            "predicted_failure": predicted_failure,
            "risk_level": risk_level,
            "model_status": self.metadata.get(
                "status", "unknown"
            ),
        }


model_service = ModelService()
