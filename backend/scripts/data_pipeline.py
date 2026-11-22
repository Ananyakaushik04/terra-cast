import os
import zipfile
import pandas as pd
import glob
from pathlib import Path

# Dynamically locate backend directory
BASE_DIR = Path(__file__).resolve().parents[1]

# Dataset paths
dataset_dir = BASE_DIR / "dataset"
nested_zip = dataset_dir / "PRSA2017_Data_20130301-20170228.zip"
extract_folder = dataset_dir / "PRSA_Data_20130301-20170228"
output_csv = dataset_dir / "beijing_aqi_merged.csv"

# Create dataset directory if missing
dataset_dir.mkdir(parents=True, exist_ok=True)

# 1. Extract nested ZIP if needed
if nested_zip.exists() and not extract_folder.exists():
    print("Extracting nested zip...")

    with zipfile.ZipFile(nested_zip, 'r') as zip_ref:
        zip_ref.extractall(dataset_dir)

    print("Extraction complete.")

# 2. Locate station CSV files
print("Locating station CSV files...")

csv_files = glob.glob(str(extract_folder / "*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No station CSV files found in {extract_folder}"
    )

print(f"Found {len(csv_files)} station files. Merging...")

dfs = []

for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

merged_df = pd.concat(dfs, ignore_index=True)

print(f"Merged dataset shape: {merged_df.shape}")

# 3. Handle missing values
print("Handling missing values...")

merged_df.ffill(inplace=True)
merged_df.bfill(inplace=True)

# 4. Save merged dataset
print(f"Saving merged dataset to {output_csv}...")

merged_df.to_csv(output_csv, index=False)

print("Data preprocessing complete!")
print(f"Dataset saved successfully: {output_csv}")
