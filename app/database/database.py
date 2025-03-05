import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from app.models.base import Base
from app.models.user import User
from app.models.task import Task
from app.common.constants.log.log import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DB_PATH = os.path.join(BASE_DIR, "database.db")  

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

logger.info(f"Initializing database engine with URL: {SQLALCHEMY_DATABASE_URL}")

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    logger.info("Database engine initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing database engine: {e}")
    raise

try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("SessionLocal created successfully.")
except Exception as e:
    logger.error(f"Error creating SessionLocal: {e}")
    raise
