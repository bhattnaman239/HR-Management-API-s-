

from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, timezone, timedelta
from app.common.enums.user_roles import UserRole
from pydantic.networks import EmailStr
import re

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
    email: EmailStr  

    @validator("password")
    def validate_strong_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v
    
    @validator("email")
    def validate_gmail_email(cls, v):
        if not v.endswith("@gmail.com"):
            raise ValueError("Email must have a '@gmail.com' domain")
        return v
    
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
    

    @validator("password")
    def validate_strong_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v

    @validator("email")
    def validate_gmail_email(cls, v):
        if not v.endswith("@gmail.com"):
            raise ValueError("Email must have a '@gmail.com' domain")
        return v
    
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
        json_encoders = {
            datetime: lambda v: (
                (v if v.tzinfo is not None else v.replace(tzinfo=timezone.utc))
                .astimezone(india_tz)
                .strftime("%d-%m-%Y %H:%M:%S")
            )
        }
class OTPVerification(BaseModel):
    email: EmailStr
    otp: str