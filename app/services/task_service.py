from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repository.task_repository import TaskRepository  
from app.models.task import Task
from app.schema.task_schema import TaskCreate, TaskUpdate
from app.common.enums.user_roles import UserRole
from app.common.constants.log import logger


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repo = TaskRepository(db)
        logger.debug("TaskService initialized with DB session.")

    def create_task(self, task_data: TaskCreate):
        logger.info("Starting task creation process.")
        logger.info("Task title: %s", task_data.title)
        task = Task(**task_data.dict())
        created_task = self.task_repo.create_task(task)
        logger.info("Task created successfully with ID: %d", created_task.id)
        return created_task

    def get_task_by_id(self, task_id: int):
        logger.debug("Fetching task with ID: %d", task_id)
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            logger.warning("Task with ID %d not found", task_id)
        else:
            logger.debug("Task found: %s", task)
        return task

    def get_all_tasks(self):
        logger.debug("Fetching all tasks")
        tasks = self.task_repo.get_all_tasks()
        logger.info("Total tasks retrieved: %d", len(tasks))
        return tasks

    def update_task(self, task_id: int, task_data: dict, current_user):
        logger.info("User %s attempting to update Task ID: %d", current_user.username, task_id)
        task = self.task_repo.get_task_by_id(task_id)
        if not task:
            logger.warning("Task ID %d not found", task_id)
            raise HTTPException(status_code=404, detail="Task not found")

        if current_user.role != UserRole.ADMIN and task.user_id != current_user.id:
            logger.warning("Unauthorized update attempt by User ID %d for Task ID %d", current_user.id, task_id)
            raise HTTPException(status_code=403, detail="You do not have permission to update this task.")

        logger.debug("Updating task with data: %s", task_data)
        updated_task = self.task_repo.update_task(task_id, task_data)
        logger.info("Task ID %d updated successfully by User ID %d", task_id, current_user.id)
        return updated_task

    def delete_task(self, task_id: int) -> bool:
        logger.info("Deleting task ID: %d", task_id)
        if not self.task_repo.delete_task(task_id):
            logger.warning("Task ID %d not found for deletion", task_id)
            raise HTTPException(status_code=404, detail="Task not found")
        logger.info("Task ID %d deleted successfully", task_id)
        return True
