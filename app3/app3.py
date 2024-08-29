
from __future__ import annotations

import datetime
from typing import List, Union
from uuid import uuid4

from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI, HTTPException,Depends

from auth_bearer import JWTBearer
from db3 import add_read, add_unread
from utils.security import decodeJWT
import logging
from asgi_correlation_id import CorrelationIdMiddleware
from loguru import logger
import sys
def configure_logging():
    from asgi_correlation_id.context import correlation_id

    def correlation_id_filter(record):
        record['correlation_id'] = correlation_id.get()
        return record['correlation_id']

    logger.remove()
    fmt = "{level}: \t  {time} {name}:{line} [{correlation_id}] - {message}"
    logger.add(sys.stderr, format=fmt, level=logging.DEBUG, filter=correlation_id_filter)


app3 = FastAPI(
    on_startup=[configure_logging],
    title='OTUS Highload Architect',
    version='1.3.0')
app3.add_middleware(
    CorrelationIdMiddleware,
    header_name='X-Request-ID',
    update_request_header=True,
    generator=lambda: uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a,
)

@app3.get('/')
def index():

    logger.info('Log with correlation ID')
    #return {'request_id': get_request_id()}

@app3.post(
    '/dialog/v2/{user_id}/add_unread', dependencies=[Depends(JWTBearer())],
    response_model=str,
)
def get_dialog_user_chat_create(
    user_id: str, token: str = Depends(JWTBearer())
):
    my_id = decodeJWT(token)['sub']
    date = datetime.datetime.now()
    data = add_unread(my_id, user_id,date)
    return data



@app3.post(
    '/dialog/v2/{user_id}/add_read',dependencies=[Depends(JWTBearer())],
    response_model=str,
)
def post_dialog_user_add_read(
    user_id: str, token: str = Depends(JWTBearer())
):
    sender = decodeJWT(token)['sub']
    date = datetime.datetime.now()
    data = add_read(sender, user_id, date)
    return data

