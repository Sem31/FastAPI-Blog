from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import BlogSchema, ShowBlogSchema
from repository import blog as blog_repository

router = APIRouter(tags=["Blog"], prefix="/api/v1")

# Define your blog-related routes here and use @router.get, @router.post, etc.


@router.get(
    "/blog",
    status_code=status.HTTP_200_OK,
)
def get_blog_list(db: Session = Depends(get_db)):
    return blog_repository.get_all(db)


@router.post(
    "/blog",
    status_code=status.HTTP_201_CREATED,
)
def create(request: BlogSchema, db: Session = Depends(get_db)):
    return blog_repository.create(db, request)


@router.get(
    "/blog/{blog_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBlogSchema,
)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    return blog_repository.get_blog(db, blog_id)


@router.delete(
    "/blog/{blog_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    return blog_repository.destroy(db, blog_id)


@router.put(
    "/blog/{blog_id}",
    status_code=status.HTTP_200_OK,
)
def update_blog(
    blog_id: int,
    request: BlogSchema,
    db: Session = Depends(get_db),
):
    return blog_repository.update(db, blog_id, request.title, request.body)


@router.get(
    "/show/blog/{blog_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowBlogSchema,
)
def show_blog(blog_id: int, db: Session = Depends(get_db)):
    return blog_repository.get_blog(db, blog_id)


@router.get(
    "/show/blog",
    status_code=status.HTTP_200_OK,
    response_model=List[ShowBlogSchema],
)
def show_all_blog(db: Session = Depends(get_db)):
    return blog_repository.get_all(db)
