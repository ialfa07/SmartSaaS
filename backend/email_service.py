
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List
import asyncio
from database import db_service

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@smartsaas.com")
        
    def send_email(self, to_email: str, subject: str, body_html: str, body_text: str = None):
        """Envoie un email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            # Version texte
            if body_text:
                part1 = MIMEText(body_text, 'plain')
                msg.attach(part1)
            
            # Version HTML
            part2 = MIMEText(body_html, 'html')
            msg.attach(part2)
            
            # Envoi
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
            return {"success": True, "message": "Email envoyé avec succès"}
        except Exception as e:
            print(f"Erreur envoi email: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def send_welcome_email(self, user_email: str, user_name: str = None):
        """Email de bienvenue pour nouveaux utilisateurs"""
        name = user_name or user_email.split('@')[0]
        
        subject = "🎉 Bienvenue sur SmartSaaS - Votre aventure IA commence !"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .feature {{ margin: 15px 0; padding: 15px; background: #f8f9ff; border-radius: 5px; }}
                .footer {{ background: #f8f9fa; padding: 20px; text-align: center; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 Bienvenue sur SmartSaaS !</h1>
                    <p>Bonjour {name}, prêt à révolutionner votre marketing avec l'IA ?</p>
                </div>
                <div class="content">
                    <h2>🎁 Vos crédits de bienvenue vous attendent !</h2>
                    <p>Félicitations ! Vous avez reçu <strong>5 crédits gratuits</strong> pour commencer à générer du contenu IA dès maintenant.</p>
                    
                    <div class="feature">
                        <h3>✨ Ce que vous pouvez faire :</h3>
                        <ul>
                            <li>🤖 Générer du contenu marketing personnalisé</li>
                            <li>🎨 Créer des visuels avec DALL-E</li>
                            <li>📅 Planifier vos campagnes</li>
                            <li>🪙 Gagner des jetons SaaS et débloquer des récompenses</li>
                        </ul>
                    </div>
                    
                    <div class="feature">
                        <h3>🎯 Conseils pour bien commencer :</h3>
                        <ol>
                            <li>Essayez le générateur de contenu avec votre secteur d'activité</li>
                            <li>Explorez les différentes plateformes (Instagram, LinkedIn, Facebook)</li>
                            <li>Complétez votre profil pour gagner 10 jetons SaaS</li>
                            <li>Partagez votre code de parrainage pour gagner plus de récompenses</li>
                        </ol>
                    </div>
                    
                    <a href="https://smartsaas.com/dashboard" class="button">🚀 Commencer maintenant</a>
                </div>
                <div class="footer">
                    <p>L'équipe SmartSaaS 💜</p>
                    <p><small>Si vous avez des questions, répondez simplement à cet email !</small></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        Bienvenue sur SmartSaaS, {name} !
        
        Félicitations ! Vous avez reçu 5 crédits gratuits pour commencer.
        
        Ce que vous pouvez faire :
        - Générer du contenu marketing personnalisé
        - Créer des visuels avec DALL-E
        - Planifier vos campagnes
        - Gagner des jetons SaaS
        
        Commencez maintenant : https://smartsaas.com/dashboard
        
        L'équipe SmartSaaS
        """
        
        return self.send_email(user_email, subject, html_body, text_body)
    
    def send_daily_reminder(self, user_email: str, credits_left: int):
        """Rappel quotidien pour utilisateurs inactifs"""
        subject = "💡 Votre dose quotidienne d'inspiration marketing vous attend !"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .stats {{ background: #f8f9ff; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌟 Bonjour !</h1>
                    <p>Il est temps de booster votre marketing avec l'IA</p>
                </div>
                
                <div class="stats">
                    <h3>📊 Votre tableau de bord :</h3>
                    <p>💳 Crédits disponibles : <strong>{credits_left}</strong></p>
                    <p>🪙 Réclamez votre récompense quotidienne : <strong>+1 jeton SaaS</strong></p>
                </div>
                
                <h3>💡 Idée du jour :</h3>
                <p>Créez du contenu pour 3 plateformes différentes avec le même thème pour maximiser votre portée !</p>
                
                <a href="https://smartsaas.com/dashboard" class="button">🚀 Générer du contenu</a>
                
                <p><small>Vous recevez cet email car vous n'avez pas utilisé SmartSaaS aujourd'hui. Vous pouvez vous désabonner à tout moment.</small></p>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_body)
    
    def send_token_reward_notification(self, user_email: str, reward_amount: int, reason: str, new_balance: int):
        """Notification de récompense en jetons"""
        subject = f"🎉 +{reward_amount} jetons SaaS gagnés !"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; text-align: center; }}
                .reward {{ background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); padding: 30px; border-radius: 10px; margin: 20px 0; }}
                .balance {{ background: #f8f9ff; padding: 20px; border-radius: 10px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎉 Félicitations !</h1>
                
                <div class="reward">
                    <h2>+{reward_amount} jetons SaaS</h2>
                    <p><strong>Raison :</strong> {reason}</p>
                </div>
                
                <div class="balance">
                    <h3>💰 Nouveau solde : {new_balance} jetons</h3>
                    <p>Utilisez vos jetons pour :</p>
                    <ul style="text-align: left; display: inline-block;">
                        <li>🔄 Échanger contre des crédits IA (50 jetons = 1 crédit)</li>
                        <li>🎁 Débloquer des fonctionnalités premium</li>
                        <li>🏆 Grimper dans le classement</li>
                    </ul>
                </div>
                
                <a href="https://smartsaas.com/tokens" style="display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">
                    Voir mes jetons
                </a>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_body)
    
    def send_referral_success(self, user_email: str, referred_email: str, reward: int):
        """Email de succès de parrainage"""
        subject = "🎊 Parrainage réussi - Récompense débloquée !"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; text-align: center; }}
                .success {{ background: linear-gradient(135deg, #a8e6cf 0%, #dcedc1 100%); padding: 30px; border-radius: 10px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🎊 Parrainage réussi !</h1>
                
                <div class="success">
                    <h2>+{reward} jetons SaaS</h2>
                    <p>Merci d'avoir invité <strong>{referred_email}</strong> !</p>
                </div>
                
                <p>Continuez à partager votre code de parrainage pour gagner plus de récompenses :</p>
                <ul style="text-align: left; display: inline-block;">
                    <li>👤 +25 jetons par inscription</li>
                    <li>💳 +50 jetons si votre filleul fait un achat</li>
                </ul>
                
                <a href="https://smartsaas.com/referral" style="display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">
                    Voir mes parrainages
                </a>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_body)
    
    def send_weekly_report(self, user_email: str, stats: Dict):
        """Rapport hebdomadaire d'activité"""
        subject = "📊 Votre rapport hebdomadaire SmartSaaS"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background: white; border-radius: 10px; padding: 30px; }}
                .stat {{ background: #f8f9ff; padding: 15px; margin: 10px 0; border-radius: 5px; display: flex; justify-content: space-between; }}
                .highlight {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; text-align: center; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Votre semaine en chiffres</h1>
                
                <div class="highlight">
                    <h2>🏆 Vous avez généré {stats.get('total_content', 0)} contenus cette semaine !</h2>
                </div>
                
                <h3>📈 Détails de votre activité :</h3>
                
                <div class="stat">
                    <span>🤖 Générations de texte :</span>
                    <strong>{stats.get('text_generations', 0)}</strong>
                </div>
                
                <div class="stat">
                    <span>🎨 Images créées :</span>
                    <strong>{stats.get('image_generations', 0)}</strong>
                </div>
                
                <div class="stat">
                    <span>🪙 Jetons SaaS gagnés :</span>
                    <strong>+{stats.get('tokens_earned', 0)}</strong>
                </div>
                
                <div class="stat">
                    <span>👥 Nouveaux parrainages :</span>
                    <strong>{stats.get('new_referrals', 0)}</strong>
                </div>
                
                <h3>🎯 Objectif de la semaine prochaine :</h3>
                <p>Essayez de générer du contenu pour 5 plateformes différentes pour diversifier votre stratégie marketing !</p>
                
                <a href="https://smartsaas.com/dashboard" style="display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">
                    Continuer à créer
                </a>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, html_body)

# Instance globale du service email
email_service = EmailService()

# Tâches automatisées
async def send_daily_reminders():
    """Envoie des rappels quotidiens aux utilisateurs inactifs"""
    inactive_users = db_service.get_inactive_users(days=2)  # Inactifs depuis 2 jours
    
    for user in inactive_users:
        await asyncio.sleep(1)  # Éviter le spam
        email_service.send_daily_reminder(user.email, user.credits)
        print(f"Rappel envoyé à {user.email}")

async def send_weekly_reports():
    """Envoie les rapports hebdomadaires"""
    all_users = db_service.get_all_active_users()
    
    for user in all_users:
        stats = db_service.get_user_weekly_stats(user.id)
        if stats['total_content'] > 0:  # Seulement pour les utilisateurs actifs
            await asyncio.sleep(1)
            email_service.send_weekly_report(user.email, stats)
            print(f"Rapport hebdomadaire envoyé à {user.email}")
