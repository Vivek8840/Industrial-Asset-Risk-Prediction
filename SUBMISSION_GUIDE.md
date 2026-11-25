# P_227 — Submission Guide

**Learner:** Vivek Mani Tripathi  
**Roll Number:** 2300321540210  
**College:** ABES Engineering College, Ghaziabad  
**Programme:** HCLTech Career Shaper Programme, 2026–27  
**Project:** P_227 — AI-Based Industrial Asset Risk Prediction Platform

## Submission contents

- `README.md` — project overview, architecture, setup, API and limitations.
- `backend/` — FastAPI application, model service, request/response schemas and API tests.
- `dashboard/` — Streamlit user interface.
- `models/` — saved XGBoost pipeline and metadata required for inference.
- `data/raw/ai4i2020.csv` — AI4I 2020 dataset used for the project.
- `notebooks/` — data exploration, preprocessing, model development and threshold selection.
- `scripts/inspect_dataset.py` — dataset inspection utility.
- `reports/final_test_metrics.json` — recorded evaluation metrics.
- `reports/Project_Synopsis_Vivek_Mani_Tripathi_2300321540210.pdf` — project synopsis.
- `docs/images/` — dashboard and prediction screenshots.
- `docs/dataset_notes.md` — dataset description and limitations.

## Run the application locally

Use Python 3.10 or later. Open a terminal in the project root.

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
python -m pip install -r backend/requirements.txt
python -m pip install -r dashboard/requirements.txt
```

The saved model was created using the library versions recorded in `models/model_metadata.json`. In particular, keep scikit-learn and XGBoost compatible with those recorded versions when loading the joblib artifact.

### 2. Start the FastAPI backend

From the project root:

```bash
python -m uvicorn app.main:app --reload --app-dir backend
```

Check:
- Health: http://127.0.0.1:8000/health
- API documentation: http://127.0.0.1:8000/docs

### 3. Start the Streamlit dashboard

Open a second terminal in the project root:

```bash
streamlit run dashboard/app.py
```

Open the local URL printed by Streamlit (normally http://localhost:8501).

The dashboard defaults to `http://127.0.0.1:8000` for the API. If a different backend address is needed, set `API_URL` in a local `.env` file using `.env.example` as a template.

## Run API tests

From the project root:

```bash
python -m pytest backend/tests -q
```

The included API tests cover the health endpoint, model metadata endpoint, valid prediction request and invalid machine type validation.

## GitHub repository

https://github.com/Vivek8840/Industrial-Asset-Risk-Prediction

Before submitting, push the final cleaned project files to this repository and verify that the README, `models/p227_xgboost_pipeline.joblib`, `models/model_metadata.json`, `data/raw/ai4i2020.csv`, screenshots and synopsis are visible in the GitHub repository.

## Current implementation status

The FastAPI backend and Streamlit dashboard are a locally demonstrated prototype. Public cloud deployment is pending. ESP32 sensor acquisition, MQTT ingestion, PostgreSQL persistence and Grafana monitoring are future extensions or deferred work, not completed features.

## Model and safety limitations

The AI4I 2020 dataset is synthetic and does not establish performance on real industrial equipment. The classifier score is not guaranteed to be a calibrated real-world failure probability. A HIGH risk classification is a prototype decision-support alert; it must not trigger automatic machine shutdown or replace engineering inspection and established safety procedures.

## Final pre-submission checklist

- [ ] Confirm the synopsis details and sign/date the PDF.
- [ ] Upload the cleaned project folder or ZIP.
- [ ] Push the same final files to GitHub.
- [ ] Verify the GitHub repository is public or accessible to the evaluator.
- [ ] Verify the model file and dataset are present in GitHub.
- [ ] Test the backend and dashboard on the submission machine.
- [ ] Do not include `.env`, passwords, tokens, virtual environments or cache folders.
