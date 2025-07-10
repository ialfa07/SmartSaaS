from sqlalchemy.orm import Session
from models import User, SaasToken, Payment, SessionLocal
from passlib.context import CryptContext
from datetime import datetime
import secrets
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DatabaseService:
    def __init__(self):
        self.db = SessionLocal()

    def get_inactive_users(self, days: int = 2):
        """Récupère les utilisateurs inactifs depuis X jours"""
        from datetime import datetime, timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Simulation pour la démo
        return []

    def get_all_active_users(self):
        """Récupère tous les utilisateurs actifs"""
        return self.db.query(User).filter(User.is_active == True).all()

    def get_user_weekly_stats(self, user_id: int):
        """Statistiques hebdomadaires d'un utilisateur"""
        # Simulation pour la démo
        return {
            "total_content": 5,
            "text_generations": 3,
            "image_generations": 2,
            "tokens_earned": 15,
            "new_referrals": 1
        }

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def create_user(self, email: str, password: str) -> User:
        # Générer un code de parrainage unique
        referral_code = self.generate_referral_code()

        hashed_password = pwd_context.hash(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            referral_code=referral_code,
            credits=5,  # Crédits gratuits
            plan="free"
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        # Ajouter des jetons de bienvenue
        self.add_saas_tokens(user.id, 10, "welcome_bonus", "Bonus de bienvenue")

        return user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def update_user_credits(self, user_id: int, credits: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            user.credits = credits
            self.db.commit()
            return True
        return False

    def add_credits(self, user_id: int, amount: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            user.credits += amount
            self.db.commit()
            return True
        return False

    def spend_credits(self, user_id: int, amount: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user and user.credits >= amount:
            user.credits -= amount
            self.db.commit()
            return True
        return False

    def get_user_saas_tokens(self, user_id: int) -> dict:
        """Récupère le solde et l'historique des jetons SaaS"""
        tokens = self.db.query(SaasToken).filter(SaasToken.user_id == user_id).all()

        balance = 0
        total_earned = 0
        history = []

        for token in tokens:
            if token.transaction_type in ["earned", "daily_login", "referral_signup", "referral_first_purchase", "welcome_bonus"]:
                balance += token.amount
                total_earned += token.amount
            elif token.transaction_type == "spent":
                balance -= token.amount

            history.append({
                "amount": token.amount,
                "type": token.transaction_type,
                "description": token.description,
                "date": token.created_at
            })

        return {
            "balance": balance,
            "total_earned": total_earned,
            "history": sorted(history, key=lambda x: x["date"], reverse=True)
        }

    def add_saas_tokens(self, user_id: int, amount: int, transaction_type: str, description: str = "") -> bool:
        """Ajoute des jetons SaaS à un utilisateur"""
        token = SaasToken(
            user_id=user_id,
            amount=amount,
            transaction_type=transaction_type,
            description=description
        )
        self.db.add(token)
        self.db.commit()
        return True

    def spend_saas_tokens(self, user_id: int, amount: int, description: str = "") -> bool:
        """Dépense des jetons SaaS"""
        user_tokens = self.get_user_saas_tokens(user_id)
        if user_tokens["balance"] >= amount:
            token = SaasToken(
                user_id=user_id,
                amount=amount,
                transaction_type="spent",
                description=description
            )
            self.db.add(token)
            self.db.commit()
            return True
        return False

    def get_referral_info(self, user_id: int) -> dict:
        """Récupère les informations de parrainage"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        # Compter les utilisateurs parrainés
        referred_users = self.db.query(User).filter(User.referred_by == user.referral_code).all()

        return {
            "referral_code": user.referral_code,
            "total_referrals": len(referred_users),
            "referred_users": [{"email": u.email, "created_at": u.created_at} for u in referred_users]
        }

    def process_referral(self, referrer_user_id: int, referred_email: str) -> dict:
        """Traite un nouveau parrainage"""
        referrer = self.get_user_by_id(referrer_user_id)
        referred = self.get_user_by_email(referred_email)

        if not referrer or not referred:
            return {"success": False, "error": "Utilisateur non trouvé"}

        if referred.referred_by:
            return {"success": False, "error": "Cet utilisateur a déjà été parrainé"}

        # Marquer l'utilisateur comme parrainé
        referred.referred_by = referrer.referral_code
        self.db.commit()

        # Récompenser le parrain
        self.add_saas_tokens(referrer_user_id, 25, "referral_signup", f"Parrainage de {referred_email}")

        return {
            "success": True,
            "referrer_reward": 25,
            "referrer_balance": self.get_user_saas_tokens(referrer_user_id)["balance"]
        }

    def get_leaderboard(self, limit: int = 10) -> list:
        """Récupère le classement des utilisateurs par jetons gagnés"""
        users = self.db.query(User).all()
        leaderboard = []

        for user in users:
            tokens_data = self.get_user_saas_tokens(user.id)
            leaderboard.append({
                "email": user.email,
                "total_earned": tokens_data["total_earned"],
                "balance": tokens_data["balance"]
            })

        return sorted(leaderboard, key=lambda x: x["total_earned"], reverse=True)[:limit]

    def generate_referral_code(self) -> str:
        """Génère un code de parrainage unique"""
        while True:
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            if not self.db.query(User).filter(User.referral_code == code).first():
                return code

    def update_user_wallet(self, user_id: int, wallet_address: str) -> bool:
        """Met à jour l'adresse de portefeuille Web3 d'un utilisateur"""
        user = self.get_user_by_id(user_id)
        if user:
            # Ajouter une colonne wallet_address à la table users si nécessaire
            # Pour l'instant, on utilise un champ existant ou on l'ajoute
            try:
                # Cette requête nécessite d'avoir ajouté la colonne wallet_address
                user.wallet_address = wallet_address
                self.db.commit()
                return True
            except Exception as e:
                print(f"Error updating wallet address: {e}")
                self.db.rollback()
                return False
        return False

    def get_user_wallet(self, user_id: int) -> str:
        """Récupère l'adresse de portefeuille Web3 d'un utilisateur"""
        user = self.get_user_by_id(user_id)
        if user:
            return user.wallet_address
        return None

    def close(self):
        self.db.close()

# Instance globale
db_service = DatabaseService()