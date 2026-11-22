import os
from pathlib import Path

# Backend directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset directory
DATASET_DIR = BASE_DIR / "dataset"

# Dataset file
DATASET_PATH = DATASET_DIR / "beijing_aqi_merged.csv"


# Load environment variables from .env if available
env_path = BASE_DIR / ".env"

if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)

                os.environ.setdefault(
                    key.strip(),
                    val.strip().strip('"').strip("'")
                )


class Settings:

    PROJECT_NAME = "TerraCast AI Engine"

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

    MODELS_DIR = Path(
        os.getenv("MODELS_DIR", str(BASE_DIR / "models"))
    )

    DATASET_DIR = DATASET_DIR
    DATASET_PATH = DATASET_PATH


settings = Settings()
