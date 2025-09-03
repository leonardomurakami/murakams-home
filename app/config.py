from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # GitHub
    github_username: Optional[str] = None
    github_token: Optional[str] = None
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    contact_email: Optional[str] = None
    
    # App
    secret_key: str = "your-secret-key-change-this"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
