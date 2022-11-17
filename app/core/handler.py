from typing import Union

import requests
import xmltodict

from app import Environment


class DataHandler:
    def __init__(self, url: str) -> None:
        self.url = url

    def extract_data_from_xml(self, data):
        raw = xmltodict.parse(data.text)
        date = raw['ValCurs']['@Date']
        local = [x for x in raw['ValCurs']['Valute'] if x['CharCode'] in Environment.CHECKED_CURRENCY]
        list(map(lambda x: x.update({'@Date': date}), local))
        return local

    def get_data_on_date(self, date: Union[str, None] = None):
        url_suffix = f"?date_req={date}" if date else ""
        data = requests.get('https://www.cbr.ru/scripts/XML_daily.asp' + url_suffix)
        if data.status_code == 200:
            return self.extract_data_from_xml(data)
        else:
            return None
        
        
