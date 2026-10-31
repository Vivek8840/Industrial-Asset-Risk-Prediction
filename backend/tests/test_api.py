
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["model_loaded"] is True


def test_model_info():
    response = client.get("/model-info")

    assert response.status_code == 200
    assert response.json()["decision_threshold"] == 0.09


def test_predict():
    payload = {
        "Type": "M",
        "Air temperature [K]": 300.0,
        "Process temperature [K]": 310.0,
        "Rotational speed [rpm]": 1500,
        "Torque [Nm]": 40.0,
        "Tool wear [min]": 100,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()
    assert 0 <= result["failure_probability"] <= 1
    assert result["decision_threshold"] == 0.09
    assert isinstance(result["predicted_failure"], bool)


def test_invalid_machine_type():
    payload = {
        "Type": "Z",
        "Air temperature [K]": 300.0,
        "Process temperature [K]": 310.0,
        "Rotational speed [rpm]": 1500,
        "Torque [Nm]": 40.0,
        "Tool wear [min]": 100,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
