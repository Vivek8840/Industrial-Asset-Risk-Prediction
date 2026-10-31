
import os
from datetime import datetime

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

st.set_page_config(
    page_title="P_227 | Industrial Risk Intelligence",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "history" not in st.session_state:
    st.session_state.history = []


# -----------------------------
# API FUNCTIONS
# -----------------------------
def get_model_info():
    try:
        response = requests.get(
            f"{API_URL}/model-info",
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def check_api():
    try:
        response = requests.get(
            f"{API_URL}/health",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def make_prediction(payload):
    response = requests.post(
        f"{API_URL}/predict",
        json=payload,
        timeout=15
    )
    response.raise_for_status()
    return response.json()


# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("🏭 P_227")
    st.caption("Industrial Asset Risk Intelligence")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Risk Prediction",
            "Prediction History",
            "Model Information",
        ],
    )

    st.divider()

    health = check_api()

    if health and health.get("model_loaded"):
        st.success("Backend connected")
    else:
        st.error("Backend unavailable")

    st.caption("AI4I 2020 · XGBoost")


# -----------------------------
# HEADER
# -----------------------------
st.title("Industrial Asset Risk Platform")
st.caption(
    "Predictive maintenance using machine learning "
    "and industrial sensor indicators."
)

model_info = get_model_info()


# -----------------------------
# OVERVIEW
# -----------------------------
if page == "Overview":

    st.subheader("Platform Overview")

    history = st.session_state.history

    total = len(history)
    failures = sum(
        item["predicted_failure"] for item in history
    )
    low_risk = sum(
        item["risk_level"] == "LOW" for item in history
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Predictions", total)
    col2.metric("Predicted Failures", failures)
    col3.metric("Low Risk Results", low_risk)
    col4.metric(
        "Decision Threshold",
        f"{model_info['decision_threshold'] * 100:.0f}%"
        if model_info else "Unavailable"
    )

    st.divider()

    st.subheader("Recent Predictions")

    if history:
        df = pd.DataFrame(history)
        st.dataframe(
            df.tail(10).iloc[::-1],
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info(
            "No predictions yet. Go to Risk Prediction "
            "to analyze your first machine."
        )

    st.subheader("Platform Capabilities")

    a, b, c = st.columns(3)

    a.info("**Machine Learning**\n\nXGBoost failure prediction")
    b.info("**Risk Intelligence**\n\nThreshold-based classification")
    c.info("**Asset Analytics**\n\nPrediction history and trends")


# -----------------------------
# RISK PREDICTION
# -----------------------------
elif page == "Risk Prediction":

    st.subheader("Machine Sensor Analysis")

    st.write(
        "Enter the current sensor readings of an industrial asset."
    )

    with st.form("prediction_form"):

        asset_id = st.text_input(
            "Asset ID",
            value="ASSET-001"
        )

        machine_type = st.selectbox(
            "Machine Type",
            ["L", "M", "H"],
            help="AI4I machine quality category."
        )

        c1, c2 = st.columns(2)

        with c1:
            air_temp = st.number_input(
                "Air Temperature (K)",
                min_value=250.0,
                max_value=350.0,
                value=300.0,
                step=0.1,
            )

            rotational_speed = st.number_input(
                "Rotational Speed (rpm)",
                min_value=1,
                max_value=5000,
                value=1500,
            )

            tool_wear = st.number_input(
                "Tool Wear (min)",
                min_value=0,
                max_value=500,
                value=100,
            )

        with c2:
            process_temp = st.number_input(
                "Process Temperature (K)",
                min_value=250.0,
                max_value=400.0,
                value=310.0,
                step=0.1,
            )

            torque = st.number_input(
                "Torque (Nm)",
                min_value=0.0,
                max_value=200.0,
                value=40.0,
                step=0.1,
            )

        submitted = st.form_submit_button(
            "Analyze Machine Risk",
            use_container_width=True,
            type="primary",
        )

    if submitted:

        if not asset_id.strip():
            st.error("Please enter an Asset ID.")
        else:
            payload = {
                "Type": machine_type,
                "Air temperature [K]": air_temp,
                "Process temperature [K]": process_temp,
                "Rotational speed [rpm]": rotational_speed,
                "Torque [Nm]": torque,
                "Tool wear [min]": tool_wear,
            }

            try:
                with st.spinner("Analyzing sensor readings..."):
                    result = make_prediction(payload)

                record = {
                    "timestamp": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "asset_id": asset_id,
                    "machine_type": machine_type,
                    **payload,
                    **result,
                }

                st.session_state.history.append(record)

                st.divider()
                st.subheader("Prediction Result")

                probability = result["failure_probability"]
                threshold = result["decision_threshold"]

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Model Score",
                    f"{probability * 100:.4f}%"
                )

                col2.metric(
                    "Decision Threshold",
                    f"{threshold * 100:.2f}%"
                )

                col3.metric(
                    "Risk Classification",
                    result["risk_level"]
                )

                if result["predicted_failure"]:
                    st.error(
                        "Failure predicted: this reading "
                        "crosses the configured decision threshold."
                    )
                else:
                    st.success(
                        "No failure predicted at the configured "
                        "decision threshold."
                    )

                st.progress(min(max(probability, 0.0), 1.0))

                st.caption(
                    "This score is not a calibrated real-world "
                    "failure probability or a guarantee of machine safety."
                )

            except requests.RequestException as error:
                st.error(f"Prediction API error: {error}")


# -----------------------------
# PREDICTION HISTORY
# -----------------------------
elif page == "Prediction History":

    st.subheader("Prediction History")

    history = st.session_state.history

    if history:
        df = pd.DataFrame(history)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        fig = px.bar(
            df,
            x="asset_id",
            y="failure_probability",
            color="risk_level",
            title="Model Scores by Asset",
            labels={
                "asset_id": "Asset",
                "failure_probability": "Model Score",
            },
        )

        st.plotly_chart(fig, use_container_width=True)

        if st.button("Clear Session History"):
            st.session_state.history = []
            st.rerun()

    else:
        st.info("No prediction history available in this session.")


# -----------------------------
# MODEL INFORMATION
# -----------------------------
elif page == "Model Information":

    st.subheader("Model Information")

    if model_info:

        col1, col2 = st.columns(2)

        col1.metric(
            "Algorithm",
            model_info["algorithm"]
        )

        col2.metric(
            "Decision Threshold",
            f"{model_info['decision_threshold']:.2f}"
        )

        st.write("**Project:**", model_info["project"])
        st.write("**Model Status:**", model_info["status"])

        st.write("### Model Features")

        st.dataframe(
            pd.DataFrame({
                "Feature": model_info["features"]
            }),
            use_container_width=True,
            hide_index=True,
        )

        st.write("### Model Limitations")

        for limitation in model_info.get("limitations", []):
            st.warning(limitation)

    else:
        st.error("Unable to retrieve model information.")

st.divider()

st.caption(
    "P_227 | AI-Based Industrial Asset Risk Prediction Platform "
    "| Prototype"
)
