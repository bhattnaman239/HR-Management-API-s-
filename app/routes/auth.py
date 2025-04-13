from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.dependencies import get_db
from app.services.auth_service import AuthService
from app.config import settings
from app.common.constants.log import logger
from app.config import settings

SECRET_KEY = settings.SECRET_KEY  # "supersecretkey"
ALGORITHM = settings.ALGORITHM      # "HS256"

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
    logger.debug(f"Login attempt for username: {form_data.username}" )
    
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        logger.warning(f"Invalid credentials for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token({"sub": user.username}, access_token_expires)
    
    logger.info(f"User {user.username} logged in successfully" )
    return {"access_token": access_token, "token_type": "bearer"}
