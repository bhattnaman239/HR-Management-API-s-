from pydantic import BaseModel, Field, validator
from datetime import date, timedelta,timezone, datetime
from typing import Optional

india_tz = timezone(timedelta(hours=5, minutes=30))

class TaskBase(BaseModel):
    title: str = Field(..., example="New Task")
    description: Optional[str] = Field(None)
    due_date: Optional[date] = Field(None, example="2025-12-31")
    status: str = Field("Pending", example="Pending/Done")

class TaskCreate(TaskBase):
    user_id: int

    @validator('due_date')
    def due_date_must_be_future(cls, v):
        if v is not None and v <= date.today():
            raise ValueError("Due date must be greater than today's date.")
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Update Title")
    description: Optional[str] = Field(None, example="Update Description")
    due_date: Optional[date] = Field(None, example="2025-12-31")
    status: Optional[str] = Field(None, example="Completed")
    @validator('due_date')
    def due_date_must_be_future(cls, v):
        if v is not None and v <= date.today():
            raise ValueError("Due date must be greater than today's date.")
        return v

class TaskRead(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.astimezone(india_tz).strftime("%d-%m-%Y")
        }