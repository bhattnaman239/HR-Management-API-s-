from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.user import User
from app.schema.user_schema import UserCreate, UserUpdate
from app.common.constants.log import logger


class UserRepository:
    def __init__(self, db: Session):
        """
        Pass in a SQLAlchemy Session when creating an instance.
        """
        self.db = db

    def create_user(self, user: User) -> User:
        """Insert a new user into the database."""
        logger.info(f"Creating a new user with username: {user.username}")
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        logger.info("User created successfully with ID: %d", user.id)
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        logger.debug("Fetching user with ID: %d", user_id)
        user = self.db.query(User).filter(User.id == user_id).first()
        if user:
            logger.info("User found: ID %d", user_id)
        else:
            logger.warning("User with ID %d not found", user_id)
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username."""
        logger.debug(f"Fetching user with username: {username}")
        user = self.db.query(User).filter(User.username == username).first()
        if user:
            logger.info(f"User found: Username {username}")
        else:
            logger.warning(f"User with username {username} not found")
        return user

    def get_all_users(self) -> List[User]:
        """Retrieve all users."""
        logger.debug("Fetching all users from the database.")
        users = self.db.query(User).all()
        logger.info("Total users retrieved: %d", len(users))
        return users

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user details."""
        logger.info("Updating user with ID: %d", user_id)
        user = self.get_user_by_id(user_id)
        if not user:
            logger.warning("User with ID %d not found for update", user_id)
            return None

        updates = user_data.dict(exclude_unset=True)
        for key, value in updates.items():
            setattr(user, key, value)

        self.db.commit()
        self.db.refresh(user)
        logger.info("User with ID %d updated successfully", user_id)
        return user

    def delete_user(self, user_id: int) -> bool:
        """Delete a user from the database."""
        logger.info("Deleting user with ID: %d", user_id)
        user = self.get_user_by_id(user_id)
        if not user:
            logger.warning("User with ID %d not found for deletion", user_id)
            return False

        self.db.delete(user)
        self.db.commit()
        logger.info("User with ID %d deleted successfully", user_id)
        return True
