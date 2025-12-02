from datetime import datetime, timedelta
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, select, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session, relationship, backref

from app.api.schemas.user import UserResponse, UserCreate
from app.config import DATABASE_URL, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, engine, SessionLocal
from app.api.models.models import User, Player
from app.api.schemas.user import Token

import bcrypt
import jwt
import random
import uvicorn

from app.database import get_db, get_current_active_user


router = APIRouter()


# Hashing Function
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


# Token Creation
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Authentication Function
def authenticate_user(db: Session, username: str, password: str):
    user = db.execute(select(User).where(User.username == username)).scalars().first()
    if not user:
        return None
    if bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
        return user
    return None


# API Endpoints
# Auth Endpoints
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["account managing"])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.execute(select(User).where(User.username == user.username)).scalars().first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db_player = Player(
        user_id=new_user.id,
        surname=user.surname,
        name=user.name,
        birthdate=user.birthdate,
        email=user.email,
        phone=user.phone,
    )
    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return new_user


@router.post("/token", response_model=Token, tags=["account managing"])
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserResponse, tags=["player panel"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
