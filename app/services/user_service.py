from fastapi import HTTPException   
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.repository.user_repository import UserRepository 
from app.models.user import User
from app.schema.user_schema import UserCreate, UserUpdate
from app.common.enums.user_roles import UserRole
from app.common.constants.log import logger

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
        logger.info("Starting user creation process for username: %s", user_data.username)
        if self.user_repo.get_user_by_username(user_data.username):
            logger.warning("User creation failed: Username %s already exists", user_data.username)
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = self.hash_password(user_data.password)
        normalized_role = user_data.role.lower() if user_data.role else UserRole.USER.value
        logger.debug("Normalized role: %s", normalized_role)

        if normalized_role not in [role.value for role in UserRole]:
            logger.error("Invalid role provided: %s", user_data.role)
            raise HTTPException(
                status_code=400,
                detail=f"Invalid role: {user_data.role}. Allowed roles: {', '.join(role.value for role in UserRole)}"
            )

        user = User(
            name=user_data.name,
            username=user_data.username,
            password=hashed_password,
            role=user_data.role if user_data.role else UserRole.USER
        )
        created_user = self.user_repo.create_user(user)
        logger.info("User created successfully with ID: %d, Role: %s", created_user.id, created_user.role)
        return created_user

    def get_user_by_username(self, username: str):
        logger.debug("Fetching user by username: %s", username)
        user = self.user_repo.get_user_by_username(username)
        if not user:
            logger.warning("User '%s' not found", username)
        else:
            logger.info("User '%s' found with ID: %d", username, user.id)
        return user

    def get_user_by_id(self, user_id: int):
        logger.debug("Fetching user with ID: %d", user_id)
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            logger.warning("User with ID %d not found", user_id)
        else:
            logger.info("User with ID %d found", user_id)
        return user

    def get_all_users(self):
        logger.debug("Fetching all users")
        users = self.user_repo.get_all_users()
        logger.info("Total users retrieved: %d", len(users))
        return users

    def update_user(self, user_id: int, user_data: UserUpdate):
        logger.info("Updating user ID: %d", user_id)
        updated_user = self.user_repo.update_user(user_id, user_data)
        if not updated_user:
            logger.warning("User ID %d not found for update", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        logger.info("User ID %d updated successfully", user_id)
        return updated_user

    def delete_user(self, user_id: int) -> bool:
        logger.info("Deleting user ID: %d", user_id)
        if not self.user_repo.delete_user(user_id):
            logger.warning("User ID %d not found for deletion", user_id)
            raise HTTPException(status_code=404, detail="User not found")
        logger.info("User ID %d deleted successfully", user_id)
        return True

    def create_test_admin(self):
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
            role=UserRole.ADMIN
        )
        self.db.add(test_admin)
        self.db.commit()
        logger.info("Test admin user created: %s", test_username)
        return test_admin