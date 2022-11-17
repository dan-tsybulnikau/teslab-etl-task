from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from app.core.database import Base


class Currency(Base):
    __tablename__ = 'currency'
    currency_id = Column(String, primary_key=True, index=True)
    name = Column(String)
    num_code = Column(Integer)
    char_code = Column(String)


class CurrencyRate(Base):
    __tablename__ = 'currency_rate'
    rate_id = Column(Integer, primary_key=True)
    nominal = Column(Integer)
    value = Column(Float)
    date_captured = Column(DateTime())
    currency_id = Column(String, ForeignKey('currency.currency_id'))
    
    currency = relationship('Currency', cascade='all, delete')
