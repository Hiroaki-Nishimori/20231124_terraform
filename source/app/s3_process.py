import os
import boto3
from app.consts import TMP_DIR
from app.logger import set_logger


__s3_client = boto3.Session().client("s3")
download_dir = f"{TMP_DIR}/download"

logger = set_logger(__name__)
def get_bucket_and_key(event: dict) -> tuple[str, str]:
    s3_dict = event["Records"][0]["s3"]
    return s3_dict["bucket"]["name"], s3_dict["object"]["key"]


def prepare_s3_file_to_local(bucket: str, key: str) -> str:
    os.makedirs(download_dir, exist_ok=True)
    filepath = f"{download_dir}/{bucket}/{key}"
    
    if os.path.exists(filepath):
        os.remove(filepath)
    
    fetch_s3_file(bucket, key, filepath)
    logger.info(f"download : {bucket}/{key}")
    return filepath


def fetch_s3_file(bucket: str, key: str, filepath: str) -> None:
    with open(filepath, "wb")as f:
        __s3_client.download_fileobj(bucket, key, f)
    