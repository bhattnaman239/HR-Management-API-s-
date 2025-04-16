# # routes/otp.py
# from fastapi import APIRouter, HTTPException, Depends
# from fastapi import BackgroundTasks  # (optional, not used here but could be)
# from app.schema.otp_schema import OTPRequest, OTPVerify
# from app.services.otp_services import send_otp, verify_otp

# router = APIRouter(prefix="/otp", tags=["OTP Verification"])

# @router.post("/send")
# async def send_otp_endpoint(payload: OTPRequest):
#     """
#     Generate an OTP for the given email and send it via email.
#     """
#     try:
#         # Trigger sending OTP email (await the async function to ensure it's sent)
#         await send_otp(payload.email)
#     except Exception as e:
#         # If email sending fails, respond with server error
#         raise HTTPException(status_code=500, detail="Failed to send OTP email")
#     return {"message": f"OTP sent to {payload.email}. Please check your inbox."}

# @router.post("/verify")
# async def verify_otp_endpoint(payload: OTPVerify):
#     """
#     Verify the OTP code for the given email.
#     """
#     if verify_otp(payload.email, payload.otp):
#         return {"message": "OTP verified successfully. Authentication successful."}
#     # If verification fails, inform the client (bad request or unauthorized)
#     raise HTTPException(status_code=400, detail="Invalid or expired OTP")



from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schema.otp_schema import OTPVerify
from app.services.otp_services import send_otp, verify_otp
from app.dependencies import get_current_user, get_db
from app.common.constants.log import logger

router = APIRouter(prefix="/otp", tags=["OTP Verification"])

# @router.post("/send")
# async def send_otp_endpoint(
#     # payload: OTPRequest,  # Although a payload is accepted, we use the authenticated user's email.
#     current_user=Depends(get_current_user)
# ):
#     """
#     Generate and send an OTP to the authenticated user's email.
#     The user's email from the token is used, ensuring that OTPs are sent only after authentication.
#     """
#     user_email = current_user.email
#     try:
#         await send_otp(user_email)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Failed to send OTP email")
#     logger.info(f"OTP sent to {user_email}")
#     return {"message": f"OTP sent to {user_email}. Please check your inbox."}

# @router.post("/verify")
# async def verify_otp_endpoint(
#     payload: OTPVerify,  # Contains the OTP code submitted by the user.
#     current_user=Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     user_email = current_user.email
#     if verify_otp(user_email, payload.otp):
#         # Mark the user as OTP verified
#         current_user.is_otp_verified = True
#         # db.add(current_user)
#         db.commit()
#         db.refresh(current_user)
#         logger.info(f"OTP verified successfully for {user_email}")
#         return {"message": "OTP verified successfully. Authentication successful."}
#     logger.warning(f"Invalid or expired OTP for {user_email}")
#     raise HTTPException(status_code=400, detail="Invalid or expired OTP")
