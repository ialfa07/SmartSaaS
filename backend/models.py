
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Configuration de la base de données
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./smartsaas.db")

# Ajuster l'URL pour PostgreSQL si nécessaire
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configuration du moteur avec options pour PostgreSQL
if "postgresql" in DATABASE_URL:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_recycle=300,
        echo=False
    )
else:
    engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèles SQLAlchemy
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    credits = Column(Integer, default=5)
    plan = Column(String, default="free")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    referral_code = Column(String, unique=True, index=True)
    referred_by = Column(String, nullable=True)
    wallet_address = Column(String, nullable=True, index=True)
    
    # Relations
    saas_tokens = relationship("SaasToken", back_populates="user")
    referred_users = relationship("User", remote_side=[id], foreign_keys=[referred_by])

class SaasToken(Base):
    __tablename__ = "saas_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)  # earned, spent, daily_login, referral, etc.
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    user = relationship("User", back_populates="saas_tokens")

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    stripe_session_id = Column(String, unique=True)
    plan_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")
    credits_added = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

# Modèles Pydantic pour les APIs
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    credits: int
    plan: str
    is_active: bool
    created_at: datetime

class TokenBalance(BaseModel):
    balance: int
    total_earned: int
    level: dict

class PromptRequest(BaseModel):
    prompt: str

class ImageRequest(BaseModel):
    prompt: str
    size: str = "1024x1024"
    quality: str = "standard"

class MarketingRequest(BaseModel):
    business_type: str
    target_audience: str
    platform: str

class CalendarRequest(BaseModel):
    business_type: str
    duration_days: int = 30

class PaymentRequest(BaseModel):
    plan_id: str

class ReferralRequest(BaseModel):
    referred_email: str

# Créer les tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Fonction pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
