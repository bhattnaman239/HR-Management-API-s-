# models/task.py
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=True)
    status = Column(String, nullable=False, default="Pending")

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
