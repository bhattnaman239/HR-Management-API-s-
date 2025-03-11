from fastapi import HTTPException

class UsernameAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Username already exists")


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")


class InvalidUserRoleException(HTTPException):
    def __init__(self, role: str, allowed_roles: list):
        super().__init__(
            status_code=400,
            detail=f"Invalid role: {role}. Allowed roles: {', '.join(allowed_roles)}"
        )


class UserDeletionException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"User with ID {user_id} not found for deletion")


class UserUpdateException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(status_code=404, detail=f"User with ID {user_id} not found for update")


class TaskNotFoundException(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(status_code=404, detail=f"Task with ID {task_id} not found")


class TaskUnauthorizedAccessException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="You do not have permission to update this task.")


class TaskDeletionException(HTTPException):
    def __init__(self, task_id: int):
        super().__init__(status_code=404, detail=f"Task with ID {task_id} not found for deletion")
