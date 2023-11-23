import boto3
from app.consts import REGION_NAME


__ses_client = boto3.client("ses", region_name=REGION_NAME)

def send_email(
    subject: str,
    body: str,
    source: str,
    destination: str
):
    response = __ses_client.send_email(
        Source=source,
        Destination={
            'ToAddresses': [destination]
        },
        Message={
            "Subject": {
                "Data": subject
            },
            "Body": {
                "Text": {
                    "Data": body
                }
            }
        }
    )
    return response