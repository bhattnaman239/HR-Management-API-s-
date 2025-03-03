from datetime import datetime, timedelta
from jose import jwt
from app.config import settings
from log.log import logger  

def create_access_token(data: dict, expires_delta: timedelta):
    """
    Create a JWT access token with an expiration.
    """
    logger.info("Generating JWT access token for user: %s", data.get("sub", "unknown"))
    
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info("JWT token created successfully, expires at: %s", expire)
        return encoded_jwt
    except Exception as e:
        logger.error("Error generating JWT token: %s", str(e))
        return None
