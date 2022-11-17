import os
import requests
def handler(event, context):
    r = requests.get(os.environ['SERVICE_URL'], headers={'Authorization': 'Bearer: ' + os.environ['TOKEN']})
    return {
    'statusCode': 200,
    'body': 'refreshed'
    }