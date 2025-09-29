from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}


@app.get("/blog/{blog_id}")
def get_blog(blog_id: int):
    return {"data": "Blog with id: {}".format(blog_id)}


@app.get("/blog/{blog_id}/comments")
def comments(blog_id: int):
    return {"data": "Blog with id: {} comment".format(blog_id)}


@app.get("/about")
def about():
    return {"data": "About data page"}


class Blog(BaseModel):
    title: str
    body: str
    published: bool = False


@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": "Blog is created with title {}".format(blog.title)}
