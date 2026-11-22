import zipfile
from pathlib import Path

# Dynamically locate backend directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Dataset directory
dataset_dir = BASE_DIR / "dataset"

# ZIP file path
nested_zip = dataset_dir / "PRSA2017_Data_20130301-20170228.zip"

# Check whether ZIP exists
if not nested_zip.exists():
    raise FileNotFoundError(f"ZIP file not found: {nested_zip}")

# Extract ZIP
print("Extracting nested zip...")

with zipfile.ZipFile(nested_zip, 'r') as zip_ref:
    zip_ref.extractall(dataset_dir)

print("Extraction complete!")
