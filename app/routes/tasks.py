from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from log.log import logger

from app.repos.database import SessionLocal
from app.services import task_service
from app.schema.task_schema import TaskCreate, TaskUpdate, TaskRead
from app.dependencies import get_current_user, get_db
from app.schema.models import User

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
def create_task(
    task_data: TaskCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    logger.debug("User '%s' creating task titled='%s'", current_user.username, task_data.title)
    try:
        new_task = task_service.create_task(db, task_data)
        return new_task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TaskRead])
def read_tasks(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    logger.debug("User '%s' fetching all tasks", current_user.username)
    tasks = task_service.get_all_tasks(db)
    logger.info("Fetched %d tasks", len(tasks))
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = task_service.get_task_by_id(db, task_id)
    if not task:
        logger.error("Task ID=%d not found", task_id)
        raise HTTPException(status_code=404, detail="Task not found.")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, 
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.debug("User '%s' updating task ID=%d", current_user.username, task_id)
    try:
        updated_task = task_service.update_task(db, task_id, task_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return updated_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.debug("User '%s' deleting task ID=%d", current_user.username, task_id)
    success = task_service.delete_task(db, task_id)
    if not success:
        logger.error("Task ID=%d not found (delete failed)", task_id)
        raise HTTPException(status_code=404, detail="Task not found.")
    logger.info("Task ID=%d deleted successfully", task_id)
    return {"message": f"Task {task_id} deleted successfully."}