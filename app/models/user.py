
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
from app.common.enums.user_roles import UserRole
from app.common.variables.types import UserRoleType
    
class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True, index=True)
        name = Column(String, nullable=False)
        username = Column(String, unique=True, index=True, nullable=False)
        password = Column(String, nullable=False)
        role = Column(UserRoleType, default=UserRole.USER, nullable=False)
        created_at = Column(DateTime, server_default=func.now(), nullable=False)
        updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

        phone_number = Column(String, unique=True, nullable=True)
        address = Column(String, nullable=True)
        email = Column(String, unique=True, nullable=False, index=True)
        tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")
        # edit2.0
        is_verified = Column(Boolean, default=False, nullable=False)