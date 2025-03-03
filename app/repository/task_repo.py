from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.task import Task
from app.schema.task_schema import TaskCreate, TaskUpdate
from log.log import logger

def create_task(db: Session, task: Task) -> Task:
    """Insert a new task into the database."""
    logger.info("Creating a new task with title: %s", task.title)
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info("Task created successfully with ID: %d", task.id)
    return task

def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    """Retrieve a task by ID."""
    logger.debug("Fetching task with ID: %d", task_id)
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        logger.info("Task found: ID %d", task_id)
    else:
        logger.warning("Task with ID %d not found", task_id)
    return task

def get_all_tasks(db: Session) -> List[Task]:
    """Retrieve all tasks."""
    logger.debug("Fetching all tasks from the database.")
    tasks = db.query(Task).all()
    logger.info("Total tasks retrieved: %d", len(tasks))
    return tasks

def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
    """Update a task's details."""
    logger.info("Updating task with ID: %d", task_id)
    task = get_task_by_id(db, task_id)
    if not task:
        logger.warning("Task with ID %d not found for update", task_id)
        return None

    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    
    db.commit()
    db.refresh(task)
    logger.info("Task with ID %d updated successfully", task_id)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task from the database."""
    logger.info("Deleting task with ID: %d", task_id)
    task = get_task_by_id(db, task_id)
    if not task:
        logger.warning("Task with ID %d not found for deletion", task_id)
        return False

    db.delete(task)
    db.commit()
    logger.info("Task with ID %d deleted successfully", task_id)
    return True