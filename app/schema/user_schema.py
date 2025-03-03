# app/schemas/user_schemas.py
from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    name: str = Field(..., example="Naman Bhatt")
    username: str = Field(..., example="NamanBhatt")


class UserCreate(UserBase):
    password: str = Field(..., example="1234")


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, example="String")
    username: Optional[str] = Field(None, example="String")
    password: Optional[str] = Field(None, example="1234")


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True
