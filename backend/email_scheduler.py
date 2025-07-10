
import asyncio
import schedule
import time
from datetime import datetime
import threading
from email_service import email_service, send_daily_reminders, send_weekly_reports

class EmailScheduler:
    def __init__(self):
        self.running = False
        
    def start_scheduler(self):
        """Démarre le planificateur d'emails"""
        self.running = True
        
        # Planifier les emails quotidiens à 10h
        schedule.every().day.at("10:00").do(self.run_daily_reminders)
        
        # Planifier les rapports hebdomadaires le lundi à 9h
        schedule.every().monday.at("09:00").do(self.run_weekly_reports)
        
        # Démarrer le planificateur dans un thread séparé
        scheduler_thread = threading.Thread(target=self._run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        
        print("📧 Planificateur d'emails démarré !")
    
    def _run_scheduler(self):
        """Exécute le planificateur en arrière-plan"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Vérifier chaque minute
    
    def run_daily_reminders(self):
        """Lance les rappels quotidiens"""
        print("📧 Envoi des rappels quotidiens...")
        asyncio.create_task(send_daily_reminders())
    
    def run_weekly_reports(self):
        """Lance les rapports hebdomadaires"""
        print("📊 Envoi des rapports hebdomadaires...")
        asyncio.create_task(send_weekly_reports())
    
    def stop_scheduler(self):
        """Arrête le planificateur"""
        self.running = False
        print("📧 Planificateur d'emails arrêté.")

# Instance globale
email_scheduler = EmailScheduler()

# Fonctions pour démarrer/arrêter
def start_email_automation():
    """Démarre l'automatisation des emails"""
    email_scheduler.start_scheduler()

def stop_email_automation():
    """Arrête l'automatisation des emails"""
    email_scheduler.stop_scheduler()
