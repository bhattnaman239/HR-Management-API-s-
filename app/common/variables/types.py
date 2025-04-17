# app/common/types.py
from sqlalchemy.types import TypeDecorator, String
from app.common.enums.user_roles import UserRole

class UserRoleType(TypeDecorator):
    """
    Custom type for UserRole enum that converts values to uppercase strings
    when binding parameters and uses `UserRole.from_string` on result values.
    """
    impl = String

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, UserRole):
            return value.value  
        if isinstance(value, str):
            return value.strip().upper()
        raise ValueError("Invalid type for UserRole")

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return UserRole.from_string(value)
