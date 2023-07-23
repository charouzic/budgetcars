import os
import pandas as pd
import requests

from app.data_processing.car_data_utils import preprocess_data, extract_features
"""
 This module is purelly showcasing how a data pipeline
 downloading data on a regular basis could work.
 The implementation of preprocess_data(df) method will
 depend on the downloaded data.
"""

# Define URLs for dataset download
CAR_DATASET_URL = "https://example.com/car_dataset.csv"

# Define data paths
DATA_DIR = "data"
RAW_DATA_FILE = os.path.join(DATA_DIR, "raw_car_data.csv")
CLEANED_DATA_FILE = os.path.join(DATA_DIR, "cleaned_car_data.csv")

# Step 1: Data Acquisition
def download_dataset(url):
    response = requests.get(url)
    if response.status_code == 200:
        with open(RAW_DATA_FILE, "wb") as f:
            f.write(response.content)
        print("Dataset downloaded successfully.")
    else:
        print("Failed to download dataset.")

# Main function to run the data pipeline
def run_data_pipeline():
    # Step 1: Data Acquisition
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    download_dataset(CAR_DATASET_URL)

    # Step 2: Data Preprocessing (there are some assumption in place)
    raw_data = pd.read_csv(RAW_DATA_FILE)
    cleaned_data = preprocess_data(raw_data)

    # Step 3: Feature Extraction (there are some assumption in place)
    extracted_features_data = extract_features(cleaned_data)

    # Save cleaned and feature extracted data
    extracted_features_data.to_csv(CLEANED_DATA_FILE, index=False)

if __name__ == "__main__":
    run_data_pipeline()
