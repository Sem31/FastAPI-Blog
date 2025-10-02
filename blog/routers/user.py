from typing import List

from fastapi import APIRouter, status, Depends, Response, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import UserSchema, ShowUserSchema
from hashing import Hash
from repository import user as repository_user
from oauth2 import get_current_user


router = APIRouter(tags=["User"], prefix="/api/v1")


@router.post(
    "/user",
    response_model=ShowUserSchema,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    request: UserSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return repository_user.create(db, request)


@router.get(
    "/user/{user_id}",
    response_model=ShowUserSchema,
    status_code=status.HTTP_201_CREATED,
)
def get_user(
    user_id=int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return repository_user.get_user(db, user_id)


@router.get(
    "/user",
    # response_model=List[ShowUserSchema],
    status_code=status.HTTP_201_CREATED,
)
def get_user_list(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return repository_user.get_all(db)


@router.delete(
    "/user/{user_id}",
    status_code=status.HTTP_201_CREATED,
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return repository_user.destroy(db, user_id)
