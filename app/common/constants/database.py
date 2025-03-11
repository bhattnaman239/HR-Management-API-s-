import os

# Base Directory (Points to `app/`)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# Database Directory (Inside `database/`)
DATABASE_DIR = os.path.join(BASE_DIR, "database")

# Define Database Path
DB_PATH = os.path.join(DATABASE_DIR, "database.db")  
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

from app.common.constants.log import logger
logger.info(f"Initializing database engine with URL: {SQLALCHEMY_DATABASE_URL}")
