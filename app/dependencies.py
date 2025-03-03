# app/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from log.log import logger

from app.repos.database import SessionLocal
from app.schema.models import User
from app.services.user_service import get_user_by_username
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Validates the JWT token, returns the current user (db model).
    If invalid, raises 401.
    """
    logger.debug("Validating token: %s", token)
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            logger.warning("Token missing 'sub' field.")
            raise credentials_exception
    except JWTError as e:
        logger.warning("JWT decode error: %s", str(e))
        raise credentials_exception

    user = get_user_by_username(db, username)
    if not user:
        logger.error("No user found with username=%s", username)
        raise credentials_exception
    
    return user
