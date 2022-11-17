from http import HTTPStatus
from typing import Union, List
import requests
import xmltodict

from app import Environment


class DataHandler:
    def __init__(self, url: str) -> None:
        self.url = url

    def extract_data_from_xml(self, data: str) -> List:
        raw = xmltodict.parse(data)
        date = raw['ValCurs']['@Date']
        local = [x for x in raw['ValCurs']['Valute'] if x['CharCode'] in Environment.CHECKED_CURRENCY]
        list(map(lambda x: x.update({'@Date': date}), local))
        return local

    def get_data_on_date(self, date: Union[str, None] = None) -> Union[List, None]:
        params = {'dare_req':date} if date else None
        data = requests.get('https://www.cbr.ru/scripts/XML_daily.asp', params=params)
        if data.status_code == HTTPStatus.OK:
            return self.extract_data_from_xml(data.text)
        else:
            return None
        
        
