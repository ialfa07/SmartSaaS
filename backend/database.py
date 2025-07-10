# database.py

# Pour MVP local : pas de vraie BDD, tout est en mémoire
# Ici tu peux plus tard intégrer SQLite, PostgreSQL ou Supabase

from typing import Dict

# Structure type base utilisateur
fake_user_db: Dict[str, dict] = {
    "test@example.com": {
        "email": "test@example.com",
        "password": "123456",
        "credits": 5
    }
}

def get_user(email: str):
    return fake_user_db.get(email)

def update_credits(email: str, amount: int):
    if email in fake_user_db:
        fake_user_db[email]["credits"] += amount
# Simulation d'une base de données pour la démo
from typing import Dict, List

# Base de données simulée pour les utilisateurs
fake_user_db: Dict[str, dict] = {
    "test@example.com": {
        "email": "test@example.com",
        "password": "123456",
        "credits": 50,
        "plan": "free",
        "created_at": "2024-01-01",
        "last_login": "2024-01-15"
    }
}

# Base de données simulée pour les transactions
fake_transactions_db: List[dict] = [
    {
        "id": "txn_001",
        "user_email": "test@example.com",
        "plan": "starter",
        "amount": 9,
        "status": "completed",
        "created_at": "2024-01-01"
    }
]

def get_user(email: str) -> dict:
    """Récupère un utilisateur"""
    return fake_user_db.get(email)

def update_user(email: str, data: dict) -> bool:
    """Met à jour un utilisateur"""
    if email in fake_user_db:
        fake_user_db[email].update(data)
        return True
    return False

def add_transaction(transaction: dict) -> str:
    """Ajoute une transaction"""
    transaction_id = f"txn_{len(fake_transactions_db) + 1:03d}"
    transaction["id"] = transaction_id
    fake_transactions_db.append(transaction)
    return transaction_id

def get_user_transactions(email: str) -> List[dict]:
    """Récupère les transactions d'un utilisateur"""
    return [txn for txn in fake_transactions_db if txn["user_email"] == email]
