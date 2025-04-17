# otp_schemas.py
from pydantic import BaseModel

class OTPVerify(BaseModel):
    otp: str
    
class ResendOTPRequest(BaseModel):
    username: str