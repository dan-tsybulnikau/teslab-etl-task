import datetime
from typing import Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from sqlalchemy.orm import Session

from app.api.api_v1.api import router
from app.core import models
from app.config import Environment
from app.core.database import engine


if Environment.DEV_ENV == "dev":
    models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router)

