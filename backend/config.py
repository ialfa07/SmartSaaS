
import os
from typing import Optional
from pydantic import validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/smartsaas")
    
    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    STRIPE_SECRET_KEY: Optional[str] = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PUBLIC_KEY: Optional[str] = os.getenv("STRIPE_PUBLIC_KEY")
    
    # Email configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    FROM_EMAIL: str = "noreply@smartsaas.com"
    
    # Frontend URL pour les liens dans les emails
    FRONTEND_URL: str = "https://smartsaas.com"
    
    @validator('SMTP_USER')
    def smtp_user_required(cls, v):
        if not v:
            print("⚠️ SMTP_USER non configuré - emails désactivés")
        return v
    
    class Config:
        env_file = ".env"
    
    # Web3/Blockchain
    WEB3_RPC_URL: Optional[str] = os.getenv("WEB3_RPC_URL")
    WEB3_PRIVATE_KEY: Optional[str] = os.getenv("WEB3_PRIVATE_KEY")
    
    # CORS
    ALLOWED_HOSTS: list = [
        "http://localhost:3000",
        "https://*.replit.app",
        "https://*.replit.dev",
        "https://*.replit.com"
    ]
    
    # Debug mode
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
