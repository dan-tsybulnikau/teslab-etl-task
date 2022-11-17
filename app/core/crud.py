import datetime
from typing import Any

from sqlalchemy.orm import Session

from app.core import models, schema


def create_currency(db: Session, currency: schema.Currency):
    db_currency = models.Currency(currency_id=currency.currency_id,name=currency.name,char_code=currency.char_code, num_code=currency.num_code)
    db.add(db_currency)
    db.commit()
    db.refresh(db_currency)
    return db_currency

def create_rate_record(db: Session, rate: schema.CurrencyValue):
    db_rate = models.CurrencyRate(nominal=rate.nominal,value=rate.value,date_captured=rate.date_captured, currency_id=rate.currency_id)
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

def get_currency_rate(db: Session, rate: schema.CurrencyValue):
    return db.query(models.CurrencyRate).filter(models.CurrencyRate.date_captured == rate.date_captured, models.CurrencyRate.currency_id == rate.currency_id).first()

def get_currency_rate_on_date(db: Session, date: datetime.datetime, skip: int = 0, limit: int = 100):
    return db.query(models.CurrencyRate).filter(models.CurrencyRate.date_captured == date).offset(skip).limit(limit).all()

