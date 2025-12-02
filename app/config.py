from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database Configuration (Replace with your actual database URL)
DATABASE_URL = "postgresql://postgres:postpass@localhost:5432/ConIFA"
SECRET_KEY = "sfA3xnmOUcavj3c87sTf6vA1RIEHTT6V3zFg2OMBWljHXJ9qoQ"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# SQLAlchemy Engine and Session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Security Dependencies
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

origins = [
   "http://localhost:3000",  # The origin of your React app
   "http://localhost:8000",  # Maybe allow the backend itself
   # Add other origins as needed (e.g., for production)
]
