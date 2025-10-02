from pydantic import BaseModel

# from models import Blog


class BlogSchema(BaseModel):
    title: str
    body: str


class ShowBlogSchema(BaseModel):
    title: str

    class Config:
        orm_mode = True
