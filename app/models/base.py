# models/base.py
from sqlalchemy.ext.declarative import declarative_base
from app.common.constants.log.log import logger

Base = declarative_base()
logger.info("Base class initialized successfully.")