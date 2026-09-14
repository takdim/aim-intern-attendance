from datetime import date, datetime, time
from zoneinfo import ZoneInfo


DEFAULT_TZ = "Asia/Makassar"


def now_in_tz(tz_name: str = DEFAULT_TZ) -> datetime:
    return datetime.now(ZoneInfo(tz_name))


def today_in_tz(tz_name: str = DEFAULT_TZ) -> date:
    return now_in_tz(tz_name).date()


def parse_time(value: str, default: time) -> time:
    if not value:
        return default
    return datetime.strptime(value, "%H:%M").time()
