import pytz
from datetime import datetime, timedelta


def get_limit_date(hours: int) -> datetime:
    return datetime.now(pytz.timezone("America/Sao_Paulo")) - timedelta(hours=hours) 