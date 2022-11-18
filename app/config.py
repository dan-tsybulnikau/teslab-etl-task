import json
import os


class Environment:
    CBR_URL = os.environ.get("CBR_URL", 'https://www.cbr.ru/scripts/XML_daily.asp')
    DB_URI = os.environ.get("DB_URI", "postgresql://postgres:postgres@localhost:15432/postgres")
    CHECKED_CURRENCY = json.loads(os.environ.get('CHECKED_CURRENCY', '["RUB", "USD", "EUR"]'))
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret")
    ENV_TYPE = os.environ.get("ENV_TYPE", 'dev')
    DATE_FORMAT = os.environ.get("DATE_FORMAT", "%d.%m.%Y")
    DATE_VALIDATOR = os.environ.get("DATE_VALIDATOR", r"[\d]{2}/[\d]{2}/[\d]{4}")