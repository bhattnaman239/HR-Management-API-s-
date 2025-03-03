from sqlalchemy.orm import Session
from app.repository import task_repo
from app.models.task import Task
from app.schema.task_schema import TaskCreate, TaskUpdate
from log.log import logger 

def create_task(db: Session, task_data: TaskCreate):
    """Business logic for creating a task."""
    logger.info("Creating new task: %s", task_data.title)
    task = Task(**task_data.dict())
    created_task = task_repo.create_task(db, task)
    logger.info("Task created successfully with ID: %d", created_task.id)
    return created_task

def get_task_by_id(db: Session, task_id: int):
    """Get a single task by ID."""
    logger.debug("Fetching task with ID: %d", task_id)
    task = task_repo.get_task_by_id(db, task_id)
    if not task:
        logger.warning("Task with ID %d not found", task_id)
    return task

def get_all_tasks(db: Session):
    """Get all tasks."""
    logger.debug("Fetching all tasks")
    tasks = task_repo.get_all_tasks(db)
    logger.info("Total tasks retrieved: %d", len(tasks))
    return tasks

def update_task(db: Session, task_id: int, task_data: TaskUpdate):
    """Validate and update task details."""
    logger.info("Updating task ID: %d", task_id)
    updated_task = task_repo.update_task(db, task_id, task_data)
    if not updated_task:
        logger.warning("Task ID %d not found for update", task_id)
    else:
        logger.info("Task ID %d updated successfully", task_id)
    return updated_task

def delete_task(db: Session, task_id: int) -> bool:
    """Handle task deletion."""
    logger.info("Deleting task ID: %d", task_id)
    if not task_repo.delete_task(db, task_id):
        logger.warning("Task ID %d not found for deletion", task_id)
        return False
    logger.info("Task ID %d deleted successfully", task_id)
    return True
