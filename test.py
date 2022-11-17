import requests
import xmltodict
from pprint import pprint
from types import SimpleNamespace
import json
from pydantic import BaseModel, parse_obj_as, validator, ValidationError


data = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002')
raw = xmltodict.parse(data.text)
# pprint(raw)

class Currency(BaseModel):
    id:str
    code: str
    name: str
    num_code: int


    def __init__(self, **kwargs):
        kwargs["id"] = kwargs["@ID"]
        kwargs["code"] = kwargs["CharCode"]
        kwargs["name"] = kwargs["Name"]
        kwargs["nominal"] = kwargs["Nominal"]
        kwargs["num_code"] = kwargs["NumCode"]
        kwargs["value"] = kwargs["Value"].replace(',', '.')
        super().__init__(**kwargs)

    @validator('code')
    def validate_code(cls, v: str):
        if len(v) != 3 or not v.isalpha():
            raise ValidationError('not valid code')
        return v


class CurrencyValue(BaseModel):
    nominal: int
    num_code: int
    code: float
    date: str
    currency: Currency


    def __init__(self, **kwargs):
        kwargs["id"] = kwargs["@ID"]
        kwargs["code"] = kwargs["CharCode"]
        kwargs["name"] = kwargs["Name"]
        kwargs["nominal"] = kwargs["Nominal"]
        kwargs["num_code"] = kwargs["NumCode"]
        kwargs["value"] = kwargs["Value"].replace(',', '.')
        super().__init__(**kwargs)


    @validator('code')
    def validate_code(cls, v: str):
        if len(v) != 3 or not v.isalpha():
            raise ValidationError('not valid code')
        return v

all = []
for chunk in raw['ValCurs']['Valute']:
    all.append(Currency(**chunk))
pprint(all)