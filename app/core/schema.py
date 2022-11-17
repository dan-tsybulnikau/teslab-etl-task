import datetime

from pydantic import BaseModel, ValidationError, validator


class Currency(BaseModel):
    currency_id:str
    name: str
    char_code: str
    num_code: str


    def __init__(self, **kwargs):
        kwargs["currency_id"] = kwargs["@ID"]
        kwargs["char_code"] = kwargs["CharCode"]
        kwargs["name"] = kwargs["Name"]
        kwargs["num_code"] = kwargs["NumCode"]
        super().__init__(**kwargs)

    @validator('char_code')
    def validate_code(cls, v: str):
        if len(v) != 3 or not v.isalpha():
            raise ValidationError('not valid char_code', Currency)
        return v

    class Config:
        orm_mode = True


class CurrencyValue(BaseModel):
    nominal: int
    value: float
    date_captured: datetime.datetime
    currency_id: str


    def __init__(self, **kwargs):
        kwargs["currency_id"] = kwargs["@ID"]
        kwargs["date_captured"] = datetime.datetime.strptime(kwargs["@Date"], '%d.%m.%Y')
        kwargs["nominal"] = kwargs["Nominal"]
        kwargs["value"] = kwargs["Value"].replace(',', '.')
        super().__init__(**kwargs)

    class Config:
        orm_mode = True