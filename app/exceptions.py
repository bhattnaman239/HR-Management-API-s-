from fastapi import HTTPException

class TaskNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Task not found")


class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")
