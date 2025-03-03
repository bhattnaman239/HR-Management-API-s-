# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from log.log import logger

from app.repos.database import SessionLocal
from app.services import user_service
from app.schema.user_schema import (
    UserCreate,
    UserUpdate,
    UserRead
)

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.debug("Request to create user with username=%s", user.username)
    existing_user = user_service.get_user_by_username(db, user.username)
    if existing_user:
        logger.warning("Attempted to create user with existing username=%s", user.username)
        raise HTTPException(status_code=400, detail="Username already exists.")
    created_user = user_service.create_user(db, user)
    return created_user

@router.get("/", response_model=List[UserRead])
def read_users(db: Session = Depends(get_db)):
    logger.debug("Fetching all users")
    users = user_service.get_all_users(db)
    logger.info("Fetched %d users", len(users))
    return users

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    logger.debug("Fetching user ID=%d", user_id)
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        logger.error("User ID=%d not found", user_id)
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user_route(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    logger.debug("Request to update user ID=%d with data=%s", user_id, user_data.dict())
    updated_user = user_service.update_user(db, user_id, user_data)
    if not updated_user:
        logger.error("User ID=%d not found (update failed)", user_id)
        raise HTTPException(status_code=404, detail="User not found.")
    return updated_user

@router.delete("/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db)):
    logger.debug("Request to delete user ID=%d", user_id)
    success = user_service.delete_user(db, user_id)
    if not success:
        logger.error("User ID=%d not found (delete failed)", user_id)
        raise HTTPException(status_code=404, detail="User not found.")
    logger.info("User ID=%d deleted successfully", user_id)
    return {"message": f"User {user_id} deleted successfully."}