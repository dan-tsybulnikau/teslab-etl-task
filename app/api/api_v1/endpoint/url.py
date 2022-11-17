import datetime
from http import HTTPStatus
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app import Environment
from app.core import crud
from app.core.schema import Currency, CurrencyValue
from app.core.database import get_db
from app.core.security import has_access
from app.core.handler import DataHandler

DATE_FORMAT = '%d/%m/%Y'
DATE_VALIDATOR = r"[\d]{2}/[\d]{2}/[\d]{4}"

router = APIRouter()
data_connector = DataHandler(Environment.CBR_URL)

@router.get("/refresh", dependencies=[Depends(has_access)])
def refresh(db: Session = Depends(get_db), date: Optional[str] = None):
    data = data_connector.get_data_on_date(date)
    
    if not data:
        return JSONResponse(content='Parsing was unsuccessful', status_code=HTTPStatus.BAD_REQUEST)
    
    for item in data:
        currency_record = Currency(**item)
        currency_rate_record = CurrencyValue(**item)
        try:
            crud.create_currency(db=db, currency=currency_record)
        except exc.IntegrityError:
            db.rollback()
        is_record_in_db = crud.get_currency_rate(db=db, rate=currency_rate_record)
        if not is_record_in_db:
            crud.create_rate_record(db=db, rate=currency_rate_record)
    return JSONResponse(data)

@router.get('/currency_rate', dependencies=[Depends(has_access)])
def get_currency_records(db: Session = Depends(get_db), date: str = Query(regex=DATE_FORMAT)):
    query_date = datetime.datetime.strptime(date, DATE_FORMAT)
    rate_records = crud.get_currency_rate_on_date(db=db, date=query_date)
    return JSONResponse(content=jsonable_encoder(rate_records))
    
    