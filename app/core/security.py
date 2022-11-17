from http import HTTPStatus
from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.config import Environment


security = HTTPBearer()

def has_access(credentials: HTTPAuthorizationCredentials= Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, key=Environment.SECRET_KEY)
    except JOSEError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=str(e))
        