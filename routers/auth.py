from datetime import timedelta

import models
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from schemas import Token
from sqlalchemy.orm import Session
from utils import verify

router = APIRouter(tags=["Authentification"])


@router.post("/login", response_model=Token)
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(
        models.User.email == credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    verified = verify(credentials.password, user.password)

    if not verified:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token}
