from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.repository import user_repo
from app.models.user import User
from app.schema.user_schema import UserCreate, UserUpdate
from log.log import logger 

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Encrypt user password before storing."""
    logger.debug("Hashing password")
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify user password using hashing."""
    logger.debug("Verifying password")
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user_data: UserCreate):
    """Business logic for creating a user."""
    logger.info("Creating new user: %s", user_data.username)
    
    if user_repo.get_user_by_username(db, user_data.username):
        logger.warning("User creation failed: Username %s already exists", user_data.username)
        raise ValueError("Username already exists")
    
    hashed_password = hash_password(user_data.password)
    user = User(name=user_data.name, username=user_data.username, password=hashed_password)
    created_user = user_repo.create_user(db, user)
    logger.info("User created successfully with ID: %d", created_user.id)
    return created_user

def get_user_by_username(db: Session, username: str):
    """Fetch user by username from the database."""
    logger.debug("Fetching user by username: %s", username)
    user = user_repo.get_user_by_username(db, username)
    if not user:
        logger.warning("User %s not found", username)
    return user

def get_user_by_id(db: Session, user_id: int):
    """Get a single user by ID."""
    logger.debug("Fetching user with ID: %d", user_id)
    user = user_repo.get_user_by_id(db, user_id)
    if not user:
        logger.warning("User with ID %d not found", user_id)
    return user

def get_all_users(db: Session):
    """Get all users."""
    logger.debug("Fetching all users")
    users = user_repo.get_all_users(db)
    logger.info("Total users retrieved: %d", len(users))
    return users

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """Validate and update user details."""
    logger.info("Updating user ID: %d", user_id)
    updated_user = user_repo.update_user(db, user_id, user_data)
    if not updated_user:
        logger.warning("User ID %d not found for update", user_id)
    else:
        logger.info("User ID %d updated successfully", user_id)
    return updated_user

def delete_user(db: Session, user_id: int) -> bool:
    """Handle user deletion."""
    logger.info("Deleting user ID: %d", user_id)
    if not user_repo.delete_user(db, user_id):
        logger.warning("User ID %d not found for deletion", user_id)
        return False
    logger.info("User ID %d deleted successfully", user_id)
    return True
