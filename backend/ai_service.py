
from openai import OpenAI
import os
from typing import Dict, List, Optional
import json
from logger import logger

class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def generate_saas_idea(self, prompt: str, target_audience: str = "", tech_stack: str = "") -> Dict:
        """Génère une idée de SaaS complète avec l'IA"""
        try:
            system_prompt = """Tu es un expert en création de SaaS. Génère une idée complète de micro-SaaS basée sur le prompt utilisateur.
            
            Retourne un JSON avec:
            - name: nom du SaaS
            - description: description détaillée
            - features: liste des fonctionnalités principales
            - tech_stack: technologies recommandées
            - monetization: modèle de monétisation
            - target_market: marché cible
            - mvp_timeline: timeline pour le MVP (en semaines)
            - estimated_cost: coût estimé de développement
            """
            
            user_prompt = f"""
            Idée de base: {prompt}
            Public cible: {target_audience}
            Stack technique préférée: {tech_stack}
            
            Génère une idée de SaaS complète et réalisable.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
                return {"success": True, "saas_idea": result}
            except json.JSONDecodeError:
                return {"success": True, "saas_idea": {"description": response.choices[0].message.content}}
                
        except Exception as e:
            logger.error(f"Erreur génération idée SaaS: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_code_structure(self, saas_idea: Dict) -> Dict:
        """Génère la structure de code pour une idée SaaS"""
        try:
            system_prompt = """Tu es un architecte logiciel expert. Génère la structure de code complète pour ce SaaS.
            
            Retourne un JSON avec:
            - file_structure: arborescence des fichiers
            - main_files: contenu des fichiers principaux
            - database_schema: schéma de base de données SQL
            - api_endpoints: liste des endpoints API
            - frontend_components: composants React principaux
            - deployment_config: configuration de déploiement
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Génère la structure de code pour: {json.dumps(saas_idea)}"}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
                return {"success": True, "code_structure": result}
            except json.JSONDecodeError:
                return {"success": True, "code_structure": {"description": response.choices[0].message.content}}
                
        except Exception as e:
            logger.error(f"Erreur génération code: {e}")
            return {"success": False, "error": str(e)}
    
    def generate_marketing_strategy(self, saas_idea: Dict) -> Dict:
        """Génère une stratégie marketing pour le SaaS"""
        try:
            system_prompt = """Tu es un expert en marketing digital. Crée une stratégie marketing complète pour ce SaaS.
            
            Retourne un JSON avec:
            - positioning: positionnement unique
            - target_personas: personas détaillées
            - channels: canaux d'acquisition
            - content_strategy: stratégie de contenu
            - pricing_strategy: stratégie de prix
            - launch_plan: plan de lancement
            - kpis: indicateurs clés à suivre
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Crée une stratégie marketing pour: {json.dumps(saas_idea)}"}
                ],
                temperature=0.5,
                max_tokens=1500
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
                return {"success": True, "marketing_strategy": result}
            except json.JSONDecodeError:
                return {"success": True, "marketing_strategy": {"description": response.choices[0].message.content}}
                
        except Exception as e:
            logger.error(f"Erreur génération marketing: {e}")
            return {"success": False, "error": str(e)}

ai_service = AIService()
