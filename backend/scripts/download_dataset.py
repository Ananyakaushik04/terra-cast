import urllib.request
import zipfile
import os
from pathlib import Path

url = "https://archive.ics.uci.edu/static/public/501/beijing+multi+site+air+quality+data.zip"

# Dynamically locate backend directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Dataset directory
dataset_dir = BASE_DIR / "dataset"
zip_path = dataset_dir / "beijing_aqi.zip"

print("Creating directories...")
dataset_dir.mkdir(parents=True, exist_ok=True)

print(f"Downloading dataset from {url}...")

urllib.request.urlretrieve(url, zip_path)

print("Download complete.")

print("Extracting zip file...")

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(dataset_dir)

print("Extraction complete.")

print("Cleaning up zip file...")

os.remove(zip_path)

# Verify extraction
extracted_files = os.listdir(dataset_dir)

print(f"Successfully prepared dataset. Found {len(extracted_files)} files/folders.")
