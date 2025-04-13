from fastapi import HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.repository.user_repository import UserRepository 
from app.models.user import User
from app.schema.user_schema import UserCreate, UserUpdate
from app.common.enums.user_roles import UserRole
from app.common.constants.log import logger
from datetime import datetime
from app.common.constants.exceptions import (
    UsernameAlreadyExistsException, 
    UserNotFoundException, 
    UserDeletionException,
    UserUpdateException
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        logger.debug("UserService initialized with DB session.")

    def hash_password(self, password: str) -> str:
        logger.debug("Hashing password")
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        logger.debug("Verifying password")
        return pwd_context.verify(plain_password, hashed_password)

    def create_user(self, user_data: UserCreate):
        logger.info(f"Starting user creation process for username: {user_data.username}")

        if self.user_repo.get_user_by_username(user_data.username):
            logger.warning(f"User creation failed: Username {user_data.username} already exists")
            raise UsernameAlreadyExistsException()

        if user_data.phone_number and self.user_repo.get_user_by_phone(user_data.phone_number):
            logger.warning(f"User creation failed: Phone number {user_data.phone_number} already in use")
            raise HTTPException(status_code=400, detail="Phone number already in use")
    
        if self.user_repo.get_user_by_email(user_data.email):
            logger.warning(f"User creation failed: Email {user_data.email} already in use")
            raise HTTPException(status_code=400, detail="Email already in use")

        hashed_password = self.hash_password(user_data.password)
    # Explicitly convert the role and log what is being inserted
        role_input = user_data.role or "USER"
        try:
            role_value = UserRole.from_string(role_input)
        except Exception as exc:
            logger.error("Failed to convert role '%s': %s", role_input, exc)
            role_value = UserRole.READER
        logger.debug("Final role to be saved: %s", role_value)

        role_value = UserRole.from_string(user_data.role) if user_data.role else UserRole.USER
        user = User(
        name=user_data.name,
        username=user_data.username,
        password=hashed_password,
            role=role_value,
            phone_number=user_data.phone_number,
            address=user_data.address,
            email=user_data.email
            )
        created_user = self.user_repo.create_user(user)
        logger.info(f"User created successfully with ID: {created_user.id}, Role: {created_user.role}")
        return created_user




    def get_user_by_username(self, username: str):
        logger.debug(f"Fetching user by username: {username}" )
        user = self.user_repo.get_user_by_username(username)
        if not user:
            logger.warning(f"User {username} not found")
            raise UserNotFoundException()
        logger.info(f"User {username} found with ID: {user.id}")
        return user

    def get_user_by_id(self, user_id: int):
        logger.debug(f"Fetching user with ID: {user_id}")
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            logger.warning(f"User with ID {user_id} not found")
            raise UserNotFoundException()
        logger.info(f"User with ID {user_id} found")
        return user

    def get_all_users(self):
        logger.debug("Fetching all users")
        users = self.user_repo.get_all_users()
        logger.info(f"Total users retrieved: {len(users)}")
        return users

    def update_user(self, user_id: int, user_data: UserUpdate):
        logger.info(f"Updating user ID: {user_id}")
        updated_user = self.user_repo.update_user(user_id, user_data)
        if not updated_user:
            logger.warning(f"User ID {user_id} not found for update")
            raise UserUpdateException(user_id)
        logger.info(f"User ID {user_id} updated successfully")
        return updated_user

    def delete_user(self, user_id: int) -> bool:
        logger.info(f"Deleting user ID: {user_id}")
        if not self.user_repo.delete_user(user_id):
            logger.warning(f"User ID {user_id} not found for deletion")
            raise UserDeletionException(user_id)
        logger.info(f"User ID {user_id} deleted successfully")
        return True

    def create_test_admin(self):
        logger.info("Entered create_test_admin()")
        test_username = "admin_test"    
        test_password = "Test@1234"
        if self.user_repo.get_user_by_username(test_username):
            logger.info("Test admin user already exists. Skipping creation.")
            return
        logger.info("Creating test admin user...")
        hashed_password = self.hash_password(test_password)
        test_admin = User(
            name="Test Admin",
            username=test_username,
            password=hashed_password,
            role=UserRole.ADMIN,
            created_at=datetime.utcnow(),  # explicitly setting created_at
            phone_number="9810000000",
            address="Greater Noida, India"
            # email="narjcky1234@gmail.com"     
            )
        self.db.add(test_admin)
        self.db.commit()
        logger.info(f"Test admin user created: {test_username}")
        return test_admin
    