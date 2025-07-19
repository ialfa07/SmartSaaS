
import asyncio
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import schedule
import threading
from logger import logger
from database import db_service

class AutomationService:
    def __init__(self):
        self.active_automations = {}
        self.scheduler_running = False
        
    def create_automation(self, user_id: int, name: str, config: Dict) -> Dict:
        """Crée une nouvelle automatisation"""
        try:
            automation_data = {
                "id": f"auto_{user_id}_{int(datetime.now().timestamp())}",
                "user_id": user_id,
                "name": name,
                "config": config,
                "created_at": datetime.now().isoformat(),
                "is_active": True,
                "last_run": None,
                "next_run": None
            }
            
            # Sauvegarder en base de données
            automation_id = db_service.create_automation(automation_data)
            automation_data["db_id"] = automation_id
            
            # Programmer l'automatisation
            self.schedule_automation(automation_data)
            
            return {
                "success": True,
                "automation_id": automation_data["id"],
                "message": f"Automatisation '{name}' créée avec succès"
            }
            
        except Exception as e:
            logger.error(f"Erreur création automatisation: {e}")
            return {"success": False, "error": str(e)}
    
    def schedule_automation(self, automation: Dict):
        """Programme une automatisation"""
        try:
            config = automation["config"]
            trigger_type = config.get("trigger", {}).get("type", "manual")
            
            if trigger_type == "schedule":
                frequency = config["trigger"].get("frequency", "daily")
                time_str = config["trigger"].get("time", "09:00")
                
                if frequency == "daily":
                    schedule.every().day.at(time_str).do(
                        self.run_automation, automation["id"]
                    )
                elif frequency == "weekly":
                    day = config["trigger"].get("day", "monday")
                    getattr(schedule.every(), day).at(time_str).do(
                        self.run_automation, automation["id"]
                    )
                elif frequency == "hourly":
                    schedule.every().hour.do(
                        self.run_automation, automation["id"]
                    )
                
                self.active_automations[automation["id"]] = automation
                logger.info(f"Automatisation {automation['id']} programmée")
                
        except Exception as e:
            logger.error(f"Erreur programmation automatisation: {e}")
    
    def run_automation(self, automation_id: str):
        """Exécute une automatisation"""
        try:
            if automation_id not in self.active_automations:
                logger.error(f"Automatisation {automation_id} non trouvée")
                return
            
            automation = self.active_automations[automation_id]
            config = automation["config"]
            actions = config.get("actions", [])
            
            logger.info(f"Exécution automatisation {automation_id}")
            
            results = []
            for action in actions:
                result = self.execute_action(action, automation["user_id"])
                results.append(result)
                
                # Arrêter si une action échoue et que stop_on_error est True
                if not result["success"] and config.get("stop_on_error", False):
                    break
            
            # Mettre à jour la dernière exécution
            automation["last_run"] = datetime.now().isoformat()
            db_service.update_automation_last_run(automation["db_id"])
            
            # Récompenser l'utilisateur pour l'automatisation réussie
            if all(r["success"] for r in results):
                db_service.add_saas_tokens(
                    automation["user_id"], 
                    5, 
                    "automation_success", 
                    f"Automatisation '{automation['name']}' exécutée"
                )
            
            return {
                "success": True,
                "automation_id": automation_id,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Erreur exécution automatisation: {e}")
            return {"success": False, "error": str(e)}
    
    def execute_action(self, action: Dict, user_id: int) -> Dict:
        """Exécute une action spécifique"""
        try:
            action_type = action.get("type")
            
            if action_type == "send_email":
                return self.action_send_email(action, user_id)
            elif action_type == "post_social":
                return self.action_post_social(action, user_id)
            elif action_type == "webhook":
                return self.action_webhook(action, user_id)
            elif action_type == "generate_content":
                return self.action_generate_content(action, user_id)
            else:
                return {"success": False, "error": f"Type d'action inconnu: {action_type}"}
                
        except Exception as e:
            logger.error(f"Erreur exécution action: {e}")
            return {"success": False, "error": str(e)}
    
    def action_send_email(self, action: Dict, user_id: int) -> Dict:
        """Action d'envoi d'email"""
        try:
            from email_service import email_service
            
            to_email = action.get("to_email")
            subject = action.get("subject", "Email automatique")
            content = action.get("content", "")
            
            result = email_service.send_email(to_email, subject, content, content)
            
            return {
                "success": True,
                "action": "send_email",
                "details": f"Email envoyé à {to_email}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def action_post_social(self, action: Dict, user_id: int) -> Dict:
        """Action de publication sur les réseaux sociaux"""
        try:
            platform = action.get("platform", "twitter")
            content = action.get("content", "")
            
            # Placeholder pour l'intégration des APIs sociales
            if platform == "twitter":
                # Intégrer l'API Twitter/X ici
                pass
            elif platform == "linkedin":
                # Intégrer l'API LinkedIn ici
                pass
            
            return {
                "success": True,
                "action": "post_social",
                "details": f"Publication sur {platform} simulée"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def action_webhook(self, action: Dict, user_id: int) -> Dict:
        """Action webhook HTTP"""
        try:
            url = action.get("url")
            method = action.get("method", "POST")
            data = action.get("data", {})
            headers = action.get("headers", {"Content-Type": "application/json"})
            
            if method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            elif method.upper() == "GET":
                response = requests.get(url, params=data, headers=headers, timeout=30)
            else:
                return {"success": False, "error": f"Méthode HTTP non supportée: {method}"}
            
            return {
                "success": response.status_code < 400,
                "action": "webhook",
                "details": f"Webhook {method} {url} - Status: {response.status_code}"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def action_generate_content(self, action: Dict, user_id: int) -> Dict:
        """Action de génération de contenu IA"""
        try:
            from ai_service import ai_service
            
            prompt = action.get("prompt", "")
            content_type = action.get("content_type", "text")
            
            if content_type == "text":
                from openai_client import generate_text
                result = generate_text(prompt)
                
                return {
                    "success": True,
                    "action": "generate_content",
                    "details": "Contenu généré avec succès",
                    "generated_content": result
                }
            
            return {"success": False, "error": "Type de contenu non supporté"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_user_automations(self, user_id: int) -> List[Dict]:
        """Récupère les automatisations d'un utilisateur"""
        try:
            automations = db_service.get_user_automations(user_id)
            return automations
        except Exception as e:
            logger.error(f"Erreur récupération automatisations: {e}")
            return []
    
    def start_scheduler(self):
        """Démarre le planificateur d'automatisations"""
        if self.scheduler_running:
            return
        
        self.scheduler_running = True
        
        def run_scheduler():
            while self.scheduler_running:
                schedule.run_pending()
                asyncio.sleep(1)
        
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()
        
        logger.info("🤖 Planificateur d'automatisations démarré")

automation_service = AutomationService()
