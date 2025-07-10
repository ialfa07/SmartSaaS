
import stripe
import os
from typing import Dict, Optional

# Configuration Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_...")

# Plans d'abonnement
STRIPE_PLANS = {
    "starter": {
        "price_id": "price_starter_monthly",
        "name": "Starter",
        "price": 9.99,
        "credits": 100,
        "features": ["100 crédits/mois", "Génération IA basique", "Support email"]
    },
    "pro": {
        "price_id": "price_pro_monthly", 
        "name": "Pro",
        "price": 29.99,
        "credits": 500,
        "features": ["500 crédits/mois", "Génération IA avancée", "Images IA", "Planificateur", "Support prioritaire"]
    },
    "premium": {
        "price_id": "price_premium_monthly",
        "name": "Premium", 
        "price": 79.99,
        "credits": 2000,
        "features": ["2000 crédits/mois", "Toutes les fonctionnalités", "IA premium", "Automatisation complète", "Support 24/7"]
    }
}

def create_checkout_session(user_email: str, plan_id: str) -> Dict:
    """Crée une session de paiement Stripe"""
    try:
        plan = STRIPE_PLANS.get(plan_id)
        if not plan:
            raise ValueError("Plan invalide")
            
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': plan['price_id'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://localhost:3000/pricing',
            customer_email=user_email,
            metadata={
                'plan_id': plan_id,
                'user_email': user_email
            }
        )
        return {"checkout_url": session.url, "session_id": session.id}
    except Exception as e:
        raise Exception(f"Erreur création session: {str(e)}")

def verify_payment(session_id: str) -> Dict:
    """Vérifie le paiement et retourne les détails"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "status": session.payment_status,
            "customer_email": session.customer_details.email,
            "plan_id": session.metadata.get('plan_id'),
            "amount": session.amount_total / 100
        }
    except Exception as e:
        raise Exception(f"Erreur vérification paiement: {str(e)}")

def create_customer_portal(customer_id: str) -> str:
    """Crée un lien vers le portail client Stripe"""
    try:
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url='http://localhost:3000/dashboard',
        )
        return session.url
    except Exception as e:
        raise Exception(f"Erreur portail client: {str(e)}")
