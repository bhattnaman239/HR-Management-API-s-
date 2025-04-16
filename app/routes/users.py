
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_role, require_valid_token
from app.schema.user_schema import UserCreate, UserRead, UserUpdate
from app.services.user_service import UserService
from app.common.enums.user_roles import UserRole
from app.common.constants.log import logger

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserRead],
    dependencies=[Depends(require_valid_token), Depends(require_role([UserRole.ADMIN, UserRole.READER]))])
def get_users(db: Session = Depends(get_db)):
    """
    Only Admins and Readers can view all users.
    """
    service = UserService(db)
    return service.get_all_users()

@router.get("/{user_id}", response_model=UserRead,
    dependencies=[Depends(require_valid_token)]
)
def get_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Allow an admin or reader to view any user.
    A regular user may view only their own record.
    """
    service = UserService(db)
    user = service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.role == UserRole.USER and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this user")
    return user

@router.post("/", response_model=UserRead,
    dependencies=[Depends(require_valid_token), Depends(require_role([UserRole.ADMIN]))]
)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Only an OTP-verified Admin may create a new user.
    """
    service = UserService(db)
    return service.create_user(user_data)

@router.put("/{user_id}", response_model=UserRead,
    dependencies=[Depends(require_valid_token), Depends(require_role([UserRole.ADMIN]))]
)
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    """
    Only an OTP-verified Admin can update a user's data.
    """
    service = UserService(db)
    return service.update_user(user_id, user_data)

@router.delete("/{user_id}",
    dependencies=[Depends(require_valid_token), Depends(require_role([UserRole.ADMIN]))]
)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Only an OTP-verified Admin can delete a user.
    """
    service = UserService(db)
    if not service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": f"User {user_id} deleted successfully"}
