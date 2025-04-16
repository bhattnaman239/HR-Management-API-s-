from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool
    USE_CREDENTIALS: bool
    VALIDATE_CERTS: bool

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/auth")

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD", "")
    MAIL_FROM: str = os.getenv("MAIL_FROM", "")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "587"))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "")
    MAIL_STARTTLS: bool = os.getenv("MAIL_STARTTLS", "True") in ["True", "true"]
    MAIL_SSL_TLS: bool = os.getenv("MAIL_SSL_TLS", "False") in ["True", "true"]
    USE_CREDENTIALS: bool = os.getenv("USE_CREDENTIALS", "True") in ["True", "true"]
    VALIDATE_CERTS: bool = os.getenv("VALIDATE_CERTS", "True") in ["True", "true"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
settings = Settings()
