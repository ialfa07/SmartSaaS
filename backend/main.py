
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from openai_client import generate_text, generate_image, generate_marketing_content, generate_content_calendar
from database import db_service
from models import (PromptRequest, UserCreate, UserResponse, PaymentRequest, 
                   ImageRequest, MarketingRequest, CalendarRequest, ReferralRequest,
                   create_tables, get_db)
from stripe_config import create_checkout_session, verify_payment, STRIPE_PLANS
from datetime import timedelta, datetime
from jose import JWTError, jwt
import os

# Créer les tables au démarrage
create_tables()

app = FastAPI(title="SmartSaaS API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration JWT
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

# Récompenses en jetons SaaS
TOKEN_REWARDS = {
    "daily_login": 1,
    "first_generation": 2,
    "referral_signup": 25,
    "referral_first_purchase": 50,
    "complete_profile": 10,
    "weekly_active": 15,
    "share_content": 3,
    "content_viral": 100
}

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db_service.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

def calculate_level(total_earned: int) -> dict:
    """Calcule le niveau basé sur les jetons gagnés"""
    levels = [
        {"level": 1, "name": "Débutant", "min_tokens": 0, "max_tokens": 49},
        {"level": 2, "name": "Apprenti", "min_tokens": 50, "max_tokens": 149},
        {"level": 3, "name": "Créateur", "min_tokens": 150, "max_tokens": 299},
        {"level": 4, "name": "Expert", "min_tokens": 300, "max_tokens": 499},
        {"level": 5, "name": "Maître", "min_tokens": 500, "max_tokens": 999},
        {"level": 6, "name": "Légende", "min_tokens": 1000, "max_tokens": float('inf')}
    ]
    
    for level in levels:
        if level["min_tokens"] <= total_earned <= level["max_tokens"]:
            return level
    return levels[0]

@app.get("/")
def read_root():
    return {"message": "SmartSaaS API - Plateforme de génération de contenu IA"}

@app.post("/auth/register")
def register(user_data: UserCreate):
    """Inscription utilisateur"""
    existing_user = db_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    user = db_service.create_user(user_data.email, user_data.password)
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "credits": user.credits,
            "plan": user.plan
        }
    }

@app.post("/auth/login")
def login(user_data: UserCreate):
    """Connexion utilisateur"""
    user = db_service.authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email ou mot de passe incorrect"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user.email,
            "credits": user.credits,
            "plan": user.plan
        }
    }

@app.get("/user-info")
def get_user_info(current_user = Depends(get_current_user)):
    """Retourne les informations utilisateur"""
    return {
        "email": current_user.email,
        "credits": current_user.credits,
        "plan": current_user.plan,
        "referral_code": current_user.referral_code,
        "created_at": current_user.created_at
    }

@app.post("/generate")
def generate(prompt: PromptRequest, current_user = Depends(get_current_user)):
    if current_user.credits <= 0:
        raise HTTPException(status_code=403, detail="Crédits insuffisants")
    
    response = generate_text(prompt.prompt)
    db_service.spend_credits(current_user.id, 1)
    
    # Récompenser la première génération de la journée
    db_service.add_saas_tokens(current_user.id, TOKEN_REWARDS["first_generation"], 
                              "first_generation", "Première génération IA")
    
    return {
        "result": response,
        "credits_left": current_user.credits - 1
    }

@app.post("/generate-image")
def generate_image_endpoint(request: ImageRequest, current_user = Depends(get_current_user)):
    """Génère une image avec DALL-E"""
    if current_user.credits < 3:
        raise HTTPException(status_code=403, detail="Crédits insuffisants (3 requis)")

    result = generate_image(request.prompt, request.size, request.quality)
    if result["success"]:
        db_service.spend_credits(current_user.id, 3)
        return {**result, "credits_left": current_user.credits - 3}
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.post("/generate-marketing-content")
def generate_marketing_endpoint(request: MarketingRequest, current_user = Depends(get_current_user)):
    """Génère du contenu marketing complet"""
    if current_user.credits < 5:
        raise HTTPException(status_code=403, detail="Crédits insuffisants (5 requis)")

    result = generate_marketing_content(request.business_type, request.target_audience, request.platform)
    if result["success"]:
        db_service.spend_credits(current_user.id, 5)
        return {**result, "credits_left": current_user.credits - 5}
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.post("/generate-calendar")
def generate_calendar_endpoint(request: CalendarRequest, current_user = Depends(get_current_user)):
    """Génère un calendrier de contenu"""
    if current_user.credits < 10:
        raise HTTPException(status_code=403, detail="Crédits insuffisants (10 requis)")

    result = generate_content_calendar(request.business_type, request.duration_days)
    if result["success"]:
        db_service.spend_credits(current_user.id, 10)
        return {**result, "credits_left": current_user.credits - 10}
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.get("/tokens/balance")
def get_token_balance(current_user = Depends(get_current_user)):
    """Récupère le solde de jetons SaaS de l'utilisateur"""
    tokens_data = db_service.get_user_saas_tokens(current_user.id)
    level_data = calculate_level(tokens_data["total_earned"])

    return {
        "balance": tokens_data["balance"],
        "total_earned": tokens_data["total_earned"],
        "level": level_data,
        "history": tokens_data["history"][:10]  # 10 dernières transactions
    }

@app.post("/tokens/daily-reward")
def claim_daily_reward(current_user = Depends(get_current_user)):
    """Réclame la récompense quotidienne"""
    db_service.add_saas_tokens(current_user.id, TOKEN_REWARDS["daily_login"], 
                              "daily_login", "Connexion quotidienne")
    
    tokens_data = db_service.get_user_saas_tokens(current_user.id)
    
    return {
        "success": True,
        "reward": TOKEN_REWARDS["daily_login"],
        "new_balance": tokens_data["balance"],
        "message": f"Vous avez gagné {TOKEN_REWARDS['daily_login']} jetons SaaS !"
    }

@app.get("/tokens/referral")
def get_referral_data(current_user = Depends(get_current_user)):
    """Récupère les données de parrainage"""
    referral_data = db_service.get_referral_info(current_user.id)

    return {
        "referral_code": referral_data["referral_code"],
        "total_referrals": referral_data["total_referrals"],
        "referred_users": referral_data["referred_users"],
        "referral_link": f"https://smartsaas.com/signup?ref={referral_data['referral_code']}",
        "rewards": {
            "per_signup": TOKEN_REWARDS["referral_signup"],
            "per_purchase": TOKEN_REWARDS["referral_first_purchase"]
        }
    }

@app.post("/tokens/refer")
def refer_user(referral: ReferralRequest, current_user = Depends(get_current_user)):
    """Traite un nouveau parrainage"""
    result = db_service.process_referral(current_user.id, referral.referred_email)

    if result["success"]:
        return {
            "success": True,
            "message": f"Parrainage réussi ! Vous avez gagné {result['referrer_reward']} jetons.",
            "referrer_reward": result["referrer_reward"],
            "new_balance": result["referrer_balance"]
        }
    else:
        raise HTTPException(status_code=400, detail=result.get("error", "Erreur lors du parrainage"))

@app.get("/tokens/leaderboard")
def get_tokens_leaderboard():
    """Récupère le classement des utilisateurs"""
    leaderboard = db_service.get_leaderboard(10)
    return {
        "leaderboard": leaderboard,
        "description": "Top 10 des utilisateurs par jetons gagnés"
    }

@app.post("/tokens/exchange")
def exchange_tokens_for_credits(amount: int, current_user = Depends(get_current_user)):
    """Échange des jetons contre des crédits IA"""
    if amount < 50:
        raise HTTPException(status_code=400, detail="Minimum 50 jetons requis")

    # Taux de change : 50 jetons = 1 crédit
    credits_to_add = amount // 50
    
    if db_service.spend_saas_tokens(current_user.id, amount, f"exchange_for_{credits_to_add}_credits"):
        db_service.add_credits(current_user.id, credits_to_add)
        
        return {
            "success": True,
            "tokens_spent": amount,
            "credits_received": credits_to_add,
            "new_token_balance": db_service.get_user_saas_tokens(current_user.id)["balance"],
            "new_credit_balance": current_user.credits + credits_to_add
        }
    else:
        raise HTTPException(status_code=400, detail="Jetons insuffisants")

@app.get("/plans")
def get_plans():
    """Retourne tous les plans disponibles"""
    return {"plans": STRIPE_PLANS}

@app.post("/create-checkout")
def create_checkout(payment: PaymentRequest, current_user = Depends(get_current_user)):
    """Crée une session de paiement Stripe"""
    try:
        session = create_checkout_session(current_user.email, payment.plan_id)
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify-payment")
def verify_payment_endpoint(session_id: str, current_user = Depends(get_current_user)):
    """Vérifie le paiement et met à jour les crédits"""
    try:
        payment_info = verify_payment(session_id)
        if payment_info["status"] == "paid":
            plan = STRIPE_PLANS[payment_info["plan_id"]]
            db_service.add_credits(current_user.id, plan["credits"])
            
            # Récompenser avec des jetons SaaS
            db_service.add_saas_tokens(current_user.id, 20, "payment", 
                                      f"Achat du plan {payment_info['plan_id']}")
            
            return {
                "success": True,
                "credits": current_user.credits + plan["credits"]
            }
        else:
            raise HTTPException(status_code=400, detail="Paiement non confirmé")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/tokens/rewards")
def get_available_rewards():
    """Liste toutes les façons de gagner des jetons"""
    return {
        "daily_actions": {
            "daily_login": {
                "reward": TOKEN_REWARDS["daily_login"],
                "description": "Connexion quotidienne"
            },
            "first_generation": {
                "reward": TOKEN_REWARDS["first_generation"],
                "description": "Première génération IA de la journée"
            },
            "share_content": {
                "reward": TOKEN_REWARDS["share_content"],
                "description": "Partager du contenu généré"
            }
        },
        "achievements": {
            "complete_profile": {
                "reward": TOKEN_REWARDS["complete_profile"],
                "description": "Compléter son profil"
            },
            "weekly_active": {
                "reward": TOKEN_REWARDS["weekly_active"],
                "description": "Actif 7 jours consécutifs"
            },
            "content_viral": {
                "reward": TOKEN_REWARDS["content_viral"],
                "description": "Contenu partagé 100+ fois"
            }
        },
        "referral": {
            "referral_signup": {
                "reward": TOKEN_REWARDS["referral_signup"],
                "description": "Parrainage d'un nouvel utilisateur"
            },
            "referral_first_purchase": {
                "reward": TOKEN_REWARDS["referral_first_purchase"],
                "description": "Premier achat d'un filleul"
            }
        },
        "exchange_rate": "50 jetons = 1 crédit IA"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
