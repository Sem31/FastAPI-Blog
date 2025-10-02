from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models import User
from hashing import Hash


def get_all(db: Session):
    users = db.query(User).all()
    return users


def create(db: Session, request: User):
    hashed_password = Hash.bcrypt(request.password)
    new_user = User(name=request.name, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def destroy(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id)

    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id {} not found".format(user_id),
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"data": "User with id {} deleted successfully".format(user_id)}


def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with id {} not found".format(user_id),
        )
    return user
