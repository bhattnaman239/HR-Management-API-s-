from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.repository.user_repository import UserRepository  
from app.models.user import User
from app.schema.user_schema import UserCreate, UserUpdate
from app.common.enums.user_roles import UserRole
from app.common.constants.log.log import logger

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
    logger.info(f"Creating new user: {user_data.username}")

    user_repo = UserRepository(db)

    if user_repo.get_user_by_username(user_data.username):
        logger.warning(f"User creation failed: Username {user_data.username} already exists")
        raise ValueError("Username already exists")

    hashed_password = hash_password(user_data.password)
    normalized_role = user_data.role.lower() if user_data.role else UserRole.USER.value

    if normalized_role not in [role.value for role in UserRole]:
        raise ValueError(
            f"Invalid role: {user_data.role}. "
            f"Allowed roles: {', '.join(role.value for role in UserRole)}"
        )

    user = User(
        name=user_data.name,
        username=user_data.username,
        password=hashed_password,
        role=user_data.role if user_data.role else UserRole.USER
    )

    # Create user in DB
    created_user = user_repo.create_user(user)
    logger.info(f"User created successfully with ID: {created_user.id}, Role: {created_user.role}")
    return created_user

def get_user_by_username(db: Session, username: str):
    """Fetch user by username from the database."""
    logger.debug(f"Fetching user by username: {username}")

    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(username)
    if not user:
        logger.warning(f"User {username} not found")
    return user

def get_user_by_id(db: Session, user_id: int):
    """Get a single user by ID."""
    logger.debug(f"Fetching user with ID: {user_id}")

    user_repo = UserRepository(db)
    user = user_repo.get_user_by_id(user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
    return user

def get_all_users(db: Session):
    """Get all users."""
    logger.debug("Fetching all users")

    user_repo = UserRepository(db)
    users = user_repo.get_all_users()
    logger.info(f"Total users retrieved: {len(users)}")
    return users

def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """Validate and update user details."""
    logger.info(f"Updating user ID: {user_id}")

    user_repo = UserRepository(db)
    updated_user = user_repo.update_user(user_id, user_data)
    if not updated_user:
        logger.warning(f"User ID {user_id} not found for update")
    else:
        logger.info(f"User ID {user_id} updated successfully")
    return updated_user

def delete_user(db: Session, user_id: int) -> bool:
    """Handle user deletion."""
    logger.info(f"Deleting user ID: {user_id}")

    user_repo = UserRepository(db)
    if not user_repo.delete_user(user_id):
        logger.warning(f"User ID {user_id} not found for deletion")
        return False

    logger.info(f"User ID {user_id} deleted successfully")
    return True

def create_test_admin(db: Session):
    """
    Create a test admin user with a hardcoded username/password.
    If the user already exists, skip creation.
    """
    test_username = "admin_test"
    test_password = "Test@1234"

    user_repo = UserRepository(db)
    existing_user = user_repo.get_user_by_username(test_username)
    if existing_user:
        logger.info("Test admin user already exists. Skipping creation.")
        return

    logger.info("Creating test admin user...")

    hashed_password = hash_password(test_password)
    test_admin = User(
        name="Test Admin",
        username=test_username,
        password=hashed_password,
        role=UserRole.ADMIN
    )
    db.add(test_admin)
    db.commit()
    logger.info(f"Test admin user created: {test_username}")