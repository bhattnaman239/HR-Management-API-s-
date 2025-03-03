import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from app.models.base import Base
from app.models.user import User
from app.models.task import Task
from log.log import logger 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DB_PATH = os.path.join(BASE_DIR, "database.db")  

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

logger.info("Initializing database engine with URL: %s", SQLALCHEMY_DATABASE_URL)

try:
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    logger.info("Database engine initialized successfully.")
except Exception as e:
    logger.error("Error initializing database engine: %s", e)
    raise

try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("SessionLocal created successfully.")
except Exception as e:
    logger.error("Error creating SessionLocal: %s", e)
    raise
