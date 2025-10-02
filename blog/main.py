from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Base, Blog
from schemas import BlogSchema, ShowBlogSchema
from database import engine, get_db

app = FastAPI()


Base.metadata.create_all(engine)


class BlogCreation(BaseModel):
    title: str
    body: str


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog, "Message": "Blog created"}


@app.get("/blog", status_code=status.HTTP_200_OK)
def get_blog_list(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return {"data": blogs}


@app.get("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def get_blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with id {} not found".format(blog_id),
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"Message": "Blog with id {} not found".format(blog_id)}
    return {"data": blog}


@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with id {} not found".format(blog_id),
        )

    blog.delete(synchronize_session=False)
    db.commit()
    return {"data": "Blog with id {} deleted successfully".format(blog_id)}


@app.put("/blog/{blog_id}", status_code=status.HTTP_200_OK)
def update_blog(
    blog_id: int,
    request: BlogSchema,
    response: Response,
    db: Session = Depends(get_db),
):
    blog = db.query(Blog).filter(Blog.id == blog_id)

    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with id {} not found".format(blog_id),
        )

    blog.update(
        {"title": request.title, "body": request.body}, synchronize_session=False
    )
    db.commit()
    return {"data": "Blog with id {} update successfully".format(blog_id)}


@app.get(
    "/show/blog/{blog_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBlogSchema,
)
def show_blog(blog_id: int, db: Session = Depends(get_db)):
    """Show blog by id, using response model to filter the response data.

    Args:
        blog_id (int): Blog object id
        db (Session, optional): Database Session. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with id {} not found".format(blog_id),
        )
    return blog


@app.get(
    "/show/blog",
    status_code=status.HTTP_200_OK,
    response_model=List[ShowBlogSchema],
)
def show_all_blog(db: Session = Depends(get_db)):
    """Show blog by id, using response model to filter the response data.

    Args:
        blog_id (int): Blog object id
        db (Session, optional): Database Session. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    blog = db.query(Blog).all()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with id {} not found".format(blog_id),
        )
    return blog
