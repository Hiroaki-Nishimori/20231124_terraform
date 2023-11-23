from typing import Callable
from app.logger import set_logger
from app import date_handler
from app.date_handler import StrDateInfo
from app import ce_access


logger = set_logger(__name__)

def main(unit_period: str = "week") -> str:
    cost_func: Callable = date_handler.PERIOD_COST_FUNC[unit_period]
    sdi: StrDateInfo
    sdi = cost_func()
    total_cost, detail_cost = ce_access.compute_cost_calculation(
        sdi.start, sdi.designated_end
    )
    messgage = get_message(sdi, total_cost, detail_cost)
    return messgage


def get_message(
    sdi: StrDateInfo,
    total_cost: float,
    detail_cost: dict[str, float]
) -> str:
    summary = get_summary_message(total_cost, sdi.start, sdi.actual_end)
    if total_cost == 0.0:
        return summary
    detail = get_detail_message(detail_cost)
    message = f"ユーザー様\n\n{summary}\n\n{detail}\n\nSincerely,\nYour AWS Cost Bot"
    return message


def get_summary_message(total: float, start: str, end: str) -> str:
    if start == end:
        return f"{start}の請求額: $ {total:.2f} USD"
    return f"{start}～{end}の請求額: $ {total:.2f} USD"


def get_detail_message(service_billings: dict) -> list[str]:
    sort_elems = sorted(
        service_billings.items(), key = lambda service : service[0]
    )
    lines = [
        f"  ・{key}: {value}" for key, value in sort_elems
    ]
    return "\n".join(lines)