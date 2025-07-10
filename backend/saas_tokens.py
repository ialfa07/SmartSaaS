
from typing import Dict, List
import datetime

# Base de données des jetons SaaS en mémoire
user_tokens = {
    "test@example.com": {
        "balance": 100,
        "total_earned": 100,
        "history": [
            {"date": "2024-01-01", "action": "welcome_bonus", "amount": 100, "type": "earned"}
        ]
    }
}

# Base de données des parrainages
referrals = {
    "test@example.com": {
        "referred_users": [],
        "referral_code": "TEST2024",
        "total_referrals": 0
    }
}

# Récompenses par action
TOKEN_REWARDS = {
    "welcome_bonus": 100,
    "daily_login": 10,
    "first_generation": 25,
    "share_content": 15,
    "complete_profile": 50,
    "referral_signup": 100,
    "referral_first_purchase": 200,
    "weekly_active": 30,
    "content_viral": 75,
    "feedback_provided": 20
}

def get_user_tokens(email: str) -> Dict:
    """Récupère le solde de jetons d'un utilisateur"""
    if email not in user_tokens:
        user_tokens[email] = {
            "balance": 0,
            "total_earned": 0,
            "history": []
        }
    return user_tokens[email]

def add_tokens(email: str, amount: int, action: str) -> Dict:
    """Ajoute des jetons à un utilisateur"""
    if email not in user_tokens:
        user_tokens[email] = {"balance": 0, "total_earned": 0, "history": []}
    
    user_tokens[email]["balance"] += amount
    user_tokens[email]["total_earned"] += amount
    user_tokens[email]["history"].append({
        "date": datetime.datetime.now().isoformat(),
        "action": action,
        "amount": amount,
        "type": "earned"
    })
    
    return user_tokens[email]

def spend_tokens(email: str, amount: int, action: str) -> bool:
    """Dépense des jetons"""
    if email not in user_tokens:
        return False
    
    if user_tokens[email]["balance"] >= amount:
        user_tokens[email]["balance"] -= amount
        user_tokens[email]["history"].append({
            "date": datetime.datetime.now().isoformat(),
            "action": action,
            "amount": -amount,
            "type": "spent"
        })
        return True
    return False

def get_referral_info(email: str) -> Dict:
    """Récupère les informations de parrainage"""
    if email not in referrals:
        import random
        code = f"{email[:4].upper()}{random.randint(1000, 9999)}"
        referrals[email] = {
            "referred_users": [],
            "referral_code": code,
            "total_referrals": 0
        }
    return referrals[email]

def process_referral(referrer_email: str, referred_email: str) -> Dict:
    """Traite un nouveau parrainage"""
    if referrer_email not in referrals:
        get_referral_info(referrer_email)  # Initialise si nécessaire
    
    # Ajoute le nouvel utilisateur référé
    referrals[referrer_email]["referred_users"].append({
        "email": referred_email,
        "date": datetime.datetime.now().isoformat(),
        "status": "pending"
    })
    referrals[referrer_email]["total_referrals"] += 1
    
    # Récompense le parrain
    reward = add_tokens(referrer_email, TOKEN_REWARDS["referral_signup"], "referral_signup")
    
    # Bonus pour le nouveau membre
    add_tokens(referred_email, 50, "welcome_referral")
    
    return {
        "success": True,
        "referrer_reward": TOKEN_REWARDS["referral_signup"],
        "referred_reward": 50,
        "referrer_balance": reward["balance"]
    }

def get_leaderboard(limit: int = 10) -> List[Dict]:
    """Récupère le classement des utilisateurs"""
    leaderboard = []
    for email, data in user_tokens.items():
        leaderboard.append({
            "email": email[:3] + "***",  # Anonymise l'email
            "total_earned": data["total_earned"],
            "current_balance": data["balance"]
        })
    
    # Trie par total gagné
    leaderboard.sort(key=lambda x: x["total_earned"], reverse=True)
    return leaderboard[:limit]

def calculate_level(total_earned: int) -> Dict:
    """Calcule le niveau et les badges d'un utilisateur"""
    levels = [
        {"name": "Débutant", "min_tokens": 0, "max_tokens": 99, "badge": "🌱"},
        {"name": "Actif", "min_tokens": 100, "max_tokens": 499, "badge": "⭐"},
        {"name": "Expert", "min_tokens": 500, "max_tokens": 1499, "badge": "🏆"},
        {"name": "Maître", "min_tokens": 1500, "max_tokens": 4999, "badge": "💎"},
        {"name": "Légende", "min_tokens": 5000, "max_tokens": float('inf'), "badge": "👑"}
    ]
    
    for level in levels:
        if level["min_tokens"] <= total_earned <= level["max_tokens"]:
            progress = min(100, (total_earned - level["min_tokens"]) / (level["max_tokens"] - level["min_tokens"]) * 100)
            return {
                "level": level["name"],
                "badge": level["badge"],
                "progress": progress,
                "current_tokens": total_earned,
                "next_level_tokens": level["max_tokens"] + 1 if level["max_tokens"] != float('inf') else None
            }
    
    return levels[0]  # Par défaut : Débutant
