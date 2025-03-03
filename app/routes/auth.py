# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta, datetime
from jose import jwt, JWTError

from log.log import logger

from app.repos.database import SessionLocal
from app.services.user_service import get_user_by_username, verify_password
from app.schema.models import User
from app.schema.user_schema import UserRead
from app.config import settings

router = APIRouter(prefix="/auth", tags=["authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/login")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Expects form data: 'username' and 'password'.
    Returns a JWT access token if valid credentials.
    """
    logger.debug("Login attempt for username=%s", form_data.username)
    
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        logger.warning("Invalid credentials for username=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},  
        expires_delta=access_token_expires
    )
    logger.info("User '%s' logged in successfully", user.username)
    return {"access_token": access_token, "token_type": "bearer"}

def create_access_token(data: dict, expires_delta: timedelta):
    """
    Create a JWT access token with an expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt