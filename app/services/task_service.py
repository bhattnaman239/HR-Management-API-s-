from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.repository.task_repository import TaskRepository  
from app.models.task import Task
from app.schema.task_schema import TaskCreate, TaskUpdate
from app.common.enums.user_roles import UserRole
from app.common.constants.log import logger
from app.common.constants.exceptions import (
    TaskNotFoundException,
    TaskUnauthorizedAccessException,
    TaskDeletionException
)

class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)
        logger.debug("TaskService initialized with DB session.")

    def create_task(self, task_data: TaskCreate):
        logger.info("Starting task creation process.")
        logger.info(f"Task title: {task_data.title}")
        task = Task(**task_data.dict())
        task.created_at = date.today()
        created_task = self.task_repo.create_task(task)
        logger.info(f"Task created successfully with ID: {created_task.id}")
        return created_task

    def get_task_by_id(self, task_id: int):
        logger.debug(f"Fetching task with ID: {task_id}")
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Task with ID {task_id} not found")
            raise TaskNotFoundException(task_id)
        logger.debug(f"Task found: {task}")
        return task

    def get_all_tasks(self):
        logger.debug("Fetching all tasks")
        tasks = self.task_repo.get_all_tasks()
        logger.info(f"Total tasks retrieved: {len(tasks)}")
        return tasks

    def update_task(self, task_id: int, task_data: dict, current_user):
        logger.info(f"User {current_user.username} attempting to update Task ID: {task_id}")
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Task ID {task_id} not found")
            raise TaskNotFoundException(task_id)

        if current_user.role != UserRole.ADMIN and task.user_id != current_user.id:
            logger.warning(f"Unauthorized update attempt by User ID {current_user.id} for Task ID {task_id}")
            raise TaskUnauthorizedAccessException()
        
        for key, value in task_data.items():
            setattr(task, key, value)
        

        logger.debug(f"Updating task with data: {task_data}")
        logger.info(f"Task ID {task_id} updated successfully by User ID {current_user.id}")
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        logger.info(f"Deleting task ID: {task_id}")
        if not self.task_repo.delete_task(task_id):
            logger.warning(f"Task ID {task_id} not found for deletion")
            raise TaskDeletionException(task_id)
        logger.info(f"Task ID {task_id} deleted successfully")
        return True
