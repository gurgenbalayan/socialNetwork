from datetime import timedelta, datetime
from typing import Optional
from config import load_config
import jwt
import time



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()
    cfg_token = load_config(section='token')
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=cfg_token.access_token_expire_min)

    to_encode.update({'exp': expire})
    return jwt.encode(payload=to_encode, key=cfg_token['key'], algorithm=cfg_token['algorithm'])

def decodeJWT(token: str) -> dict:
    cfg_token = load_config(section='token')
    try:
        decoded_token = jwt.decode(token, cfg_token['key'], algorithms=cfg_token['algorithm'])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}