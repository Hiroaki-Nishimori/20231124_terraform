from app.logger import set_logger
from app import create_message
from app.consts import SET_ADDRESS
from app import ses_process


logger = set_logger(__name__)
tmp_dir = "tmp"
    
def lambda_handler(event, context):
    logger.info("START cost explorer process")
    try:
        period, subject = get_period_and_subject(event)
        message = create_message.main(period)
        response = ses_process.send_email(
            subject=subject,
            body=message,
            source=SET_ADDRESS,
            destination=SET_ADDRESS
        )

        return {
            "stauts": "success",
            "e-mail response": response
        }
    except Exception as e:
        return {
            "status": "failed",
            "error": e
        }


def get_period_and_subject(event: str) -> tuple[str, str]:
    period = event.get("period", "week")
    subject = event.get("subject", f"AWS Cost Report ~{period}~")
    return subject, period