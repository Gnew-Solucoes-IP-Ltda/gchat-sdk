import pytz
from datetime import datetime


class Chat:
    
    def __init__(self, id, last_message_date, is_me):
        self.id = id
        self.last_message_date = self._date_converter(last_message_date)
        self.is_me = is_me

    def _date_converter(self, date_string):
        return datetime.fromisoformat(date_string).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))