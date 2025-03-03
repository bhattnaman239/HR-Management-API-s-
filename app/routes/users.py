from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user
from app.services import user_service
from app.schema.user_schema import UserCreate, UserUpdate, UserRead
from log.log import logger  

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create a new user (no authentication required)."""
    logger.info("Creating a new user with username: %s", user_data.username)
    user = user_service.create_user(db, user_data)
    logger.info("User created successfully with ID: %d", user.id)
    return user

@router.get("/", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    """Get all users (public endpoint)."""
    logger.debug("Fetching all users")
    users = user_service.get_all_users(db)
    logger.info("Total users retrieved: %d", len(users))
    return users

@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a single user by ID (public endpoint)."""
    logger.debug("Fetching user with ID: %d", user_id)
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        logger.warning("User with ID %d not found", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update user details (only authenticated users)."""
    logger.info("User %s is updating user ID: %d", current_user.username, user_id)
    updated_user = user_service.update_user(db, user_id, user_data)
    if not updated_user:
        logger.warning("User with ID %d not found for update", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("User ID %d updated successfully", user_id)
    return updated_user

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a user (only authenticated users)."""
    logger.info("User %s is deleting user ID: %d", current_user.username, user_id)
    if not user_service.delete_user(db, user_id):
        logger.warning("User with ID %d not found for deletion", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("User ID %d deleted successfully", user_id)
    return {"message": f"User {user_id} deleted successfully"}
