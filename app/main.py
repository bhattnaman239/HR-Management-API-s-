import uvicorn
from fastapi import FastAPI
from log.log import logger
from app.database.database import Base, engine
from app.routes.users import router as user_router
from app.routes.tasks import router as task_router
from app.routes.auth import router as auth_router 

# Create all tables if they don't exist
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


if __name__ == "__main__":
    logger.debug("Launching Uvicorn server from main.py...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)