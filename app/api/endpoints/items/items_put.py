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
