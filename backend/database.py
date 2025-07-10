# Simulation d'une base de données en mémoire

fake_user_db = {
    "test@example.com": {
        "email": "test@example.com",
        "password": "123456",
        "credits": 50,
        "plan": "free",
        "created_at": "2024-01-01"
    },
    "premium@example.com": {
        "email": "premium@example.com", 
        "password": "premium123",
        "credits": 500,
        "plan": "pro",
        "created_at": "2024-01-01"
    }
}

def get_user(email: str):
    """Récupère un utilisateur par email"""
    return fake_user_db.get(email)

def update_user_credits(email: str, credits: int):
    """Met à jour les crédits d'un utilisateur"""
    if email in fake_user_db:
        fake_user_db[email]["credits"] = credits
        return True
    return False

def add_credits(email: str, amount: int):
    """Ajoute des crédits à un utilisateur"""
    if email in fake_user_db:
        fake_user_db[email]["credits"] += amount
        return True
    return False

def subtract_credits(email: str, amount: int):
    """Soustrait des crédits à un utilisateur"""
    if email in fake_user_db:
        if fake_user_db[email]["credits"] >= amount:
            fake_user_db[email]["credits"] -= amount
            return True
    return False