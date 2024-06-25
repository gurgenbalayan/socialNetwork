# generated by fastapi-codegen:
#   filename:  openapi.json
#   timestamp: 2024-03-23T12:29:33+00:00

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field





class User(BaseModel):
    user_id: str = Field(..., description='Идентификатор пользователя')
    first_name: str = Field(..., description='Имя', example='Имя')
    second_name: str = Field(..., description='Фамилия', example='Фамилия')
    birthdate: date = Field(..., description='Дата рождения', example='2017-02-01')
    biography: Optional[str] = Field(None, description='Интересы', example='Хобби, интересы и т.п.')
    city: Optional[str] = Field(None, description='Город', example='Москва')




class PostText(BaseModel):
    text: str = Field(
        ...,
        description='Текст поста',
        example='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Lectus mauris ultrices eros in cursus turpis massa.',
    )

class PostId(BaseModel):
    text: str = Field(
        ...,
        description='Id поста',
        example='1d535fd6-7521-4cb1-aa6d-031be7123c4d',
    )

class DialogMessageText(BaseModel):
    root: str = Field(
        ..., description='Текст сообщения', example='Привет, как дела?'
    )


class DialogMessage(BaseModel):
    from_: str = Field(..., alias='from')
    to: str
    text: DialogMessageText


class Post(BaseModel):
    author_id: str = Field(..., description='7f03ec11-8a0d-4564-885e-135e8fc4d24c')
    text: str = Field(..., description='тут пост')
    date_post: datetime = Field(..., description='Дата поста', example='2017-02-01')


class LoginPostRequest(BaseModel):
    user_id: str = Field(..., example='e4d2e6b0-cde2-42c5-aac3-0b8316f21e58')
    password: str = Field(..., example='Секретная строка')


class LoginPostResponse(BaseModel):
    token: str = Field(..., example='e4d2e6b0-cde2-42c5-aac3-0b8316f21e58')


class LoginPostResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class LoginPostResponse2(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class UserRegisterPostRequest(BaseModel):
    first_name: str = Field(..., example='Имя')
    second_name: str = Field(..., example='Фамилия')
    birthdate: date = Field(..., description='Дата рождения', example='2017-02-01')
    biography: Optional[str] = Field(None, example='Хобби, интересы и т.п.')
    city: Optional[str] = Field(None, example='Москва')
    password: str = Field(None, example='Секретная строка')


class UserRegisterPostResponse(BaseModel):
    user_id: str = Field(..., example='e4d2e6b0-cde2-42c5-aac3-0b8316f21e58')


class UserRegisterPostResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class UserRegisterPostResponse2(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class UserGetIdGetResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class UserGetIdGetResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class UserSearchGetResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class UserSearchGetResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class FriendSetUserIdPutResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class FriendSetUserIdPutResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class FriendDeleteUserIdPutResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class FriendDeleteUserIdPutResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostCreatePostRequest(BaseModel):
    text: PostText


class PostCreatePostResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostCreatePostResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostUpdatePutRequest(BaseModel):
    id: str
    text: PostText


class PostUpdatePutResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostUpdatePutResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostDeleteIdPutResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostDeleteIdPutResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostGetIdGetResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostGetIdGetResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostFeedGetResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class PostFeedGetResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class DialogUserIdSendPostRequest(BaseModel):
    text: DialogMessageText


class DialogUserIdSendPostResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class DialogUserIdSendPostResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class DialogUserIdListGetResponse(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )


class DialogUserIdListGetResponse1(BaseModel):
    message: str = Field(..., description='Описание ошибки')
    request_id: Optional[str] = Field(
        None,
        description='Идентификатор запроса. Предназначен для более быстрого поиска проблем.',
    )
    code: Optional[int] = Field(
        None,
        description='Код ошибки. Предназначен для классификации проблем и более быстрого решения проблем.',
    )
