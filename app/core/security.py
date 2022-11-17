from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app import Environment


security = HTTPBearer()

def has_access(credentials: HTTPAuthorizationCredentials= Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, key=Environment.SECRET_KEY)
    except JOSEError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e))
        

import os
import requests
def handler(event, context):
    r = requests.get(os.environ.get('SERVICE_URL'), headers={'Authorization': 'Bearer: ' + os.environ.get('TOKEN')})
    return {
    'statusCode': 200,
    'body': 'refreshed'
    }