from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    USE_TLS = os.getenv("SMTP_USE_TLS", "True").lower() in ("true","1","yes")
    LOG_FILE = os.getenv("LOG_FILE", "email_service.log")

settings = Settings()