# app/schemas/task_schemas.py
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class TaskBase(BaseModel):
    title: str = Field(...)
    description: Optional[str] = Field(None)
    due_date: Optional[date] = Field(None, example="2025-12-31")
    status: str = Field("Pending", example="Pending/Done")


class TaskCreate(TaskBase):
    user_id: int


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Update Title")
    description: Optional[str] = Field(None, example="Update Description")
    due_date: Optional[date] = Field(None, example="2025-12-31")
    status: Optional[str] = Field(None, example="Completed")
    user_id: int
    


class TaskRead(TaskBase):
    id: int
    user_id: int


    class Config:
        from_attributes = True
