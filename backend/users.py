
# Module de gestion des utilisateurs
from typing import Dict

# Base de données simulée
users_database: Dict[str, dict] = {
    "test@example.com": {
        "email": "test@example.com",
        "password": "123456",
        "credits": 50,
        "plan": "free"
    }
}

def get_user_by_email(email: str):
    return users_database.get(email)

def update_user_credits(email: str, credits: int):
    if email in users_database:
        users_database[email]["credits"] = credits

def add_user_credits(email: str, credits: int):
    if email in users_database:
        users_database[email]["credits"] += credits
