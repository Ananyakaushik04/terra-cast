from fastapi import APIRouter, HTTPException
import pandas as pd
from pathlib import Path

from app.api.schemas import PredictionInput
from app.services.model_service import model_service
from app.services.shap_service import shap_service
from app.services.expert_service import llm_service
from app.core.config import settings

router = APIRouter()


# ==========================================
# 1. DATASET SAMPLE API
# ==========================================

@router.get("/dataset/sample")
def get_dataset_sample(station: str = None):
    """
    Returns a random historical row from the Beijing PRSA dataset.
    Supports optional station filtering.
    """

    try:
        # Dynamically locate the dataset directory
        BASE_DIR = Path(__file__).resolve().parents[2]

        csv_path = BASE_DIR / "dataset" / "beijing_aqi_merged.csv"

        # Check dataset availability
        if not csv_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Dataset file not found: {csv_path}"
            )

        # Load CSV dataset
        df = pd.read_csv(csv_path)

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="Dataset is empty"
            )

        # Required columns
        required_columns = [
            "month",
            "hour",
            "TEMP",
            "PRES",
            "DEWP",
            "RAIN",
            "WSPM",
            "PM2.5",
            "PM10",
            "SO2",
            "NO2",
            "CO",
            "O3",
            "station",
            "year",
            "day"
        ]

        # Validate columns
        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=500,
                detail=f"Missing dataset columns: {missing_columns}"
            )

        # Remove rows with missing required values
        df = df.dropna(subset=required_columns)

        if df.empty:
            raise HTTPException(
                status_code=404,
                detail="No valid dataset records available"
            )

        # Filter by station if provided
        if station:
            station_df = df[
                df["station"].astype(str).str.lower()
                == station.lower()
            ]

            if station_df.empty:
                raise HTTPException(
                    status_code=404,
                    detail=f"No data found for station: {station}"
                )

            df = station_df

        # Select a random historical record
        row = df.sample(1).iloc[0]

        return {
            "month": int(row["month"]),
            "hour": int(row["hour"]),

            "TEMP": round(float(row["TEMP"]), 1),
            "PRES": round(float(row["PRES"]), 1),
            "DEWP": round(float(row["DEWP"]), 1),
            "RAIN": round(float(row["RAIN"]), 1),
            "WSPM": round(float(row["WSPM"]), 1),

            "PM2_5_lag1": round(float(row["PM2.5"]), 1),
            "PM10_lag1": round(float(row["PM10"]), 1),
            "SO2_lag1": round(float(row["SO2"]), 1),
            "NO2_lag1": round(float(row["NO2"]), 1),
            "CO_lag1": round(float(row["CO"]), 1),
            "O3_lag1": round(float(row["O3"]), 1),

            "station": str(row["station"]),
            "year": int(row["year"]),
            "day": int(row["day"])
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Dataset Sample Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=f"Dataset loading failed: {str(e)}"
        )


# ==========================================
# 2. FAST ML PREDICTION API
# ==========================================

@router.post("/predict/fast")
def predict_fast(data: PredictionInput):
    """
    Returns ML predictions and SHAP feature importance.
    """

    try:
        aqi_pred, category_name, input_data = model_service.predict(data)

        top_features = shap_service.get_top_features(
            input_data,
            top_n=6
        )

        return {
            "aqi_prediction": round(aqi_pred, 1),
            "health_category": category_name,
            "top_driving_features": top_features
        }

    except Exception as e:
        print("Fast Prediction Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================
# 3. AI POLICY RECOMMENDATION API
# ==========================================

@router.post("/predict/policy")
def predict_policy(data: PredictionInput):
    """
    Generates an AI-based policy brief using the LLM service.
    """

    try:
        aqi_pred, category_name, input_data = model_service.predict(data)

        top_features = shap_service.get_top_features(
            input_data,
            top_n=6
        )

        policy_brief = llm_service.generate_policy_brief(
            round(aqi_pred, 1),
            category_name,
            top_features,
            extended_context=data
        )

        return {
            "policy_brief": policy_brief
        }

    except Exception as e:
        print("Policy Generation Error:", str(e))

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
