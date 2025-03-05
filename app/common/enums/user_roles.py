from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    READER = "reader"

    @classmethod
    def from_string(cls, role_str: str):
        """Normalize input role and return corresponding enum value."""
        role_str = role_str.lower()
        if role_str in cls._value2member_map_:
            return cls._value2member_map_[role_str]
        raise ValueError(f"Invalid role: {role_str}. Allowed roles: {', '.join(cls._value2member_map_.keys())}")
