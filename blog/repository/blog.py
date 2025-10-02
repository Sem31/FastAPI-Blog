from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import Blog


def get_all(db: Session):
    blogs = db.query(Blog).all()
    return blogs


def create(db: Session, request: Blog):
    new_blog = Blog(title=request.title, body=request.body, user_id=request.user_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def destroy(db: Session, blog_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with id {} not found".format(blog_id),
        )

    blog.delete(synchronize_session=False)
    db.commit()
    return blog


def update(db: Session, blog_id: int, title: str, body: str):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with id {} not found".format(blog_id),
        )

    blog.update({"title": title, "body": body}, synchronize_session=False)
    db.commit()
    return blog


def get_blog(db: Session, blog_id: int):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()

    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Blog with id {} not found".format(blog_id),
        )

    return blog
