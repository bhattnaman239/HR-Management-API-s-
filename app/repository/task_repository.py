from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.task import Task
from app.schema.task_schema import TaskCreate, TaskUpdate
from app.common.constants.log.log import logger

class TaskRepository:
    def __init__(self, db: Session):
        """
        Pass in a SQLAlchemy Session when creating an instance.
        """
        self.db = db

    def create_task(self, task: Task) -> Task:
        """Insert a new task into the database."""
        logger.info(f"Creating a new task with title: {task.title}")
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        logger.info(f"Task created successfully with ID: {task.id}")
        return task

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by ID."""
        logger.debug("Fetching task with ID: %d", task_id)
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if task:
            logger.info("Task found: ID %d", task_id)
        else:
            logger.warning("Task with ID %d not found", task_id)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks."""
        logger.debug("Fetching all tasks from the database.")
        tasks = self.db.query(Task).all()
        logger.info("Total tasks retrieved: %d", len(tasks))
        return tasks

    def update_task(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        """Update a task's details."""
        logger.info("Updating task with ID: %d", task_id)
        task = self.get_task_by_id(task_id)
        if not task:
            logger.warning("Task with ID %d not found for update", task_id)
            return None

        if hasattr(task_data, "dict"):
            updates = task_data.dict(exclude_unset=True)
        else:
            updates = task_data

        for key, value in updates.items():
            setattr(task, key, value)

        self.db.commit()
        self.db.refresh(task)
        logger.info("Task with ID %d updated successfully", task_id)
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task from the database."""
        logger.info("Deleting task with ID: %d", task_id)
        task = self.get_task_by_id(task_id)
        if not task:
            logger.warning("Task with ID %d not found for deletion", task_id)
            return False

        self.db.delete(task)
        self.db.commit()
        logger.info("Task with ID %d deleted successfully", task_id)
        return True
