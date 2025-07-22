import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
from jinja2 import Environment, FileSystemLoader
from database import db_service
from config import settings

class EmailService:
    def __init__(self):
        # Configuration SMTP centralisée via settings
        self.smtp_server = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = f"SmartSaaS <{os.getenv('FROM_EMAIL', 'noreply@smartsaas.com')}>"

        # Configuration Jinja2 pour les templates
        template_dir = os.path.join(os.path.dirname(__file__), 'templates')
        os.makedirs(template_dir, exist_ok=True)  # Créer le dossier s'il n'existe pas
        self.env = Environment(loader=FileSystemLoader(template_dir))

        # URLs de base pour les templates
        self.base_urls = {
            'dashboard': os.getenv('FRONTEND_URL', 'https://smartsaas.com') + '/dashboard',
            'tokens': os.getenv('FRONTEND_URL', 'https://smartsaas.com') + '/tokens',
            'referral': os.getenv('FRONTEND_URL', 'https://smartsaas.com') + '/referral'
        }

    async def send_email_async(self, to_email: str, subject: str, body_html: str, body_text: str = None):
        """Envoie un email de manière asynchrone"""
        try:
            # Créer le message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email

            # Version texte
            if body_text:
                part1 = MIMEText(body_text, 'plain', 'utf-8')
                msg.attach(part1)

            # Version HTML
            part2 = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(part2)

            # Envoi dans un thread pour ne pas bloquer FastAPI
            def send_smtp():
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
                server.quit()

            # Exécuter dans un thread séparé
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, send_smtp)

            return {"success": True, "message": "Email envoyé avec succès"}
        except Exception as e:
            print(f"Erreur envoi email: {str(e)}")
            return {"success": False, "error": str(e)}

    def send_email(self, to_email: str, subject: str, body_html: str, body_text: str = None):
        """Version synchrone pour compatibilité"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email

            if body_text:
                part1 = MIMEText(body_text, 'plain', 'utf-8')
                msg.attach(part1)

            part2 = MIMEText(body_html, 'html', 'utf-8')
            msg.attach(part2)

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()

            return {"success": True, "message": "Email envoyé avec succès"}
        except Exception as e:
            print(f"Erreur envoi email: {str(e)}")
            return {"success": False, "error": str(e)}

    def render_template(self, template_name: str, **kwargs):
        """Rend un template avec les variables fournies"""
        try:
            template = self.env.get_template(template_name)
            return template.render(**kwargs, **self.base_urls)
        except Exception as e:
            print(f"Erreur rendu template {template_name}: {str(e)}")
            return None

    async def send_welcome_email(self, user_email: str, user_name: str = None):
        """Email de bienvenue pour nouveaux utilisateurs"""
        name = user_name or user_email.split('@')[0]
        subject = "🎉 Bienvenue sur SmartSaaS - Votre aventure IA commence !"

        template_vars = {
            "name": name,
            "dashboard_url": self.base_urls['dashboard']
        }

        # Rendre les templates
        html_body = self.render_template('welcome_email.html', **template_vars)
        text_body = self.render_template('welcome_email.txt', **template_vars)

        if html_body and text_body:
            return await self.send_email_async(user_email, subject, html_body, text_body)
        else:
            # Fallback si templates non trouvés
            return self.send_email(user_email, subject, 
                f"<h1>Bienvenue {name} sur SmartSaaS !</h1><p>Votre aventure IA commence maintenant.</p>",
                f"Bienvenue {name} sur SmartSaaS ! Votre aventure IA commence maintenant.")

    async def send_daily_reminder(self, user_email: str, credits_left: int):
        """Rappel quotidien pour utilisateurs inactifs"""
        subject = "💡 Votre dose quotidienne d'inspiration marketing vous attend !"

        template_vars = {
            "credits_left": credits_left,
            "dashboard_url": self.base_urls['dashboard']
        }

        html_body = self.render_template('daily_reminder.html', **template_vars)

        if html_body:
            return await self.send_email_async(user_email, subject, html_body)
        else:
            # Fallback simple
            return await self.send_email_async(user_email, subject,
                f"<h1>Bonjour !</h1><p>Vous avez {credits_left} crédits disponibles. Créez du contenu dès maintenant !</p>")

    async def send_token_reward_notification(self, user_email: str, reward_amount: int, reason: str, new_balance: int):
        """Notification de récompense en jetons"""
        subject = f"🎉 +{reward_amount} jetons SaaS gagnés !"

        template_vars = {
            "reward_amount": reward_amount,
            "reason": reason,
            "new_balance": new_balance,
            "tokens_url": self.base_urls['tokens']
        }

        html_body = self.render_template('token_reward.html', **template_vars)

        if html_body:
            return await self.send_email_async(user_email, subject, html_body)
        else:
            return await self.send_email_async(user_email, subject,
                f"<h1>+{reward_amount} jetons SaaS !</h1><p>Raison: {reason}<br>Nouveau solde: {new_balance}</p>")

    async def send_referral_success(self, user_email: str, referred_email: str, reward: int):
        """Email de succès de parrainage"""
        subject = "🎊 Parrainage réussi - Récompense débloquée !"

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 30px; text-align: center;">
            <h1>🎊 Parrainage réussi !</h1>
            <div style="background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%); padding: 30px; border-radius: 10px; margin: 20px 0;">
                <h2>+{reward} jetons SaaS</h2>
                <p>Merci d'avoir invité <strong>{referred_email}</strong> !</p>
            </div>
            <p>Continuez à partager votre code de parrainage pour gagner plus de récompenses :</p>
            <ul style="text-align: left; display: inline-block;">
                <li>👤 +25 jetons par inscription</li>
                <li>💳 +50 jetons si votre filleul fait un achat</li>
            </ul>
            <a href="{self.base_urls['referral']}" style="display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">
                Voir mes parrainages
            </a>
        </div>
        """

        return await self.send_email_async(user_email, subject, html_body)

    async def send_weekly_report(self, user_email: str, stats: Dict):
        """Rapport hebdomadaire d'activité"""
        subject = "📊 Votre rapport hebdomadaire SmartSaaS"

        html_body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 30px;">
            <h1>📊 Votre semaine en chiffres</h1>

            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                <h2>🏆 Vous avez généré {stats.get('total_content', 0)} contenus cette semaine !</h2>
            </div>

            <h3>📈 Détails de votre activité :</h3>

            <div style="background: #f8f9ff; padding: 15px; margin: 10px 0; border-radius: 5px; display: flex; justify-content: space-between;">
                <span>🤖 Générations de texte :</span>
                <strong>{stats.get('text_generations', 0)}</strong>
            </div>

            <div style="background: #f8f9ff; padding: 15px; margin: 10px 0; border-radius: 5px; display: flex; justify-content: space-between;">
                <span>🎨 Images créées :</span>
                <strong>{stats.get('image_generations', 0)}</strong>
            </div>

            <div style="background: #f8f9ff; padding: 15px; margin: 10px 0; border-radius: 5px; display: flex; justify-content: space-between;">
                <span>🪙 Jetons SaaS gagnés :</span>
                <strong>+{stats.get('tokens_earned', 0)}</strong>
            </div>

            <div style="background: #f8f9ff; padding: 15px; margin: 10px 0; border-radius: 5px; display: flex; justify-content: space-between;">
                <span>👥 Nouveaux parrainages :</span>
                <strong>{stats.get('new_referrals', 0)}</strong>
            </div>

            <h3>🎯 Objectif de la semaine prochaine :</h3>
            <p>Essayez de générer du contenu pour 5 plateformes différentes pour diversifier votre stratégie marketing !</p>

            <a href="{self.base_urls['dashboard']}" style="display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">
                Continuer à créer
            </a>
        </div>
        """

        return await self.send_email_async(user_email, subject, html_body)

# Instance globale du service email
email_service = EmailService()

# Tâches automatisées asynchrones
async def send_daily_reminders():
    """Envoie des rappels quotidiens aux utilisateurs inactifs"""
    try:
        inactive_users = db_service.get_inactive_users(days=2)

        for user in inactive_users:
            await asyncio.sleep(1)  # Éviter le spam
            await email_service.send_daily_reminder(user.email, user.credits)
            print(f"✅ Rappel envoyé à {user.email}")

        print(f"📧 {len(inactive_users)} rappels quotidiens envoyés")
    except Exception as e:
        print(f"❌ Erreur envoi rappels quotidiens: {str(e)}")

async def send_weekly_reports():
    """Envoie les rapports hebdomadaires"""
    try:
        all_users = db_service.get_all_active_users()
        reports_sent = 0

        for user in all_users:
            stats = db_service.get_user_weekly_stats(user.id)
            if stats.get('total_content', 0) > 0:  # Seulement pour les utilisateurs actifs
                await asyncio.sleep(1)
                await email_service.send_weekly_report(user.email, stats)
                reports_sent += 1
                print(f"✅ Rapport hebdomadaire envoyé à {user.email}")

        print(f"📊 {reports_sent} rapports hebdomadaires envoyés")
    except Exception as e:
        print(f"❌ Erreur envoi rapports hebdomadaires: {str(e)}")