import uvicorn
from fastapi import FastAPI
from app.common.constants.log import logger

from app.database.database import Base, engine, SessionLocal
from app.routes.users import router as user_router
from app.routes.tasks import router as task_router
from app.routes.auth import router as auth_router
from app.services.user_service import UserService 

# Create all tables if they don't exist
logger.info("Creating database tables if they don't exist...")
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task & User Management API",
    description="A simple CRUD API for tasks and users",
    version="1.0.0",
)

logger.info("Starting the Task & User Management API...")

# Include Routers
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(task_router)

@app.on_event("startup")
def initialize_test_user():
    """Create a hardcoded test admin user on server startup."""
    db = SessionLocal()
    user_service = UserService(db) 
    try:
        user_service.create_test_admin()  
    except Exception as e:
        logger.error(f"Error creating test admin user: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    logger.debug("Launching Uvicorn server from main.py...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
