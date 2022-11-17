import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core import schema
from app.core.models import Currency, CurrencyRate

STANDARD_SKIP = 0
STANDARD_LIMIT = 100

def create_currency(db: Session, currency: schema.Currency):
    db_currency = Currency(currency_id=currency.currency_id,name=currency.name,char_code=currency.char_code, num_code=currency.num_code)
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency

def create_rate_record(db: Session, rate: schema.CurrencyValue):
    db_rate = CurrencyRate(nominal=rate.nominal,value=rate.value,date_captured=rate.date_captured, currency_id=rate.currency_id)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

def get_currency_rate(db: Session, rate: schema.CurrencyValue):
    return db.query(CurrencyRate).filter(CurrencyRate.date_captured == rate.date_captured, CurrencyRate.currency_id == rate.currency_id).first()

def get_currency_rate_on_date(db: Session, date: datetime.datetime, skip: int = 0, limit: int = 100):
    return db.query(CurrencyRate).filter(CurrencyRate.date_captured == date).offset(STANDARD_SKIP).limit(STANDARD_LIMIT).all()

