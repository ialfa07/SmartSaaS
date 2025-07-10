
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import os

# Configuration base de données
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/smartsaas")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modèles de base de données
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    credits = Column(Integer, default=5)
    plan = Column(String, default="free")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)

class TokenTransaction(Base):
    __tablename__ = "token_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, index=True, nullable=False)
    amount = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)  # "earned" or "spent"
    created_at = Column(DateTime, default=datetime.utcnow)

class Referral(Base):
    __tablename__ = "referrals"
    
    id = Column(Integer, primary_key=True, index=True)
    referrer_email = Column(String, nullable=False)
    referred_email = Column(String, nullable=False)
    referral_code = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, completed
    created_at = Column(DateTime, default=datetime.utcnow)

class ContentGeneration(Base):
    __tablename__ = "content_generations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    generation_type = Column(String, nullable=False)  # text, image, marketing, calendar
    credits_used = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# Fonction pour créer les tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Dependency pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fonctions utilitaires pour les utilisateurs
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, hashed_password: str):
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_credits(db: Session, email: str, credits: int):
    user = get_user_by_email(db, email)
    if user:
        user.credits = credits
        db.commit()
        return True
    return False

def add_user_credits(db: Session, email: str, amount: int):
    user = get_user_by_email(db, email)
    if user:
        user.credits += amount
        db.commit()
        return True
    return False

# Fonctions pour les jetons
def get_user_tokens(db: Session, email: str):
    transactions = db.query(TokenTransaction).filter(
        TokenTransaction.user_email == email
    ).all()
    
    balance = sum(t.amount if t.transaction_type == "earned" else -t.amount for t in transactions)
    total_earned = sum(t.amount for t in transactions if t.transaction_type == "earned")
    
    return {
        "balance": balance,
        "total_earned": total_earned,
        "history": [
            {
                "date": t.created_at.isoformat(),
                "action": t.action,
                "amount": t.amount,
                "type": t.transaction_type
            }
            for t in transactions[-10:]  # 10 dernières transactions
        ]
    }

def add_token_transaction(db: Session, email: str, amount: int, action: str):
    transaction = TokenTransaction(
        user_email=email,
        amount=amount,
        action=action,
        transaction_type="earned"
    )
    db.add(transaction)
    db.commit()
    return get_user_tokens(db, email)

def spend_user_tokens(db: Session, email: str, amount: int, action: str):
    current_balance = get_user_tokens(db, email)["balance"]
    if current_balance >= amount:
        transaction = TokenTransaction(
            user_email=email,
            amount=amount,
            action=action,
            transaction_type="spent"
        )
        db.add(transaction)
        db.commit()
        return True
    return False
