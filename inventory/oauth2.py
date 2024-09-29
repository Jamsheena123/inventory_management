from datetime import datetime, timedelta
import pytz
from rest_framework import exceptions
import jwt










ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM="HS256"
SECRET_KEY="qwertyuiopasdfghjklzxcvbnm"


def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.now(pytz.utc)+timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    print(to_encode)
    print(expire)
    encode_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    print(encode_jwt)
    return encode_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed("Invalid token")