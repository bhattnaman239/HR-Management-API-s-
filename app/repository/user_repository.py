from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user_schema import UserCreate, UserUpdate
from typing import Optional, List
from app.common.constants.log.log import logger

def create_user(db: Session, user: User) -> User:
    """Insert a new user into the database."""
    logger.info("Creating a new user with username: %s", user.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info("User created successfully with ID: %d", user.id)
    return user

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by ID."""
    logger.debug("Fetching user with ID: %d", user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        logger.info("User found: ID %d", user_id)
    else:
        logger.warning("User with ID %d not found", user_id)
    return user

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Retrieve a user by username."""
    logger.debug("Fetching user with username: %s", username)
    user = db.query(User).filter(User.username == username).first()
    if user:
        logger.info("User found: Username %s", username)
    else:
        logger.warning("User with username %s not found", username)
    return user

def get_all_users(db: Session) -> List[User]:
    """Retrieve all users."""
    logger.debug("Fetching all users from the database.")
    users = db.query(User).all()
    logger.info("Total users retrieved: %d", len(users))
    return users

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """Update user details."""
    logger.info("Updating user with ID: %d", user_id)
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning("User with ID %d not found for update", user_id)
        return None
    
    for key, value in user_data.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    logger.info("User with ID %d updated successfully", user_id)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user from the database."""
    logger.info("Deleting user with ID: %d", user_id)
    user = get_user_by_id(db, user_id)
    if not user:
        logger.warning("User with ID %d not found for deletion", user_id)
        return False
    
    db.delete(user)
    db.commit()
    logger.info("User with ID %d deleted successfully", user_id)
    return True
