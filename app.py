# generated by fastapi-codegen:
#   filename:  openapi.json
#   timestamp: 2024-03-23T12:29:33+00:00

from __future__ import annotations
import pickle
from typing import List, Union

import aio_pika
from fastapi import FastAPI, HTTPException,Depends, Request, WebSocket
from pydantic import confloat
import json
from auth_bearer import JWTBearer
import uuid
from models import *
from db.db import add_user, authenticate_user, get_user_by_id, get_user_by_fs_with_index, get_posts, write_post, \
    get_friends, send_message, get_dialog, send_message_tarantool, get_dialog_tarantool
from utils.hashing import Hasher
from utils.security import create_access_token, decodeJWT
from datetime import timedelta
from db.redis_tools import RedisTools
from config import load_config
from rebuild_cache import rebuild_cache_for_friends


app = FastAPI(
    title='OTUS Highload Architect',
    version='1.2.0',
)

@app.on_event('startup')
async def startup_event() -> None:
    cfg_rabbitmq = load_config(section='rabbitmq')
    url = cfg_rabbitmq['url']
    robust_connecton = await aio_pika.connect_robust(url)
    app.connection = robust_connecton
    async def _confirms_channel():
        return await robust_connecton.channel(publisher_confirms=True)

    async def _transactional_channel():
        return await robust_connecton.channel(publisher_confirms=False)

    app.channel_pool_sub = aio_pika.pool.Pool(_confirms_channel, max_size=10000)
    app.channel_pool_pub = aio_pika.pool.Pool(_confirms_channel, max_size=10000)
    app.channel_pool_pub_tx = aio_pika.pool.Pool(_transactional_channel, max_size=10000)

@app.on_event('shutdown')
async def shutdown_event() -> None:
    await app.channel_pool_sub.close()
    await app.channel_pool_pub.close()
    await app.channel_pool_pub_tx.close()
    await app.connection.close()

@app.websocket("/post/feed/posted")
async def websocket_endpoint(websocket: WebSocket, jwt: str = JWTBearer()):
    await websocket.accept()
    data = await websocket.receive_text()
    data = json.loads(data)
    token = data["token"]
    user_id = decodeJWT(token)['sub']
    if jwt.verify_jwt(token):
        uuid_str = str(uuid.uuid4())
        await websocket.send_text(f"SUCCESS LOGIN")
        cfg_rabbitmq = load_config(section='rabbitmq')
        url = cfg_rabbitmq['url']
        async with app.channel_pool_sub.acquire() as channel:
            await channel.set_qos(prefetch_count=5)
            ex_new_posts = await channel.get_exchange('posts', ensure=False)
            queue = await channel.declare_queue(uuid_str, auto_delete=True)
            await queue.bind(ex_new_posts, routing_key=user_id)
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        await websocket.send_text(message.body)
                        if queue.name in message.body.decode():
                            break

    else:
        await websocket.send_text(f"INVALID TOKEN")
        await websocket.close()



@app.get(
    '/dialog/{user_id}/list', dependencies=[Depends(JWTBearer())],
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
    data = get_dialog_tarantool(my_id, user_id)
    if data:
        return data
    else:
        raise HTTPException(status_code=404, detail='Page not found')



@app.post(
    '/dialog/{user_id}/send',dependencies=[Depends(JWTBearer())],
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
    if text is None or text == '':
        return 'message cannot be empty'
    else:
        result=send_message_tarantool(sender, user_id, text)
        return result


@app.put(
    '/friend/delete/{user_id}',
    response_model=None,
    responses={
        '500': {'model': FriendDeleteUserIdPutResponse},
        '503': {'model': FriendDeleteUserIdPutResponse1},
    },
)
def put_friend_delete_user_id(
    user_id: str,
) -> Union[None, FriendDeleteUserIdPutResponse, FriendDeleteUserIdPutResponse1]:
    pass


@app.put(
    '/friend/set/{user_id}',
    response_model=None,
    responses={
        '500': {'model': FriendSetUserIdPutResponse},
        '503': {'model': FriendSetUserIdPutResponse1},
    },
)
def put_friend_set_user_id(
    user_id: str,
) -> Union[None, FriendSetUserIdPutResponse, FriendSetUserIdPutResponse1]:
    pass


@app.post(
    '/login',
    response_model=LoginPostResponse,
    responses={
        '500': {'model': LoginPostResponse1},
        '503': {'model': LoginPostResponse2},
    },
)
def post_login(
    body: LoginPostRequest,
) -> Union[LoginPostResponse, LoginPostResponse1, LoginPostResponse2]:
    password = body.password
    user_id = body.user_id
    pass_hash = authenticate_user(user_id)
    if not pass_hash:
        raise HTTPException(status_code=401, detail='Incorrect username or password')
    elif Hasher.verify_password(plain_password=password, hashed_password=pass_hash):
        if user_id in RedisTools.get_keys():
            return LoginPostResponse(token=RedisTools.get_value(user_id))
        cfg_token = load_config(section='token')
        access_token_expires = timedelta(minutes=int(cfg_token['access_token_expire_min']))
        access_token = create_access_token(data={'sub': user_id}, expires_delta=access_token_expires)
        RedisTools.set_key(key=user_id, value=access_token)
        return LoginPostResponse(token=access_token)
    else:
        raise HTTPException(status_code=401, detail='Incorrect username or password')




@app.post(
    '/post/create', dependencies=[Depends(JWTBearer())],
    response_model=str,
    responses={
        '500': {'model': PostCreatePostResponse},
        '503': {'model': PostCreatePostResponse1},
    }
)
async def post_post_create(
    request: Request, body: PostText, token: str = Depends(JWTBearer())
) -> Union[str, PostCreatePostResponse, PostCreatePostResponse1]:
    post = body.text
    author_id = decodeJWT(token)['sub']
    post_queue = str({
            "postId": str(uuid.uuid4()),
            "postText": post,
            "author_user_id": author_id
          }
    )
    friends = get_friends(author_id)
    w_post = write_post(author_id, post)
    async with request.app.channel_pool_pub_tx.acquire() as channel:
        ex_new_posts = await channel.get_exchange('posts', ensure=False)
        async with channel.transaction():
            for user_id in friends:
                await ex_new_posts.publish(aio_pika.Message(body=f"{post_queue}".encode()), routing_key=user_id, mandatory=False)
    rebuild_cache_for_friends(author_id)
    if w_post == "success":
        return "success"
    else:
        return "fail"


@app.put(
    '/post/delete/{id}',
    response_model=None,
    responses={
        '500': {'model': PostDeleteIdPutResponse},
        '503': {'model': PostDeleteIdPutResponse1},
    },
)
def put_post_delete_id(
    id: str,
) -> Union[None, PostDeleteIdPutResponse, PostDeleteIdPutResponse1]:
    pass


@app.get(
    '/post/feed', dependencies=[Depends(JWTBearer())],
    response_model=List[Post],
    responses={
        '500': {'model': PostFeedGetResponse},
        '503': {'model': PostFeedGetResponse1},
    },
)
def get_post_feed(token: str = Depends(JWTBearer()),
    offset: Optional[confloat(ge=0.0)] = 0, limit: Optional[confloat(ge=1.0)] = 10
) -> Union[List[Post], PostFeedGetResponse, PostFeedGetResponse1]:
    user_id = decodeJWT(token)['sub']
    if RedisTools.get_value("feed_"+user_id):
        return pickle.loads(RedisTools.get_value("feed_"+user_id))
    data = get_posts(user_id=user_id, limit=limit, offset=offset)
    if data:
        RedisTools.cache_data("feed_"+user_id, bytes(pickle.dumps(data)))
        return data
    else:
        raise HTTPException(status_code=404, detail='Page not found')


@app.get(
    '/post/get/{id}',
    response_model=Post,
    responses={
        '500': {'model': PostGetIdGetResponse},
        '503': {'model': PostGetIdGetResponse1},
    },
)
def get_post_get_id(
    id: str,
) -> Union[Post, PostGetIdGetResponse, PostGetIdGetResponse1]:
    pass


@app.put(
    '/post/update',
    response_model=None,
    responses={
        '500': {'model': PostUpdatePutResponse},
        '503': {'model': PostUpdatePutResponse1},
    },
)
def put_post_update(
    body: PostUpdatePutRequest = None,
) -> Union[None, PostUpdatePutResponse, PostUpdatePutResponse1]:
    pass


@app.get(
    '/user/get/{id}', dependencies=[Depends(JWTBearer())],
    response_model=User,
    responses={
        '500': {'model': UserGetIdGetResponse},
        '503': {'model': UserGetIdGetResponse1},
    },
)
def get_user_get_id(
    user_id: str,
) -> Union[User, UserGetIdGetResponse, UserGetIdGetResponse1]:
    data = get_user_by_id(user_id)
    if data:
        model={'user_id': data[0], 'first_name': data[1], 'second_name': data[2], 'birthdate': data[3], 'biography': data[4], 'city': data[5]}
        return model
    else:
        raise HTTPException(status_code=404, detail='Page not found')


@app.post(
    '/user/register',
    response_model=UserRegisterPostResponse,
    responses={
        '500': {'model': UserRegisterPostResponse1},
        '503': {'model': UserRegisterPostResponse2},
    },
)
def post_user_register(
    body: UserRegisterPostRequest,
) -> Union[
    UserRegisterPostResponse, UserRegisterPostResponse1, UserRegisterPostResponse2
]:
    user_id = str(uuid.uuid4())
    add_user(user_id, body.first_name, body.second_name, body.birthdate, body.biography, body.city, Hasher.get_password_hash(body.password))

    return UserRegisterPostResponse(user_id=user_id)

@app.get(
    '/user/search', dependencies=[Depends(JWTBearer())],
    responses={
        '500': {'model': UserSearchGetResponse},
        '503': {'model': UserSearchGetResponse1},
    },
)
def get_user_search(
    first_name: str, second_name: str
) -> Union[List[User], UserSearchGetResponse, UserSearchGetResponse1]:
    #data = get_user_by_fs_without_index(first_name,second_name)
    data = get_user_by_fs_with_index(first_name, second_name)
    data_list=[]
    if data:
        for user in data:
            model = {'user_id': user[0], 'first_name': user[1], 'second_name': user[2], 'birthdate': user[3],
                     'biography': user[4], 'city': user[5]}
            data_list.append(model)
        return data_list
    else:
        return []
