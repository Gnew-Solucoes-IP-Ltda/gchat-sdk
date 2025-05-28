import pytz
from datetime import datetime


class Contact:

    def __init__(self, id: str, name: str, number: str) -> None:
        self.id = id
        self.name = name
        self.number = number


class Chat:
    
    def __init__(self, id: str, last_message_date: str, is_me: bool, contact: Contact):
        self.id = id
        self.last_message_date = self._date_converter(last_message_date)
        self.is_me = is_me
        self.contact = contact

    def _date_converter(self, date_string):
        return datetime.fromisoformat(date_string).replace(tzinfo=pytz.timezone("America/Sao_Paulo"))