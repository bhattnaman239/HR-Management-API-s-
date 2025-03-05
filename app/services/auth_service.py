from sqlalchemy.orm import Session
from app.services.user_service import get_user_by_username, verify_password
from app.utils.security import create_access_token
from app.common.constants.log.log import logger

def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate user by verifying credentials.
    """
    logger.info("Authenticating user: %s", username)
    user = get_user_by_username(db, username)
    
    if not user:
        logger.warning("Authentication failed: User %s not found", username)
        return None
    
    if not verify_password(password, user.password):
        logger.warning("Authentication failed: Incorrect password for user %s", username)
        return None
    
    logger.info("User %s authenticated successfully", username)
    return user
