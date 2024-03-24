from datetime import timedelta, datetime
from typing import Optional
from config import load_config
import jwt




def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    to_encode = data.copy()
    cfg_token = load_config(section='token')
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=cfg_token.access_token_expire_min)

    to_encode.update({'exp': expire})
    return jwt.encode(payload=to_encode, key=cfg_token['key'], algorithm=cfg_token['algorithm'])