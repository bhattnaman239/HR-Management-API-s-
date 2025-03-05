from datetime import datetime, timedelta
from jose import jwt
from app.config import settings
from app.common.constants.log.log import logger

def create_access_token(data: dict, expires_delta: timedelta):
    """
    Create a JWT access token with an expiration.
    """
    logger.info(f"Generating JWT access token for user: {data.get('sub', 'unknown')}")

    
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info(f"JWT token created successfully, expires at: {expire}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error generating JWT token: {str(e)}")
        return None
