from fastapi import Depends, HTTPException
from models import User

# Simule une "base de données" avec 1 utilisateur
users_db = {
    "test@example.com": {"email": "test@example.com", "password": "123456", "credits": 5}
}

def fake_auth(email: str = "test@example.com"):
    if email in users_db:
        return User(email=email)
    raise HTTPException(status_code=401, detail="Unauthorized")
