from minio import Minio
import pandas as pd
from .tw_logger import logger
from airflow.models import Variable


MINIO_ACCESS_KEY = Variable.get("MINIO_ROOT_USER")
MINIO_SECRET_KEY = Variable.get("MINIO_ROOT_PASSWORD")
MINIO_ENDPOINT_URL = "minio:9000"

RAW_BUCKET = "raw-data"
PROCESSED_BUCKET = "processed-data"


storage_options = {
    "key": MINIO_ACCESS_KEY,
    "secret": MINIO_SECRET_KEY,
    "endpoint_url": "http://minio:9000",
}


client = Minio(
    MINIO_ENDPOINT_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,  # Set to True if you're using HTTPS
)


def write_csv(data: pd.DataFrame, bucket_name: str, run_id: str, file_name: str):
    logger.info(f"Writing data to Minio bucket: {bucket_name}")
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    write_path = f"s3://{bucket_name}/{run_id}/{file_name}"
    try:
        data.to_csv(write_path, index=False, storage_options=storage_options)
        logger.info(f"Data written to {write_path}")
    except Exception as e:
        logger.error(f"Error writing data to Minio: {e}")
        raise


def read_csv(bucket_name: str, run_id: str, file_name: str):
    try:
        return pd.read_csv(
            f"s3://{bucket_name}/{run_id}/{file_name}", storage_options=storage_options
        )
    except Exception as e:
        logger.error(f"Error reading data from Minio {e}")
        raise
