from typing import List
from pydantic import BaseModel

# from models import Blog


class BlogSchema(BaseModel):
    title: str
    body: str
    user_id: int


class UserBlogSchema(BaseModel):
    title: str
    body: str


class ShowUserSchema(BaseModel):
    name: str
    email: str
    blogs: List[UserBlogSchema] = []

    class Config:
        orm_mode = True


class ShowBlogSchema(BaseModel):
    title: str
    body: str
    creator: ShowUserSchema

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class LoginSchema(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str | None = None
