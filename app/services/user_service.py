# app/services/user_service.py
from sqlalchemy.orm import Session
from app.schema.models import User
from log.log import logger
from app.schema.user_schema import UserCreate, UserUpdate
from typing import Optional, List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user_data: UserCreate) -> User:
    logger.debug("Creating user with username=%s", user_data.username)
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(
        name=user_data.name,
        username=user_data.username,
        password=hashed_pw
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info("User created with ID=%d", new_user.id)
    return new_user

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    logger.debug("Querying user by ID=%d", user_id)
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str) -> Optional[User]:
    logger.debug("Querying user by username=%s", username)
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session) -> List[User]:
    logger.debug("Retrieving all users")
    return db.query(User).all()

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    logger.debug("Updating user ID=%d", user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error("User ID=%d not found (update failed)", user_id)
        return None

    if user_data.name is not None:
        user.name = user_data.name
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.password is not None:
        user.password = get_password_hash(user_data.password)

    db.commit()
    db.refresh(user)
    logger.info("User ID=%d updated successfully", user_id)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    logger.debug("Deleting user ID=%d", user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error("User ID=%d not found (delete failed)", user_id)
        return False

    db.delete(user)
    db.commit()
    logger.info("User ID=%d deleted successfully", user_id)
    return True