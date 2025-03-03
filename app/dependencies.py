from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime

from log.log import logger
from app.database.database import SessionLocal
from app.models.user import User  # ✅ Corrected Import
from app.services.user_service import get_user_by_username
from app.config import settings

# OAuth2 scheme for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_db():
    """Dependency to get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Validates JWT token, returns the current user.
    If token is invalid or expired, raises 401 Unauthorized.
    """
    logger.debug("Validating JWT token...")

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token. Please login again.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        expire = payload.get("exp")

        if username is None:
            logger.warning("JWT token is missing 'sub' field.")
            raise credentials_exception

        # Check if the token has expired
        if expire is None or datetime.utcnow() > datetime.utcfromtimestamp(expire):
            logger.warning("JWT token has expired for user=%s", username)
            raise credentials_exception

    except JWTError as e:
        logger.warning("JWT decode error: %s", str(e))
        raise credentials_exception

    # Fetch user from database
    user = get_user_by_username(db, username)
    if not user:
        logger.error("Authentication failed. No user found with username=%s", username)
        raise credentials_exception

    logger.info("Authenticated user: %s", user.username)
    return user
