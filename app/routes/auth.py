
from fastapi import APIRouter, HTTPException, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import jwt, JWTError

from app.dependencies import get_db
from app.services.auth_service import AuthService
from app.services.otp_services import send_otp, verify_otp
from app.config import settings
from app.common.constants.log import logger
from app.schema.otp_schema import OTPVerify
from app.schema.user_schema import UserCreate
from app.common.enums.user_roles import UserRole
from app.schema.otp_schema import ResendOTPRequest

router = APIRouter(prefix="/auth", tags=["authentication"])

###############################
# Signup Endpoints
###############################
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    The user is created with is_verified=False and an OTP is sent to their email.
    If the user attempts to sign up with a role of 'ADMIN', the request is rejected.
    """
    if user_data.role.upper() == "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot sign up as an admin."
        )
    
    auth_service = AuthService(db)
    user = auth_service.create_user(user_data)
    if not user:
        raise HTTPException(status_code=400, detail="User creation failed")
    
    await send_otp(user.email)
    logger.info(f"Signup OTP sent to {user.email}")
    return {"message": "User registered successfully. Please verify OTP sent to your email."}

@router.post("/verify-signup-otp")
async def verify_signup_otp(otp_data: OTPVerify, username: str, db: Session = Depends(get_db)):
    """
    Verify OTP for a newly registered user.
    On success, the user's record is updated with is_verified=True.
    """
    auth_service = AuthService(db)
    user = auth_service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if verify_otp(user.email, otp_data.otp):
        user.is_verified = True
        db.commit()
        logger.info(f"Signup OTP verified for user {user.username}")
        return {"message": "OTP verified. Signup complete."}
    else:
        logger.warning(f"Invalid OTP for user {user.username}")
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

@router.post("/resend-signup-otp")
async def resend_signup_otp(
    payload: ResendOTPRequest,
    db: Session = Depends(get_db),
):
    auth_service = AuthService(db)
    user = auth_service.get_user_by_username(payload.username)
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Account already verified.")
    await send_otp(user.email)
    logger.info(f"Resent signup OTP to {user.email}")
    return {"message": "OTP resent to your registered email."}

###############################
# Signin Endpoint 
###############################
@router.post("/signin")
def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    response: Response = None
):
    """
    Signin for returning users.
    Validates username and password.
    If the credentials are valid, a JWT token is generated and set in an HTTP‑only cookie.
    No OTP verification is required at signin.
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        logger.warning(f"Signin failed: Invalid credentials for {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token({"sub": user.username}, access_token_expires)
    logger.info(f"User {user.username} signed in successfully.")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=access_token_expires.seconds
    )
    return {"message": "Signin successful; token set in cookie."}

###############################
# Logout Endpoint
###############################
@router.post("/logout")
def logout(response: Response):
    """
    Logout the user by deleting the authentication cookie.
    """
    response.delete_cookie("access_token")
    logger.info("User logged out successfully")
    return {"message": "Logged out successfully."}
