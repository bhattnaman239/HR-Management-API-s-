
from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user_schema import UserCreate
from app.common.enums.user_roles import UserRole
from app.repository.user_repository import UserRepository
from app.common.constants.log import logger
from app.utils.security import AuthUtils, get_password_hash, verify_password  # Import here
from fastapi import HTTPException
class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        logger.debug("AuthService initialized with DB session.")

    def authenticate_user(self, username: str, password: str):
        user = self.user_repo.get_user_by_username(username)
        if not user:
            logger.warning(f"User {username} not found for authentication.")
            return None
        if not verify_password(password, user.password):
            logger.warning(f"Incorrect password for user {username}.")
            return None
        logger.info(f"User {username} authenticated successfully.")
        return user

    def create_access_token(self, data: dict, expires_delta):
        token = AuthUtils.create_access_token(data, expires_delta)
        logger.debug(f"Access token created for user: {data.get('sub')}")
        return token

    def create_user(self, user_data: UserCreate) -> User:
        if self.user_repo.get_user_by_username(user_data.username):
            raise HTTPException(status_code=400, detail="Username already exists")
        if self.user_repo.get_user_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists")
        
        hashed_password = get_password_hash(user_data.password)
        
        user = User(
            name=user_data.name,
            username=user_data.username,
            password=hashed_password,
            email=user_data.email,
            phone_number=user_data.phone_number,
            address=user_data.address,
            role=user_data.role,
            is_verified=False 
        )
        return self.user_repo.create_user(user)

    def get_user_by_username(self, username: str) -> User:
        user = self.user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
