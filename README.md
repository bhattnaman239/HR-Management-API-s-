# Task & User Management API

This project provides a **FastAPI** application that allows you to **create, read, update, and delete** both **Users and Tasks**, with a **SQLite database** under the hood. It also includes:

- **JWT-based authentication** to ensure only verified users can modify data.
- **Logging** via Python’s logging module (outputs both to console and a log file).
- **Layered architecture** (`routes → services → database/models → schemas`).
- **Pydantic models** for request/response validation.
- **`.env` usage** for storing secrets like `SECRET_KEY`.

---

## 🚀 Features

1. **User Management**
   - Create, list, get by ID, update, and delete users.
   - Passwords are securely stored using **Passlib**.

2. **Task Management**
   - Create, list, get by ID, update, and delete tasks.
   - Each task is associated with a user (`user_id`).

3. **Authentication**
   - Users obtain a **JWT token** by sending their username/password to `/auth/login`.
   - Bearer token is required to perform actions on tasks (and can be required for user endpoints if desired).

4. **Logging**
   - **Detailed logs** are written to the console and `app.log` (configured in `log/log.py`).

5. **Database**
   - **SQLite database** by default (in the `data/` folder).
   - **ORM powered by SQLAlchemy**.

---
