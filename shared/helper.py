from datetime import datetime, timedelta
import platform

def ticks_to_date(ticks: int) -> datetime:
    return datetime(1, 1, 1) + timedelta(microseconds=ticks/10)

def date_to_ticks(date: datetime) -> int:
    tz_info = date.tzinfo
    start_of_ticks: datetime = datetime(1, 1, 1, tzinfo=tz_info)
    return  (date - start_of_ticks).total_seconds() * 10000000

def is_windows() -> bool:
    return platform.system() == 'Windows'