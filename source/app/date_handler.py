from datetime import date
from dateutil.relativedelta import relativedelta
from dataclasses import dataclass
from typing import Callable
@dataclass
class StrDateInfo:
    start: str
    designated_end: str # コストエクスプローラーで指定する値
    actual_end: str # 集計される締日　メッセージ表記用


today: date = date.today()
def get_previous_from_target_day(
    target_date: date = today,
    prev_num: int = None
) -> str:
    if prev_num <= 0:
        raise ValueError("正の数を指定してください")
    return (target_date - relativedelta(days=prev_num)).isoformat()

str_yesterday = get_previous_from_target_day(prev_num=1)


def get_monthly_date_range() -> StrDateInfo:
    return StrDateInfo(
        start=(today - relativedelta(months=1)).isoformat(),
        designated_end=today.isoformat(),
        actual_end=str_yesterday,
    )


def get_last_weekly_date_range() -> StrDateInfo:
    return StrDateInfo(
        start=get_previous_from_target_day(prev_num=7),
        designated_end=today.isoformat(),
        actual_end=str_yesterday,
    )


def get_yesterday_date_range() -> StrDateInfo:
    return StrDateInfo(
        start=str_yesterday,
        designated_end=today.isoformat(),
        actual_end=str_yesterday,
    )


PERIOD_COST_FUNC: dict[str, Callable] = {
    "day": get_yesterday_date_range,
    "week": get_last_weekly_date_range,
    "month": get_monthly_date_range
}
