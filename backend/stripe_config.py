
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
import stripe
import os
from typing import Dict

# Configuration Stripe (vous devrez ajouter vos vraies clés dans les secrets)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', 'sk_test_fake_key_for_demo')

# Plans disponibles
STRIPE_PLANS = {
    "starter": {
        "name": "Starter",
        "price": 9,
        "credits": 100,
        "features": [
            "100 crédits/mois",
            "Génération de texte IA",
            "Support email"
        ],
        "stripe_price_id": "price_1234starter"
    },
    "pro": {
        "name": "Pro", 
        "price": 29,
        "credits": 500,
        "features": [
            "500 crédits/mois",
            "Génération texte + images",
            "Calendrier de contenu",
            "Support prioritaire"
        ],
        "stripe_price_id": "price_1234pro"
    },
    "enterprise": {
        "name": "Enterprise",
        "price": 99,
        "credits": 2000,
        "features": [
            "2000 crédits/mois",
            "Toutes les fonctionnalités",
            "API accès",
            "Support dédié"
        ],
        "stripe_price_id": "price_1234enterprise"
    }
}

def create_checkout_session(user_email: str, plan_id: str) -> Dict:
    """Crée une session de checkout Stripe"""
    try:
        if plan_id not in STRIPE_PLANS:
            raise ValueError("Plan non valide")
        
        plan = STRIPE_PLANS[plan_id]
        
        # En mode démo, on simule une session Stripe
        session = {
            "id": f"cs_test_demo_{plan_id}_{user_email}",
            "url": f"https://checkout.stripe.com/pay/demo#{plan_id}",
            "success_url": "http://localhost:3000/success",
            "cancel_url": "http://localhost:3000/pricing"
        }
        
        return session
        
    except Exception as e:
        raise Exception(f"Erreur création session: {str(e)}")

def verify_payment(session_id: str) -> Dict:
    """Vérifie le statut d'un paiement"""
    try:
        # En mode démo, on simule la vérification
        if "demo" in session_id:
            plan_id = session_id.split("_")[3]
            return {
                "status": "paid",
                "plan_id": plan_id,
                "amount": STRIPE_PLANS[plan_id]["price"]
            }
        else:
            # En production, utilisez stripe.checkout.Session.retrieve(session_id)
            return {"status": "unpaid"}
            
    except Exception as e:
        raise Exception(f"Erreur vérification: {str(e)}")
import stripe
import os
from typing import Dict

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

STRIPE_PLANS = {
    "starter": {
        "price_id": "price_starter_monthly",
        "name": "Starter",
        "price": 900,  # 9€ en centimes
        "credits": 100,
        "features": ["100 générations IA", "Support email", "Jetons SaaS bonus"]
    },
    "pro": {
        "price_id": "price_pro_monthly", 
        "name": "Pro",
        "price": 2900,  # 29€ en centimes
        "credits": 1000,
        "features": ["Générations illimitées", "Branding personnalisé", "Support prioritaire", "API access"]
    },
    "business": {
        "price_id": "price_business_monthly",
        "name": "Business", 
        "price": 9900,  # 99€ en centimes
        "credits": 5000,
        "features": ["Multi-comptes", "Export CSV/API", "Jetons SaaS premium", "Support dédié"]
    }
}

def create_checkout_session(customer_email: str, plan_id: str) -> Dict:
    """Crée une session de paiement Stripe"""
    try:
        plan = STRIPE_PLANS[plan_id]
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=customer_email,
            line_items=[{
                'price': plan['price_id'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url='https://yourdomain.com/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='https://yourdomain.com/pricing',
            metadata={
                'plan_id': plan_id,
                'customer_email': customer_email
            }
        )
        
        return {
            "success": True,
            "session_id": session.id,
            "url": session.url
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def verify_payment(session_id: str) -> Dict:
    """Vérifie le statut d'un paiement"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        
        return {
            "status": "paid" if session.payment_status == "paid" else "pending",
            "plan_id": session.metadata.get("plan_id"),
            "customer_email": session.metadata.get("customer_email"),
            "amount": session.amount_total
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
