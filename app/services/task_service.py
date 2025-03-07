from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.task_repository import TaskRepository  # <--- IMPORT CLASS
from app.models.task import Task
from app.schema.task_schema import TaskCreate, TaskUpdate
from app.common.enums.user_roles import UserRole
from app.common.constants.log.log import logger

def create_task(db: Session, task_data: TaskCreate):
    """Business logic for creating a task."""
    logger.info(f"Creating new task: {task_data.title}")
    task = Task(**task_data.dict())

    task_repo = TaskRepository(db)

    created_task = task_repo.create_task(task) 
    logger.info("Task created successfully with ID: %d", created_task.id)
    return created_task

def get_task_by_id(db: Session, task_id: int):
    """Get a single task by ID."""
    logger.debug("Fetching task with ID: %d", task_id)

    task_repo = TaskRepository(db)
    task = task_repo.get_task_by_id(task_id)   

    if not task:
        logger.warning("Task with ID %d not found", task_id)
    return task

def get_all_tasks(db: Session):
    """Get all tasks."""
    logger.debug("Fetching all tasks")

    task_repo = TaskRepository(db)
    tasks = task_repo.get_all_tasks()           

    logger.info("Total tasks retrieved: %d", len(tasks))
    return tasks

def update_task(db: Session, task_id: int, task_data: dict, current_user):
    """Update a task only if the user owns it or is an Admin."""
    logger.info(f"User {current_user.username} attempting to update Task ID: {task_id}")

    task_repo = TaskRepository(db)
    task = task_repo.get_task_by_id(task_id)     
    if not task:
        logger.warning("Task ID %d not found", task_id)
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role != UserRole.ADMIN and task.user_id != current_user.id:
        logger.warning("Unauthorized attempt by User ID %d to update Task ID %d", current_user.id, task_id)
        raise HTTPException(status_code=403, detail="You do not have permission to update this task.")

    updated_task = task_repo.update_task(task_id, task_data)  
    logger.info("Task ID %d updated successfully by User ID %d", task_id, current_user.id)
    return updated_task

def delete_task(db: Session, task_id: int) -> bool:
    """Handle task deletion."""
    logger.info("Deleting task ID: %d", task_id)

    task_repo = TaskRepository(db)
    if not task_repo.delete_task(task_id):        
        logger.warning("Task ID %d not found for deletion", task_id)
        return False

    logger.info("Task ID %d deleted successfully", task_id)
    return True
