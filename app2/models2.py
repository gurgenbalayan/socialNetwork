# generated by fastapi-codegen:
#   filename:  openapi.json
#   timestamp: 2024-03-23T12:29:33+00:00

from __future__ import annotations

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field





class DialogMessageText(BaseModel):
    root: str = Field(
        ..., description='Текст сообщения', example='Привет, как дела?'
    )


class DialogMessage(BaseModel):
    who: str = Field(..., description='7f03ec11-8a0d-4564-885e-135e8fc4d24c')
    text: str = Field(..., description='тут сообщение')
    date_message: datetime = Field(..., description='Дата сообщения', example='2017-02-01')





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