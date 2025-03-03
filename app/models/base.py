# models/base.py
from sqlalchemy.ext.declarative import declarative_base
from log.log import logger

Base = declarative_base()
logger.info("Base class initialized successfully.")