
from __future__ import annotations
from prometheus_fastapi_instrumentator import Instrumentator
from typing import List, Union
from uuid import uuid4
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI, HTTPException, Depends
import requests
from auth_bearer import JWTBearer
from models2 import *
from db2 import send_message_tarantool, get_dialog_tarantool, send_message, get_dialog
from utils.security import decodeJWT
import logging
from asgi_correlation_id import CorrelationIdMiddleware
from loguru import logger
import sys
sys.path.insert(0,"../")
from saga_coordinator import execute_saga
import sys
def configure_logging():
    from asgi_correlation_id.context import correlation_id

    def correlation_id_filter(record):
        record['correlation_id'] = correlation_id.get()
        return record['correlation_id']

    logger.remove()
    fmt = "{level}: \t  {time} {name}:{line} [{correlation_id}] - {message}"
    logger.add(sys.stderr, format=fmt, level=logging.DEBUG, filter=correlation_id_filter)


app2 = FastAPI(
    on_startup=[configure_logging],
    title='OTUS Highload Architect',
    version='1.3.0')
app2.add_middleware(
    CorrelationIdMiddleware,
    header_name='X-Request-ID',
    update_request_header=True,
    generator=lambda: uuid4().hex,
    validator=is_valid_uuid4,
    transformer=lambda a: a,
)

@app2.get('/')
def index():

    logger.info('Log with correlation ID')
    #return {'request_id': get_request_id()}

@app2.get(
    '/dialog/v2/{user_id}/list', dependencies=[Depends(JWTBearer())],
    response_model=List[DialogMessage],
    responses={
        '500': {'model': DialogUserIdListGetResponse},
        '503': {'model': DialogUserIdListGetResponse1},
    },
)
def get_dialog_user_id_list(
    user_id: str, token: str = Depends(JWTBearer())
) -> Union[
    List[DialogMessage], DialogUserIdListGetResponse, DialogUserIdListGetResponse1
]:
    my_id = decodeJWT(token)['sub']
    requests.post('http://127.0.0.1:8008/dialog/v2/{}/add_read'.format(user_id),
                  headers={"Content-Type": "application/json",
                           "Authorization": "Bearer {}".format(token)})
    data = get_dialog(my_id, user_id)
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail='Page not found')



@app2.post(
    '/dialog/v2/{user_id}/send',dependencies=[Depends(JWTBearer())],
    response_model=str,
    responses={
        '500': {'model': DialogUserIdSendPostResponse},
        '503': {'model': DialogUserIdSendPostResponse1},
    },
)
def post_dialog_user_id_send(
    user_id: str, token: str = Depends(JWTBearer()), body: DialogUserIdSendPostRequest = None
) -> Union[None, DialogUserIdSendPostResponse, DialogUserIdSendPostResponse1]:
    sender = decodeJWT(token)['sub']
    text = body.text.root
    date = datetime.now()
    if text is None or text == '':
        return 'message cannot be empty'
    else:
#        result=send_message(sender, user_id, text, date)
        result = execute_saga(sender, user_id, text, date)
        return result

Instrumentator().instrument(app2).expose(app2)