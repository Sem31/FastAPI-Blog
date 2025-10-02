from pydantic import BaseModel

# from models import Blog


class BlogSchema(BaseModel):
    title: str
    body: str


class ShowBlogSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    name: str
    email: str
    password: str


class ShowUserSchema(BaseModel):
    name: str
    email: str

    class Config:
        orm_mode = True
