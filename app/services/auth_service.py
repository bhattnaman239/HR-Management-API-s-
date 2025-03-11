from sqlalchemy.orm import Session
from app.services.user_service import UserService  
from app.utils.security import AuthUtils
from app.common.constants.log import logger


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_service = UserService(db)  
        logger.debug("AuthService initialized with DB session.")

    def authenticate_user(self, username: str, password: str):
        """
        Authenticate user by verifying credentials.
        """
        logger.info("Authenticating user: %s", username)
        user = self.user_service.get_user_by_username(username)  
        
        if not user:
            logger.warning("Authentication failed: User %s not found", username)
            return None

        if not self.user_service.verify_password(password, user.password):  
            logger.warning("Authentication failed: Incorrect password for user %s", username)
            return None

        logger.info("User %s authenticated successfully", username)
        return user

    def create_access_token(self, data: dict, expires_delta):
        """
        Create a JWT access token using the provided data and expiration delta.
        """
        token = AuthUtils.create_access_token(data, expires_delta)
        logger.debug("Access token created for user: %s", data.get("sub"))
        return token
