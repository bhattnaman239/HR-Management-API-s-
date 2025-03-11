from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_role
from app.services.user_service import UserService 
from app.schema.user_schema import UserCreate, UserUpdate, UserRead
from app.common.enums.user_roles import UserRole
from app.common.constants.log import logger


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201, dependencies=[Depends(require_role([UserRole.ADMIN]))])
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Admin can create a new user."""
    logger.info("Admin creating a new user: %s", user_data.username)
    service = UserService(db)
    return service.create_user(user_data)

@router.get("/", response_model=List[UserRead], dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.READER]))])
def get_users(db: Session = Depends(get_db)):
    """Admins & Readers can get all users."""
    logger.info("Fetching all users")
    service = UserService(db)
    return service.get_all_users()

@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.READER]))])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Admins & Readers can get a user by ID."""
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        logger.warning("User with ID %d not found", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserRead, dependencies=[Depends(require_role([UserRole.ADMIN]))])
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """Only Admins can update users."""
    logger.info("Admin updating user ID: %d", user_id)
    service = UserService(db)
    updated_user = service.update_user(user_id, user_data)
    if not updated_user:
        logger.warning("User with ID %d not found for update", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", dependencies=[Depends(require_role([UserRole.ADMIN]))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Only Admins can delete users."""
    logger.info("Admin deleting user ID: %d", user_id)
    service = UserService(db)
    if not service.delete_user(user_id):
        logger.warning("User with ID %d not found for deletion", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted successfully"}
