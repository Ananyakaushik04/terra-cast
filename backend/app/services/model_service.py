import os
import joblib
import pandas as pd
from pathlib import Path

from app.core.config import settings


class ModelService:

    def __init__(self):

        # Use the models directory defined in config.py
        models_dir = Path(settings.MODELS_DIR)

        reg_model_path = models_dir / "xgboost_regression.pkl"
        cls_model_path = models_dir / "rf_classification.pkl"

        self.reg_model = None
        self.cls_model = None

        self.feature_names = [
            'month', 'hour', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM',
            'PM2_5_lag1', 'PM10_lag1', 'SO2_lag1', 'NO2_lag1',
            'CO_lag1', 'O3_lag1'
        ]

        print("Models directory:", models_dir.resolve())
        print("Regression model exists:", reg_model_path.exists())
        print("Classification model exists:", cls_model_path.exists())

        try:
            if not reg_model_path.exists():
                raise FileNotFoundError(
                    f"Regression model not found: {reg_model_path}"
                )

            if not cls_model_path.exists():
                raise FileNotFoundError(
                    f"Classification model not found: {cls_model_path}"
                )

            self.reg_model = joblib.load(reg_model_path)
            self.cls_model = joblib.load(cls_model_path)

            print("Models loaded successfully!")

        except Exception as e:
            print(f"ERROR LOADING MODELS: {e}")

    def predict(self, data):

        if self.reg_model is None or self.cls_model is None:
            raise Exception("Models are not loaded properly.")

        input_data = pd.DataFrame([[
            data.month, data.hour, data.TEMP, data.PRES, data.DEWP,
            data.RAIN, data.WSPM, data.PM2_5_lag1, data.PM10_lag1,
            data.SO2_lag1, data.NO2_lag1, data.CO_lag1, data.O3_lag1
        ]], columns=self.feature_names)

        aqi_pred = float(self.reg_model.predict(input_data)[0])

        class_pred = int(self.cls_model.predict(input_data)[0])

        categories = ["Good", "Moderate", "Unhealthy", "Hazardous"]

        category_name = (
            categories[class_pred]
            if 0 <= class_pred < 4
            else "Unknown"
        )

        return aqi_pred, category_name, input_data


model_service = ModelService()

        return aqi_pred, category_name, input_data


model_service = ModelService()
