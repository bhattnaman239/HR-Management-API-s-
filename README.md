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

## 🔑 **Authentication & Authorization**
This API follows a **Role-Based Access Control (RBAC)** system.

| **Action**                 | **Admin** | **User** | **Reader** |
|----------------------------|----------|----------|------------|
| ✅ **Create Users**        | ✅ Yes    | ❌ No    | ❌ No      |
| 🔍 **Get All Users**       | ✅ Yes    | ❌ No    | ✅ Yes     |
| 🔍 **Get User by ID**      | ✅ Yes    | ❌ No    | ✅ Yes     |
| ✏ **Update User**         | ✅ Yes    | ❌ No    | ❌ No      |
| ❌ **Delete User**         | ✅ Yes    | ❌ No    | ❌ No      |
| ✅ **Create Tasks**        | ✅ Yes    | ✅ Yes   | ❌ No      |
| 🔍 **Get All Tasks**       | ✅ Yes    | ✅ Yes   | ✅ Yes     |
| 🔍 **Get Task by ID**      | ✅ Yes    | ✅ Yes   | ✅ Yes     |
| ✏ **Update Tasks**        | ✅ Yes (Any Task) | ✅ Yes (Only Own Tasks) | ❌ No |
| ❌ **Delete Tasks**        | ✅ Yes    | ❌ No    | ❌ No      |

---

## 🔧 **Installation & Setup**

```
🔹 1️⃣ Clone the Repository
git clone https://github.com/your-username/task-user-management-api.git
cd task-user-management-api

🔹 2️⃣ Create a Virtual Environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

🔹 3️⃣ Install Dependencies
pip install -r requirements.txt

🔹 4️⃣ Set Up Environment Variables
SECRET_KEY="supersecretkey"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

🔹 5️⃣ Run the FastAPI Server
uvicorn app.main:app --reload
```
