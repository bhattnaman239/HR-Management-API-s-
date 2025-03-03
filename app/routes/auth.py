from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.dependencies import get_db
from app.services.auth_service import authenticate_user, create_access_token
from app.config import settings
from log.log import logger

router = APIRouter(prefix="/auth", tags=["authentication"])

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
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning("Invalid credentials for username=%s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.username}, access_token_expires)
    
    logger.info("User '%s' logged in successfully", user.username)
    return {"access_token": access_token, "token_type": "bearer"}