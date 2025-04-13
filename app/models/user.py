# # models/user.py
# from sqlalchemy import Column, Integer, String, Enum
# from sqlalchemy.orm import relationship
# from .base import Base
# from app.common.enums.user_roles import UserRole


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     username = Column(String, unique=True, index=True, nullable=False)
#     password = Column(String, nullable=False)
#     role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
#     tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

    # created_at = Column(String, nullable=False)
    # updated_at = Column(String, nullable=True)
    # email = Column(String, nullable=True)
    # phone_number = Column(String, nullable=True)
    # address = Column(String, nullable=True)


#2nd
# # models/user.py

# from sqlalchemy import Column, Integer, String, Enum, DateTime
# from sqlalchemy.orm import relationship
# from datetime import datetime
# from .base import Base
# from app.common.enums.user_roles import UserRole

# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, nullable=False)
#     username = Column(String, unique=True, index=True, nullable=False)
#     password = Column(String, nullable=False)
#     role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    
#     # New Timestamp fields:
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = Column(DateTime, default=None, onupdate=datetime.utcnow, nullable=True)

#     tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


from sqlalchemy import Column, Integer, String, Enum, DateTime, func
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
        # Use server_default for the database to automatically set the timestamp.
        created_at = Column(DateTime, server_default=func.now(), nullable=False)
        updated_at = Column(DateTime, server_default=None, onupdate=func.now(), nullable=True)
        phone_number = Column(String, unique=True, nullable=True)
        address = Column(String, nullable=True)
        # email = Column(String, unique=True, nullable=False, index=True)
        email = Column(String, unique=True, nullable=False, index=True)
        tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")