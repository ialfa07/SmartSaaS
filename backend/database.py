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
