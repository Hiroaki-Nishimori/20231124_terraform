import shutil
import json


from app.logger import set_logger
from app import create_message
from app import s3_process
from app.consts import TMP_DIR, SET_ADDRESS
from app import ses_process


logger = set_logger(__name__)
tmp_dir = "tmp"
    
def lambda_handler(event, context):
    logger.info("START cost explorer process")
    try:
        bucket, key = s3_process.get_bucket_and_key(event)
        filepath = s3_process.prepare_s3_file_to_local(filepath)
        subject, unit_period = get_subject_and_period(filepath)
        message = create_message.main(unit_period)
        response = ses_process.send_email(
            subject=subject,
            body=message,
            source=SET_ADDRESS,
            destination=SET_ADDRESS
        )

        shutil.rmtree(TMP_DIR)
        return {
            "stauts": "success",
            "bucket": bucket,
            "key": key,
            "e-mail response": response
        }
    except Exception as e:
        logger.exception(f"error occyred: {e}")
        return {
            "status": "failed",
            "bucket": bucket,
            "key": key,
            "error": e
        }


def get_subject_and_period(json_path: str) -> tuple[str, str]:
    with open(json_path, "r") as file:
        data = json.load(file)
    subject = data.get("subject", "AWS Monthly Cost Report")
    period = data.get("period", "week")
    return subject, period