import os
import requests
from http import HTTPStatus

def handler(event, context):
    r = requests.get(os.environ['SERVICE_URL'], headers={'Authorization': 'Bearer: ' + os.environ['TOKEN']})
    return {
    'statusCode': HTTPStatus.OK,
    'body': 'refreshed'
    }