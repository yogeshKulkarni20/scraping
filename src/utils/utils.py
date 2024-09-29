from datetime import datetime, timedelta
from src.constant import iso_format_date_time


def getToday(format=iso_format_date_time) -> str:
    return datetime.now().strftime(format)


def getLastNthDay(duration: int, format=iso_format_date_time) -> str:
    return (datetime.now() - timedelta(days=duration)
            ).strftime(format)
