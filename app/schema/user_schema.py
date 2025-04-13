# # # app/schemas/user_schemas.py
# from pydantic import BaseModel, Field, validator
# from typing import Optional
# from app.common.enums.user_roles import UserRole

# class UserBase(BaseModel):
#     name: str = Field(..., min_length=2, max_length=50, example="Naman Bhatt")
#     username: str = Field(..., min_length=3, max_length=30, example="NamanBhatt")
#     role: str = Field(..., example="admin", description="User role. Can be 'admin', 'user', or 'reader'.")
    

#     @validator("role", pre=True, always=True)
#     def validate_role(cls, value):
#         """Normalize role to lowercase before validation."""
#         return UserRole.from_string(value)


# class UserCreate(UserBase):
#     password: str = Field(..., min_length=2, max_length=100, example="strongpassword")
#     # created_at: Optional[str] = Field(None, example="2023-10-01T12:00:00Z")


# class UserUpdate(BaseModel):
#     name: Optional[str] = Field(None, min_length=2, max_length=50, example="Updated Name")
#     username: Optional[str] = Field(None, min_length=3, max_length=30, example="UpdatedUsername")
#     password: Optional[str] = Field(None, min_length=3, max_length=100, example="NewStrongPassword")
#     role: str | None = None 

# class UserRead(UserBase):
#     id: int

#     class Config:
#         from_attributes = True


#2nd

# app/schemas/user_schemas.py

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timezone, timedelta
from app.common.enums.user_roles import UserRole
from pydantic.networks import EmailStr
import re

# Define the Indian time zone (UTC+05:30)
india_tz = timezone(timedelta(hours=5, minutes=30))

class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Naman Bhatt")
    username: str = Field(..., min_length=3, max_length=30, example="NamanBhatt")
    role: str = Field(
        ...,
        example="admin",
        description="User role. Can be 'admin', 'user', or 'reader'."
    )
    
    @validator("role", pre=True, always=True)
    def validate_role(cls, value):
        return UserRole.from_string(value)


class UserCreate(UserBase):
    password: str = Field(..., min_length=2, max_length=100, example="strongpassword")
    phone_number: Optional[str] = Field(None, example="+919810000000")
    address: Optional[str] = Field(None, example="Greater Noida, India")
    email: EmailStr  # Required and validated automatically

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v:
            pattern = re.compile(r"^\+91[6-9]\d{9}$")
            if not pattern.match(v):
                raise ValueError("Invalid phone number format. Use '+919XXXXXXXXX'")
        return v
    
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50, example="Updated Name")
    username: Optional[str] = Field(None, min_length=3, max_length=30, example="UpdatedUsername")
    password: Optional[str] = Field(None, min_length=3, max_length=100, example="NewStrongPassword")
    role: Optional[str] = None 
    phone_number: Optional[str] = Field(None, example="+919810000000")
    address: Optional[str] = Field(None, example="Greater Noida, India")
    email: Optional[str] = None 

    @validator("phone_number")
    def validate_phone_number(cls, v):
        if v:
            pattern = re.compile(r"^\+91[6-9]\d{9}$")
            if not pattern.match(v):
                raise ValueError("Invalid phone number format. Use '+919XXXXXXXXX'")
        return v
    
class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    phone_number: Optional[str] = Field(None, min_length=10, max_length=13, example="+919810000000")
    address: Optional[str] = Field(None, min_length=10, max_length=50, example="Greater Noida, India")
    email: EmailStr

    class Config:
        # Define a custom JSON encoder to convert datetime values to Indian Standard Time (UTC+05:30)
        json_encoders = {
            datetime: lambda v: (
                # If datetime is naive, assume it is in UTC
                (v if v.tzinfo is not None else v.replace(tzinfo=timezone.utc))
                .astimezone(india_tz)
                .strftime("%d-%m-%Y %H:%M:%S")
            )
        }
class OTPVerification(BaseModel):
    email: EmailStr
    otp: str