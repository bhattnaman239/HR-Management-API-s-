from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from app.config import settings
from app.common.constants.log import logger

class AuthUtils:
    """Utility class for authentication-related operations."""
    @staticmethod
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash the provided password using bcrypt.
    """
    logger.debug("Hashing password")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
