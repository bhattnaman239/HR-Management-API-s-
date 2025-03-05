from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_role
from app.services import user_service
from app.schema.user_schema import UserCreate, UserUpdate, UserRead
from app.common.enums.user_roles import UserRole
from app.common.constants.log.log import logger

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201, dependencies=[Depends(require_role([UserRole.ADMIN]))])
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Admin can create a new user."""
    logger.info("Admin creating a new user: %s", user_data.username)
    return user_service.create_user(db, user_data)

@router.get("/", response_model=List[UserRead], dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.READER]))])
def get_users(db: Session = Depends(get_db)):
    """Admins & Readers can get all users."""
    logger.info("Fetching all users")
    return user_service.get_all_users(db)

@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.READER]))])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Admins & Readers can get a user by ID."""
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        logger.warning("User with ID %d not found", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead, dependencies=[Depends(require_role([UserRole.ADMIN]))])
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Only Admins can update users."""
    logger.info("Admin updating user ID: %d", user_id)
    updated_user = user_service.update_user(db, user_id, user_data)
    if not updated_user:
        logger.warning("User with ID %d not found for update", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", dependencies=[Depends(require_role([UserRole.ADMIN]))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Only Admins can delete users."""
    logger.info("Admin deleting user ID: %d", user_id)
    if not user_service.delete_user(db, user_id):
        logger.warning("User with ID %d not found for deletion", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted successfully"}

