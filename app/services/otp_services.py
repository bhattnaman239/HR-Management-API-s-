
import asyncio
import secrets
from datetime import datetime, timedelta
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import logging
from fastapi import HTTPException

from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)
fast_mail = FastMail(conf)

otp_storage: dict[str, dict] = {}

async def send_otp(email: EmailStr) -> None:
    otp_code = str(secrets.randbelow(10**6)).zfill(6)
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
    await asyncio.sleep(delay_seconds)
    entry = otp_storage.get(email)
    if entry and entry["code"] == otp_code:
        otp_storage.pop(email, None)

def verify_otp(email: EmailStr, code: str) -> bool:
    entry = otp_storage.get(email)
    if not entry:
        return False
    if entry["code"] == code and datetime.utcnow() < entry["expires"]:
        otp_storage.pop(email, None)
        return True
    if datetime.utcnow() >= entry["expires"]:
        otp_storage.pop(email, None)
    return False
