from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user
from app.services import task_service
from app.schema.task_schema import TaskCreate, TaskUpdate, TaskRead
from log.log import logger  

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskRead)
def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new task (only authenticated users)."""
    logger.info("User %s is creating a new task", current_user.username)
    task = task_service.create_task(db, task_data)
    logger.info("Task created successfully with ID: %d", task.id)
    return task

@router.get("/", response_model=List[TaskRead])
def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks (public endpoint)."""
    logger.debug("Fetching all tasks")
    tasks = task_service.get_all_tasks(db)
    logger.info("Total tasks retrieved: %d", len(tasks))
    return tasks

@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single task by ID (public endpoint)."""
    logger.debug("Fetching task with ID: %d", task_id)
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
    current_user: dict = Depends(get_current_user)
):
    """Update task details (only authenticated users)."""
    logger.info("User %s is updating task ID: %d", current_user.username, task_id)
    updated_task = task_service.update_task(db, task_id, task_data)
    if not updated_task:
        logger.warning("Task with ID %d not found for update", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info("Task ID %d updated successfully", task_id)
    return updated_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete a task (only authenticated users)."""
    logger.info("User %s is deleting task ID: %d", current_user.username, task_id)
    if not task_service.delete_task(db, task_id):
        logger.warning("Task with ID %d not found for deletion", task_id)
        raise HTTPException(status_code=404, detail="Task not found")
    logger.info("Task ID %d deleted successfully", task_id)
    return {"message": f"Task {task_id} deleted successfully"}
