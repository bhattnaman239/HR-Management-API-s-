# routes/otp.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi import BackgroundTasks  # (optional, not used here but could be)
from app.schema.otp_schema import OTPRequest, OTPVerify
from app.services.otp_services import send_otp, verify_otp

router = APIRouter()

@router.post("/otp/send")
async def send_otp_endpoint(payload: OTPRequest):
    """
    Generate an OTP for the given email and send it via email.
    """
    try:
        # Trigger sending OTP email (await the async function to ensure it's sent)
        await send_otp(payload.email)
    except Exception as e:
        # If email sending fails, respond with server error
        raise HTTPException(status_code=500, detail="Failed to send OTP email")
    return {"message": f"OTP sent to {payload.email}. Please check your inbox."}

@router.post("/otp/verify")
async def verify_otp_endpoint(payload: OTPVerify):
    """
    Verify the OTP code for the given email.
    """
    if verify_otp(payload.email, payload.otp):
        return {"message": "OTP verified successfully. Authentication successful."}
    # If verification fails, inform the client (bad request or unauthorized)
    raise HTTPException(status_code=400, detail="Invalid or expired OTP")
