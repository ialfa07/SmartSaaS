import stripe
import os
from typing import Dict
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# --- Configuration de Stripe ---
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

if not stripe.api_key:
    print("⚠️  Avertissement: STRIPE_SECRET_KEY n'est pas définie.")
    stripe.api_key = "sk_test_placeholder"

# --- Plans d'Abonnement ---
# Les prix sont en centimes pour éviter les erreurs de virgule flottante
STRIPE_PLANS = {
    "starter": {
        "price_id": os.getenv("STRIPE_STARTER_PRICE_ID", "price_starter_monthly_placeholder"),
        "name": "Starter",
        "price": 900,  # 9€ en centimes
        "credits": 100,
        "features": ["100 crédits IA/mois", "Génération de texte", "Support par email", "+10 SaaS tokens/mois"]
    },
    "pro": {
        "price_id": os.getenv("STRIPE_PRO_PRICE_ID", "price_pro_monthly_placeholder"),
        "name": "Pro",
        "price": 2900,  # 29€ en centimes
        "credits": 1000,
        "features": ["Crédits illimités", "Génération texte & images", "Planificateur de contenu", "Support prioritaire", "+50 SaaS tokens/mois"]
    },
    "business": {
        "price_id": os.getenv("STRIPE_BUSINESS_PRICE_ID", "price_business_monthly_placeholder"),
        "name": "Business",
        "price": 9900,  # 99€ en centimes
        "credits": 5000,
        "features": ["Multi-comptes", "Export CSV/API", "Accès API", "Support dédié", "+100 SaaS tokens/mois"]
    }
}

def create_checkout_session(customer_email: str, plan_id: str, success_url: str, cancel_url: str) -> Dict:
    """
    Crée une session de paiement Stripe pour un plan d'abonnement.
    """
    if plan_id not in STRIPE_PLANS:
        return {"success": False, "error": f"Le plan '{plan_id}' est invalide."}

    plan = STRIPE_PLANS[plan_id]

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=customer_email,
            line_items=[{
                'price': plan['price_id'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=f"{success_url}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=cancel_url,
            metadata={
                'plan_id': plan_id,
                'customer_email': customer_email
            }
        )
        return {"success": True, "session_id": session.id, "url": session.url}
    except stripe.error.StripeError as e:
        return {"success": False, "error": f"Erreur Stripe: {e.user_message or str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Erreur lors de la création: {str(e)}"}

def verify_payment(session_id: str) -> Dict:
    """Vérifie le statut d'un paiement via son ID de session."""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            "status": "paid" if session.payment_status == "paid" else "pending",
            "plan_id": session.metadata.get("plan_id"),
            "customer_email": session.metadata.get("customer_email"),
            "amount": session.amount_total
        }
    except stripe.error.StripeError as e:
        return {"status": "error", "error": f"Erreur Stripe: {e.user_message or str(e)}"}
    except Exception as e:
        return {"status": "error", "error": f"Erreur de vérification: {str(e)}"}

def create_customer_portal(customer_id: str, return_url: str) -> Dict:
    """Crée un lien vers le portail client Stripe"""
    try:
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url,
        )
        return {"success": True, "url": session.url}
    except Exception as e:
        return {"success": False, "error": f"Erreur portail client: {str(e)}"}