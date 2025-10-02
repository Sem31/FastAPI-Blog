from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import LoginSchema, Token
from models import User
from hashing import Hash
from generate_token import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Authentication"], prefix="/auth")


@router.post("/login")
def login(request: LoginSchema, db: Session = Depends(get_db)):
    # Here you would add your authentication logic
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=404, detail="Invalid credentials")

    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=404, detail="Incorrect password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
