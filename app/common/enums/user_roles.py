# app/common/enums/user_roles.py
from enum import Enum

class UserRole(Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    READER = "READER"

    @classmethod
    def from_string(cls, s):
        # If s is already an instance of UserRole, return it.
        if isinstance(s, cls):
            return s
        normalized = s.strip().upper()
        if normalized in {"ADMIN", "USER"}:
            return cls(normalized)
        # For anything else, default to READER.
        return cls.READER
