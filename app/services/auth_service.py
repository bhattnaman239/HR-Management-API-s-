from sqlalchemy.orm import Session
from app.services.user_service import get_user_by_username, verify_password
from app.utils.security import create_access_token
from app.common.constants.log.log import logger

def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate user by verifying credentials.
    """
    logger.info("Authenticating user: {username}")
    user = get_user_by_username(db, username)
    
    if not user:
        logger.warning(f"Authentication failed: User {username} not found")
        return None
    
    if not verify_password(password, user.password):
        logger.warning(f"Authentication failed: Incorrect password for user {username}")
        return None
    
    logger.info(f"User {username} authenticated successfully")
    return user
