import pandas as pd
import requests

from .minio_io import write_csv, read_csv, RAW_BUCKET

from .tw_logger import logger


def collect_raw_data(api_url: str, bucket_name: str, run_id: str):
    response = requests.get(api_url)
    if response.status_code == 200:
        logger.info("Data retrieved successfully")
        data = response.json()
        api_df = pd.DataFrame(data=data)
        write_csv(api_df, bucket_name, run_id, "raw_data.csv")
    else:
        logger.error("Failed to retrieve data")
        raise ValueError(f"Error while collecting data from api: {api_url}")


def process_raw_data(bucket_name: str, run_id: str):
    logger.info("Processing data")
    data = read_csv(RAW_BUCKET, run_id, file_name="raw_data.csv")
    data["email"] = data["email"].str.lower()
    write_csv(data, bucket_name, run_id, "processed_data.csv")
    logger.info("Data processed and written to Minio")
