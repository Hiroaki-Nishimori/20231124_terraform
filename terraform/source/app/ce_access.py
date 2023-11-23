import boto3
from botocore.client import BaseClient
import os
from app.logger import set_logger

REGION_NAME = os.getenv("REGION_NAME", "ap-northeast-1")

__ce_client: BaseClient = boto3.client("ce", region_name=REGION_NAME)
__granularity = "DAILY"
__metrics = "UnblendedCost"

logger = set_logger(__name__)

def compute_cost_calculation(
    str_start: str,
    str_end: str
) -> tuple[float, dict[str, float]]:
    response = get_cost_and_usage(str_start, str_end)
    logger.info(f"response: \n\n{response}\n")
    total_cost, details = aggregate_billings_per_service(response)
    zero_filtered = exclude_zero_cost(details)
    return total_cost, zero_filtered


def get_cost_and_usage(
    str_start: str,
    str_end: str,
    granularity: str = __granularity,
    metrics: str = __metrics
) -> dict:
    return __ce_client.get_cost_and_usage(
        TimePeriod={"Start": str_start, "End": str_end},
        Granularity=granularity,
        Metrics=[metrics],
        GroupBy=[{"Type": "DIMENSION", "Key": "SERVICE"}]
    )


# サービスごとの集計
def aggregate_billings_per_service(
    response: dict, metrics: str = __metrics
) -> tuple[dict[str, float], float]:
    details = {}
    total_cost = 0.0
    results = response["ResultsByTime"]
    for result in results:
        for service in result["Groups"]:
            name = service["Keys"][0]

            # 新しいキーに対して初期値を設定
            if name not in details:
                details[name] = 0.0
            cost = float(service["Metrics"][metrics]["Amount"])
            details[name] += cost
            total_cost += cost

    return round(total_cost, 2), details 


# コストがかかってないものは除外
def exclude_zero_cost(service_billings: dict[str, float]):
    filtered_zero = filter(
        lambda item: item[1] != 0.0, service_billings.items()
    )
    return dict(filtered_zero)
