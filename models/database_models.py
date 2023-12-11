from typing import List
import pydantic
from pydantic import BaseModel


class User(BaseModel):
    name: str
    surname: str
    patronymic: str
    email: str
    password: str


class Service(BaseModel):
    name: str
    description: str
    cost: str


class News(BaseModel):
    name: str
    description: str


class Request(BaseModel):
    id_user: str | None
    id_service: str
    user_fullname: str
    phone_number: str