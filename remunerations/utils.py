import datetime
from jwt import encode, decode, ExpiredSignatureError, InvalidSignatureError
from decouple import config
    
def expire_date(days: int):
    now = datetime.datetime.now()
    new_date = now + datetime.timedelta(days)
    return new_date

def write_token(data: dict):
    token = encode(payload={**data, 'exp': expire_date(int(config('EXPIRE_DATE'))) }, key=config('SECRET_KEY'), algorithm='HS256')
    return token.encode('UTF-8')