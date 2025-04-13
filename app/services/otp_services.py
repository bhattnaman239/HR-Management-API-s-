# otp_service.py
import asyncio
import secrets
from datetime import datetime, timedelta

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import logging
from fastapi import HTTPException

from app.config import settings  # import the Settings instance with SMTP config

# Configure FastAPI-Mail using ConnectionConfig with settings from .env
conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    USE_CREDENTIALS = settings.USE_CREDENTIALS,
    VALIDATE_CERTS = settings.VALIDATE_CERTS
)
fast_mail = FastMail(conf)

# In-memory store for OTPs: { email: {"code": <OTP>, "expires": <datetime>} }
otp_storage: dict[str, dict] = {}

async def send_otp(email: EmailStr) -> None:
    """Generate an OTP, store it, and send it via email."""
    otp_code = str(secrets.randbelow(10**6)).zfill(6)  # e.g., "052419"
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    otp_storage[email] = {"code": otp_code, "expires": expires_at}
    asyncio.create_task(_expire_otp(email, otp_code, delay_seconds=300))

    subject = "Your One-Time Password (OTP)"
    body = f"Your OTP code is {otp_code}. It will expire in 5 minutes."
    message = MessageSchema(subject=subject, recipients=[email], body=body, subtype="plain")
    
    try:
        await fast_mail.send_message(message)
    except Exception as exc:
        logging.error("Error sending OTP email: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to send OTP email")
    

async def _expire_otp(email: str, otp_code: str, delay_seconds: int):
    """Background task to remove OTP from storage after a delay."""
    await asyncio.sleep(delay_seconds)
    # After 5 minutes, delete the OTP if it hasn't been refreshed or used
    entry = otp_storage.get(email)
    if entry and entry["code"] == otp_code:
        otp_storage.pop(email, None)

def verify_otp(email: EmailStr, code: str) -> bool:
    """Verify a provided OTP code for the given email. Returns True if valid."""
    entry = otp_storage.get(email)
    if not entry:
        return False  # No OTP sent or it has already expired/been used
    # Check if OTP matches and is not expired
    if entry["code"] == code and datetime.utcnow() < entry["expires"]:
        # OTP is valid – remove it after successful verification to prevent reuse
        otp_storage.pop(email, None)
        return True
    # If code is wrong or expired, you may optionally remove it as well:
    if datetime.utcnow() >= entry["expires"]:
        otp_storage.pop(email, None)  # expired, remove from store
    return False
