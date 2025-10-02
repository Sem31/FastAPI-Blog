from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import Base, Blog, User
from schemas import BlogSchema, ShowBlogSchema, UserSchema, ShowUserSchema
from database import engine, get_db

from hashing import Hash

app = FastAPI()


Base.metadata.create_all(engine)


class BlogCreation(BaseModel):
    title: str
    body: str


@app.post(
    "/blog",
    status_code=status.HTTP_201_CREATED,
    tags=["Blog"],
)
def create(request: BlogSchema, db: Session = Depends(get_db)):
    new_blog = Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": new_blog, "Message": "Blog created"}


@app.get(
    "/blog",
    status_code=status.HTTP_200_OK,
    tags=["Blog"],
)
def get_blog_list(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return {"data": blogs}


@app.get(
    "/blog/{blog_id}",
    status_code=status.HTTP_200_OK,
    tags=["Blog"],
)
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


@app.delete(
    "/blog/{blog_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Blog"],
)
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


@app.put(
    "/blog/{blog_id}",
    status_code=status.HTTP_200_OK,
    tags=["Blog"],
)
def update_blog(
    blog_id: int,
    request: BlogSchema,
    response: Response,
    db: Session = Depends(get_db),
    tags=["Blog"],
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
    tags=["Blog"],
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
    tags=["Blog"],
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


@app.post(
    "/user",
    response_model=ShowUserSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
)
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get(
    "/user/{user_id}",
    response_model=ShowUserSchema,
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
)
def get_user(user_id=int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id {} not found".format(user_id),
        )
    return user


@app.get(
    "/user",
    response_model=List[ShowUserSchema],
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
)
def get_user_list(db: Session = Depends(get_db)):
    user = db.query(User).all()
    return user


@app.delete(
    "/user/{user_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["User"],
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id {} not found".format(user_id),
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"data": "User with id {} deleted successfully".format(user_id)}
