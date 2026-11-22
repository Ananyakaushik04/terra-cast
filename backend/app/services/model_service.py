import joblib
import pandas as pd
from pathlib import Path

from app.core.config import settings


class ModelService:

    def __init__(self):

        # Get models directory from config.py
        self.models_dir = Path(settings.MODELS_DIR)

        # Model file paths
        reg_model_path = self.models_dir / "xgboost_regression.pkl"
        cls_model_path = self.models_dir / "rf_classification.pkl"

        # Initialize models
        self.reg_model = None
        self.cls_model = None

        # Features required by ML models
        self.feature_names = [
            'month', 'hour', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM',
            'PM2_5_lag1', 'PM10_lag1', 'SO2_lag1', 'NO2_lag1',
            'CO_lag1', 'O3_lag1'
        ]

        # Debug information
        print("================================")
        print("TERRACAST MODEL INITIALIZATION")
        print("Models directory:", self.models_dir.resolve())
        print("Regression model exists:", reg_model_path.exists())
        print("Classification model exists:", cls_model_path.exists())
        print("================================")

        try:

            # Check regression model
            if not reg_model_path.exists():
                raise FileNotFoundError(
                    f"Regression model not found: {reg_model_path}"
                )

            # Check classification model
            if not cls_model_path.exists():
                raise FileNotFoundError(
                    f"Classification model not found: {cls_model_path}"
                )

            # Load models
            self.reg_model = joblib.load(reg_model_path)
            self.cls_model = joblib.load(cls_model_path)

            print("Regression model loaded successfully!")
            print("Classification model loaded successfully!")
            print("All TerraCast models loaded successfully!")

        except Exception as e:

            self.reg_model = None
            self.cls_model = None

            print("ERROR LOADING TERRACAST MODELS:", str(e))

    def predict(self, data):

        # Verify models are loaded
        if self.reg_model is None or self.cls_model is None:
            raise Exception(
                "Models are not loaded properly. Check Render logs."
            )

        # Prepare input data
        input_data = pd.DataFrame(
            [[
                data.month,
               
