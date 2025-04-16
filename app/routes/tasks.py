
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_role, require_valid_token
from app.schema.task_schema import TaskCreate, TaskUpdate, TaskRead
from app.services.task_service import TaskService
from app.common.enums.user_roles import UserRole
from app.common.constants.log import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead,
    dependencies=[Depends(require_valid_token), Depends(require_role([UserRole.USER, UserRole.ADMIN]))]
)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Only OTP-verified Admins and regular Users may create tasks.
    (Service logic should verify that a User can only create tasks for themselves.)
    """
    service = TaskService(db)
    return service.create_task(task_data)

@router.get("/", response_model=List[TaskRead],
    dependencies=[Depends(require_valid_token)]
)
def get_tasks(db: Session = Depends(get_db)):
    """
    All OTP-verified users (Admins, Users, Readers) may view tasks.
    """
    service = TaskService(db)
    return service.get_all_tasks()

@router.get("/{task_id}", response_model=TaskRead,
    dependencies=[Depends(require_valid_token)]
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """
    All OTP-verified users may view a specific task.
    """
    service = TaskService(db)
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead,
    dependencies=[Depends(require_valid_token), Depends(require_role([UserRole.USER, UserRole.ADMIN]))]
)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Only OTP-verified Admins and Users can update tasks.
    For Users, the service should ensure that they can only update their own tasks.
    """
    service = TaskService(db)
    updated_task = service.update_task(task_id, task_data.dict(), current_user)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}",
    dependencies=[Depends(require_valid_token), Depends(require_role([UserRole.ADMIN]))]
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """
    Only an OTP-verified Admin may delete a task.
    """
    service = TaskService(db)
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}
