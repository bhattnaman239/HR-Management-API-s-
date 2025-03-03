# app/services/task_service.py
from sqlalchemy.orm import Session
from typing import Optional, List
from log.log import logger

from app.schema.models import Task, User
from app.schema.task_schema import TaskCreate, TaskUpdate

def create_task(db: Session, task_data: TaskCreate) -> Task:
    logger.debug("Creating task with title=%s for user_id=%d", task_data.title, task_data.user_id)

    owner = db.query(User).filter(User.id == task_data.user_id).first()
    if not owner:
        logger.error("User with ID=%d does not exist. Cannot create task.", task_data.user_id)
        raise ValueError(f"User with ID={task_data.user_id} does not exist")

    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        due_date=task_data.due_date,
        status=task_data.status,
        user_id=task_data.user_id 
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    logger.info("Task created with ID=%d for user_id=%d", new_task.id, task_data.user_id)
    return new_task

def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    logger.debug("Fetching task ID=%d", task_id)
    return db.query(Task).filter(Task.id == task_id).first()

def get_all_tasks(db: Session) -> List[Task]:
    logger.debug("Retrieving all tasks")
    return db.query(Task).all()

def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
    logger.debug("Updating task ID=%d", task_id)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.error("Task ID=%d not found. Update failed.", task_id)
        return None

    if task_data.title is not None:
        task.title = task_data.title
    if task_data.description is not None:
        task.description = task_data.description
    if task_data.due_date is not None:
        task.due_date = task_data.due_date
    if task_data.status is not None:
        task.status = task_data.status
    if task_data.user_id is not None:
        owner = db.query(User).filter(User.id == task_data.user_id).first()
        if not owner:
            logger.error("User with ID=%d does not exist. Cannot reassign task.", task_data.user_id)
            raise ValueError(f"User ID={task_data.user_id} not found for reassignment.")
        task.user_id = task_data.user_id

    db.commit()
    db.refresh(task)
    logger.info("Task ID=%d updated successfully", task_id)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    logger.debug("Deleting task ID=%d", task_id)
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        logger.error("Task ID=%d not found. Delete failed.", task_id)
        return False
    db.delete(task)
    db.commit()
    logger.info("Task ID=%d deleted successfully", task_id)
    return True