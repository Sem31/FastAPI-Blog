from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import LoginSchema
from models import User
from hashing import Hash

router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post("/login")
def login(request: LoginSchema, db: Session = Depends(get_db)):
    # Here you would add your authentication logic
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Incorrect password")

    return user
