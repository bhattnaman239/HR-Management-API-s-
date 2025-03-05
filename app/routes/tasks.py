from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, require_role
from app.services import task_service
from app.schema.task_schema import TaskCreate, TaskUpdate, TaskRead
from app.common.enums.user_roles import UserRole
from app.common.constants.log.log import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead, dependencies=[Depends(require_role([UserRole.USER, UserRole.ADMIN]))])
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Users and Admins can create tasks."""
    logger.info("Creating task: %s", task_data.title)
    return task_service.create_task(db, task_data)

@router.get("/", response_model=List[TaskRead], dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.READER, UserRole.USER]))])
def get_tasks(db: Session = Depends(get_db)):
    """All users can view tasks."""
    logger.info("Fetching all tasks")
    return task_service.get_all_tasks(db)

@router.get("/{task_id}", response_model=TaskRead, dependencies=[Depends(require_role([UserRole.ADMIN, UserRole.READER, UserRole.USER]))])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """All users can get task by ID."""
    task = task_service.get_task_by_id(db, task_id)
    if not task:
        logger.warning("Task with ID %d not found", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, 
    task_data: TaskUpdate, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    """Users can update only their own tasks; Admins can update any task."""
    logger.info("User %s attempting to update Task ID: %d", current_user.username, task_id)
    updated_task = task_service.update_task(db, task_id, task_data.dict(), current_user)
    if not updated_task:
        logger.warning("Task with ID %d not found for update", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/{task_id}", dependencies=[Depends(require_role([UserRole.ADMIN]))])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Only Admins can delete tasks."""
    logger.info("Admin deleting task ID: %d", task_id)
    if not task_service.delete_task(db, task_id):
        logger.warning("Task ID %d not found for deletion", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": f"Task {task_id} deleted successfully"}
