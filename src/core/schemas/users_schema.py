from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


class UserInfo(BaseModel):
    id: int
    name: str
    followers: List[User]
    following: List[User]


# Основная схема ответа
class UserInfoResponse(BaseModel):
    result: bool
    user: UserInfo | None
