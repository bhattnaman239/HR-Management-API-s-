


from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schema.otp_schema import OTPVerify
from app.services.otp_services import send_otp, verify_otp
from app.dependencies import get_current_user, get_db
from app.common.constants.log import logger

router = APIRouter(prefix="/otp", tags=["OTP Verification"])
