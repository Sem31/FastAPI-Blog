from typing import List

from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import UserSchema, ShowUserSchema
from hashing import Hash


router = APIRouter(tags=["User"], prefix="/api/v1")


@router.post(
    "/user",
    response_model=ShowUserSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_user(request: UserSchema, db: Session = Depends(get_db)):
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/user/{user_id}",
    response_model=ShowUserSchema,
    status_code=status.HTTP_201_CREATED,
)
def get_user(user_id=int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id {} not found".format(user_id),
        )
    return user


@router.get(
    "/user",
    # response_model=List[ShowUserSchema],
    status_code=status.HTTP_201_CREATED,
)
def get_user_list(db: Session = Depends(get_db)):
    user = db.query(User).all()
    return user


@router.delete(
    "/user/{user_id}",
    status_code=status.HTTP_201_CREATED,
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
