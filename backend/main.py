from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from openai_client import generate_text, generate_image, generate_marketing_content, generate_content_calendar
from auth import fake_auth, users_db
from models import PromptRequest, User, PaymentRequest, ImageRequest, MarketingRequest, CalendarRequest
from stripe_config import create_checkout_session, verify_payment, STRIPE_PLANS
from saas_tokens import (
    get_user_tokens, add_tokens, spend_tokens, get_referral_info, 
    process_referral, get_leaderboard, calculate_level, TOKEN_REWARDS
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
def generate(prompt: PromptRequest, user: User = Depends(fake_auth)):
    if users_db[user.email]["credits"] <= 0:
        raise HTTPException(status_code=403, detail="Not enough credits")
    response = generate_text(prompt.prompt)
    users_db[user.email]["credits"] -= 1
    return {"result": response, "credits_left": users_db[user.email]["credits"]}

@app.get("/plans")
def get_plans():
    """Retourne tous les plans disponibles"""
    return {"plans": STRIPE_PLANS}

@app.post("/create-checkout")
def create_checkout(payment: PaymentRequest, user: User = Depends(fake_auth)):
    """Crée une session de paiement Stripe"""
    try:
        session = create_checkout_session(user.email, payment.plan_id)
        return session
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/verify-payment")
def verify_payment_endpoint(session_id: str, user: User = Depends(fake_auth)):
    """Vérifie le paiement et met à jour les crédits"""
    try:
        payment_info = verify_payment(session_id)
        if payment_info["status"] == "paid":
            plan = STRIPE_PLANS[payment_info["plan_id"]]
            users_db[user.email]["credits"] += plan["credits"]
            users_db[user.email]["plan"] = payment_info["plan_id"]
            return {"success": True, "credits": users_db[user.email]["credits"]}
        else:
            raise HTTPException(status_code=400, detail="Paiement non confirmé")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/user-info")
def get_user_info(user: User = Depends(fake_auth)):
    """Retourne les informations utilisateur"""
    user_data = users_db[user.email]
    return {
        "email": user.email,
        "credits": user_data["credits"],
        "plan": user_data.get("plan", "free")
    }

@app.post("/generate-image")
def generate_image_endpoint(request: ImageRequest, user: User = Depends(fake_auth)):
    """Génère une image avec DALL-E"""
    if users_db[user.email]["credits"] < 3:  # 3 crédits pour une image
        raise HTTPException(status_code=403, detail="Not enough credits (3 required)")
    
    result = generate_image(request.prompt, request.size, request.quality)
    if result["success"]:
        users_db[user.email]["credits"] -= 3
        return {
            **result,
            "credits_left": users_db[user.email]["credits"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.post("/generate-marketing-content")
def generate_marketing_endpoint(request: MarketingRequest, user: User = Depends(fake_auth)):
    """Génère du contenu marketing complet"""
    if users_db[user.email]["credits"] < 5:  # 5 crédits pour contenu complet
        raise HTTPException(status_code=403, detail="Not enough credits (5 required)")
    
    result = generate_marketing_content(
        request.business_type, 
        request.target_audience, 
        request.platform
    )
    
    if result["success"]:
        users_db[user.email]["credits"] -= 5
        return {
            **result,
            "credits_left": users_db[user.email]["credits"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.post("/generate-calendar")
def generate_calendar_endpoint(request: CalendarRequest, user: User = Depends(fake_auth)):
    """Génère un calendrier de contenu"""
    if users_db[user.email]["credits"] < 10:  # 10 crédits pour calendrier
        raise HTTPException(status_code=403, detail="Not enough credits (10 required)")
    
    result = generate_content_calendar(request.business_type, request.duration_days)
    
    if result["success"]:
        users_db[user.email]["credits"] -= 10
        return {
            **result,
            "credits_left": users_db[user.email]["credits"]
        }
    else:
        raise HTTPException(status_code=400, detail=result["error"])

@app.get("/tokens/balance")
def get_token_balance(user: User = Depends(fake_auth)):
    """Récupère le solde de jetons SaaS de l'utilisateur"""
    tokens_data = get_user_tokens(user.email)
    level_data = calculate_level(tokens_data["total_earned"])
    
    return {
        "balance": tokens_data["balance"],
        "total_earned": tokens_data["total_earned"],
        "level": level_data,
        "history": tokens_data["history"][-10:]  # 10 dernières transactions
    }

@app.post("/tokens/daily-reward")
def claim_daily_reward(user: User = Depends(fake_auth)):
    """Réclame la récompense quotidienne"""
    # Vérification simple (en production, il faudrait vérifier la date)
    tokens_data = add_tokens(user.email, TOKEN_REWARDS["daily_login"], "daily_login")
    
    return {
        "success": True,
        "reward": TOKEN_REWARDS["daily_login"],
        "new_balance": tokens_data["balance"],
        "message": f"Vous avez gagné {TOKEN_REWARDS['daily_login']} jetons SaaS !"
    }

@app.get("/tokens/referral")
def get_referral_data(user: User = Depends(fake_auth)):
    """Récupère les données de parrainage"""
    referral_data = get_referral_info(user.email)
    
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
def refer_user(referral: ReferralRequest, user: User = Depends(fake_auth)):
    """Traite un nouveau parrainage"""
    result = process_referral(user.email, referral.referred_email)
    
    if result["success"]:
        return {
            "success": True,
            "message": f"Parrainage réussi ! Vous avez gagné {result['referrer_reward']} jetons.",
            "referrer_reward": result["referrer_reward"],
            "new_balance": result["referrer_balance"]
        }
    else:
        raise HTTPException(status_code=400, detail="Erreur lors du parrainage")

@app.get("/tokens/leaderboard")
def get_tokens_leaderboard():
    """Récupère le classement des utilisateurs"""
    leaderboard = get_leaderboard(10)
    
    return {
        "leaderboard": leaderboard,
        "description": "Top 10 des utilisateurs par jetons gagnés"
    }

@app.post("/tokens/exchange")
def exchange_tokens_for_credits(amount: int, user: User = Depends(fake_auth)):
    """Échange des jetons contre des crédits IA"""
    if amount < 50:
        raise HTTPException(status_code=400, detail="Minimum 50 jetons requis")
    
    # Taux de change : 50 jetons = 1 crédit
    credits_to_add = amount // 50
    
    if spend_tokens(user.email, amount, f"exchange_for_{credits_to_add}_credits"):
        users_db[user.email]["credits"] += credits_to_add
        
        return {
            "success": True,
            "tokens_spent": amount,
            "credits_received": credits_to_add,
            "new_token_balance": get_user_tokens(user.email)["balance"],
            "new_credit_balance": users_db[user.email]["credits"]
        }
    else:
        raise HTTPException(status_code=400, detail="Jetons insuffisants")

@app.get("/tokens/rewards")
def get_available_rewards():
    """Liste toutes les façons de gagner des jetons"""
    return {
        "daily_actions": {
            "daily_login": {"reward": TOKEN_REWARDS["daily_login"], "description": "Connexion quotidienne"},
            "first_generation": {"reward": TOKEN_REWARDS["first_generation"], "description": "Première génération IA de la journée"},
            "share_content": {"reward": TOKEN_REWARDS["share_content"], "description": "Partager du contenu généré"}
        },
        "achievements": {
            "complete_profile": {"reward": TOKEN_REWARDS["complete_profile"], "description": "Compléter son profil"},
            "weekly_active": {"reward": TOKEN_REWARDS["weekly_active"], "description": "Actif 7 jours consécutifs"},
            "content_viral": {"reward": TOKEN_REWARDS["content_viral"], "description": "Contenu partagé 100+ fois"}
        },
        "referral": {
            "referral_signup": {"reward": TOKEN_REWARDS["referral_signup"], "description": "Parrainage d'un nouvel utilisateur"},
            "referral_first_purchase": {"reward": TOKEN_REWARDS["referral_first_purchase"], "description": "Premier achat d'un filleul"}
        },
        "exchange_rate": "50 jetons = 1 crédit IA"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
