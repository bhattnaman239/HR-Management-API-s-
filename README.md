Task & User Management API
This project provides a FastAPI application that allows you to create, read, update, and delete both Users and Tasks, with a SQLite database under the hood. It also includes:

*JWT-based authentication to ensure only verified users can modify data.
*Logging via Python’s logging module (outputs both to console and a log file).
*Layered architecture (routes → services → database/models → schemas).
*Pydantic models for request/response validation.
*.env usage for storing secrets like SECRET_KEY.

Features
1. User Management
Create, list, get by ID, update, and delete users.
Passwords are stored hashed using passlib.

2. Task Management
Create, list, get by ID, update, and delete tasks.
Each task is associated with a user (user_id).

3. Authentication
Users obtain a JWT token by sending their username/password to /auth/login.
Bearer token is required to perform actions on tasks (and can be required for user endpoints if desired).

4. Logging
Detailed logs are written to console and app.log (as configured in log/log.py).

5. Database
SQLite database by default (in the data/ folder).
ORM powered by SQLAlchemy.

API/
├── .env                 # Holds environment variables (SECRET_KEY, etc.)
├── .gitignore           # Lists files/folders to exclude from version control
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── config.py        # Loads settings from .env (or pydantic-settings)
│   ├── database.py      # SQLAlchemy engine, SessionLocal, Base
│   ├── models.py        # SQLAlchemy models (User, Task)
│   ├── routes/
│   │   ├── auth.py      # /auth endpoints (login)
│   │   ├── tasks.py     # /tasks endpoints
│   │   └── users.py     # /users endpoints
│   ├── schema/
│   │   ├── user_schema.py  # Pydantic schemas for User
│   │   └── task_schema.py  # Pydantic schemas for Task
│   ├── services/
│   │   ├── user_service.py # Business logic for users
│   │   └── task_service.py # Business logic for tasks
│   └── dependencies.py  # get_current_user(), etc.
├── data/
│   └── database.db      # SQLite database file (ignored in .gitignore if desired)
├── log/
│   └── log.py           # Logging configuration
├── requirements.txt     # Python dependencies
└── README.md            # This file
