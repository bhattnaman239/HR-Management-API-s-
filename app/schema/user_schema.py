# app/schemas/user_schemas.py
from pydantic import BaseModel, Field, validator
from typing import Optional
from app.common.enums.user_roles import UserRole

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Naman Bhatt")
    username: str = Field(..., min_length=3, max_length=30, example="NamanBhatt")
    role: str

    @validator("role", pre=True, always=True)
    def validate_role(cls, value):
        """Normalize role to lowercase before validation."""
        return UserRole.from_string(value)


class UserCreate(UserBase):
    password: str = Field(..., min_length=2, max_length=100, example="strongpassword")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, example="Updated Name")
    username: Optional[str] = Field(None, min_length=3, max_length=30, example="UpdatedUsername")
    password: Optional[str] = Field(None, min_length=3, max_length=100, example="NewStrongPassword")
    role: str | None = None 

class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
