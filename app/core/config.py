from pydantic_settings import BaseSettings
from pydantic import EmailStr

class Settings(BaseSettings):
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    USE_TLS: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
