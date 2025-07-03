# users.py

from models import User
from database import fake_user_db

def authenticate_user(email: str, password: str) -> User | None:
    user = fake_user_db.get(email)
    if user and user["password"] == password:
        return User(email=email)
    return None

def create_user(email: str, password: str) -> User | None:
    if email in fake_user_db:
        return None
    fake_user_db[email] = {"email": email, "password": password, "credits": 5}
    return User(email=email)
