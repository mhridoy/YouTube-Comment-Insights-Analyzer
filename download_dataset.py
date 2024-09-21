import os
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import logging
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Check if Kaggle API credentials are set
if not os.environ.get('KAGGLE_USERNAME') or not os.environ.get('KAGGLE_KEY'):
    logger.error("Kaggle API credentials are not set. Please set KAGGLE_USERNAME and KAGGLE_KEY environment variables.")
    raise ValueError("Kaggle API credentials are not set")

# Set up Kaggle API
api = KaggleApi()
try:
    api.authenticate()
    logger.info("Kaggle API authentication successful")
except Exception as e:
    logger.error(f"Kaggle API authentication failed: {str(e)}")
    raise

# Define the dataset to download
dataset = "muhammadanasmahmood/youtube-comments"
output_dir = "dataset"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    logger.info(f"Created output directory: {output_dir}")

# Download the dataset
logger.info(f"Starting download of dataset: {dataset}")
try:
    api.dataset_download_files(dataset, path=output_dir, unzip=False)
    logger.info(f"Dataset downloaded to: {output_dir}")
except Exception as e:
    logger.error(f"Failed to download dataset: {str(e)}")
    if isinstance(e, kaggle.rest.ApiException):
        logger.error(f"Kaggle API Exception: {e.status}, {e.reason}")
        logger.error(f"Response headers: {e.headers}")
    raise

# Locate the downloaded zip file
zip_file = os.path.join(output_dir, f"{dataset.split('/')[-1]}.zip")
if os.path.exists(zip_file):
    logger.info(f"Unzipping dataset: {zip_file}")
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        os.remove(zip_file)  # Remove zip file after extraction
        logger.info("Dataset unzipped successfully")
    except Exception as e:
        logger.error(f"Failed to unzip dataset: {str(e)}")
        raise
else:
    logger.warning("No zip file found. Dataset may already be unzipped or download may have failed.")

# List the contents of the dataset directory and print first few lines of CSV files
logger.info("\nContents of the dataset directory:")
try:
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
        logger.info(f"- {file} (Size: {file_size:.2f} MB)")
        
        if file.endswith('.csv'):
            logger.info(f"\nFirst few lines of {file}:")
            df = pd.read_csv(file_path, nrows=5)
            logger.info(df.to_string())
except Exception as e:
    logger.error(f"Failed to list directory contents or read CSV files: {str(e)}")

logger.info("\nDataset download, extraction, and preview complete.")
