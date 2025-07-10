from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from openai_client import generate_text
from auth import fake_auth, users_db
from models import PromptRequest, User, PaymentRequest
from stripe_config import create_checkout_session, verify_payment, STRIPE_PLANS

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
