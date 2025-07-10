
import os
from typing import Dict, List
import json

# Clé API OpenAI (à configurer dans les secrets)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-fake-key-for-demo")

def generate_text(prompt: str, max_tokens: int = 500) -> str:
    """Génère du texte avec OpenAI GPT"""
    try:
        # Pour la démo, on simule une réponse
        if "post LinkedIn" in prompt.lower():
            return """🚀 Les tendances marketing 2024 qui vont révolutionner votre stratégie !

✨ IA et personnalisation à grande échelle
📱 Social commerce en pleine expansion  
🎯 Marketing conversationnel avec les chatbots
📊 Données first-party au cœur des stratégies
🌱 Marketing durable et éthique

Quelle tendance vous inspire le plus pour cette année ?

#Marketing2024 #IA #Innovation #DigitalMarketing #Tendances"""
        
        elif "restaurant" in prompt.lower():
            return """🍽️ Découvrez notre nouveau menu de saison !

Des plats préparés avec des ingrédients frais et locaux, pour une expérience culinaire inoubliable.

Réservez dès maintenant et laissez-vous surprendre par nos créations !

#Restaurant #CuisineFraiche #MenuDeSaison"""
        
        else:
            return f"""Voici du contenu généré basé sur votre demande : "{prompt[:50]}..."

Ce contenu a été créé pour répondre à vos besoins marketing spécifiques. Il est optimisé pour l'engagement et conçu pour votre audience cible.

N'hésitez pas à l'adapter selon vos besoins !"""
            
    except Exception as e:
        return f"Erreur lors de la génération : {str(e)}"

def generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard") -> Dict:
    """Génère une image avec DALL-E"""
    try:
        # Pour la démo, on retourne une image placeholder
        return {
            "success": True,
            "image_url": f"https://via.placeholder.com/{size.replace('x', 'x')}/4F46E5/FFFFFF?text=Image+IA+Generee",
            "prompt": prompt,
            "size": size,
            "quality": quality
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur génération image : {str(e)}"
        }

def generate_marketing_content(business_type: str, target_audience: str, platform: str) -> Dict:
    """Génère du contenu marketing adapté"""
    
    try:
        # Génération du texte principal
        if platform == "instagram":
            text_content = f"""✨ {business_type.title()} qui comprend ses clients !

Spécialement conçu pour {target_audience}, nous savons ce qui vous fait vibrer.

Découvrez notre univers et rejoignez notre communauté ! 

#Instagram #Marketing #{business_type.replace(' ', '')}"""
            
        elif platform == "linkedin":
            text_content = f"""🚀 Comment {business_type} révolutionne l'expérience client

Notre approche centrée sur {target_audience} nous permet de créer des solutions innovantes qui répondent aux vrais besoins du marché.

Découvrez notre vision et partagez votre avis en commentaire !

#LinkedIn #Innovation #Business"""
            
        else:
            text_content = f"""Nouveau chez {business_type} ! 

Parfait pour {target_audience}, découvrez ce qui nous rend uniques.

Suivez-nous pour plus de contenus exclusifs !"""

        # Génération de l'image
        image_result = generate_image(f"Marketing visuel moderne pour {business_type}, style professionnel, couleurs attrayantes")
        
        # Génération de la légende
        caption = f"""🎯 Contenu spécialement créé pour {target_audience}

✅ Engageant et authentique
✅ Optimisé pour {platform}
✅ Call-to-action intégré

#Marketing #IA #{platform.title()} #{business_type.replace(' ', '')}"""
        
        return {
            "success": True,
            "content": {
                "text": text_content,
                "image": image_result,
                "caption": caption,
                "platform": platform,
                "business_type": business_type,
                "target_audience": target_audience
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur génération contenu : {str(e)}"
        }

def generate_content_calendar(business_type: str, duration_days: int = 30) -> Dict:
    """Génère un calendrier de contenu pour X jours"""
    
    try:
        calendar_content = f"""📅 CALENDRIER DE CONTENU - {business_type.upper()} ({duration_days} jours)

SEMAINE 1:
📱 Lundi: Post de présentation + Story behind the scenes
📸 Mercredi: Contenu produit/service + Carousel informatif  
🎥 Vendredi: Vidéo témoignage client + Post engagement

SEMAINE 2:
💡 Lundi: Conseil/Astuce + Story interactive
🎯 Mercredi: Contenu éducatif + Post questions/réponses
🚀 Vendredi: Annonce/Nouveauté + Story countdown

SEMAINE 3:
👥 Lundi: Contenu communauté + Story user-generated content
📊 Mercredi: Infographie/Statistiques + Post didactique
🎉 Vendredi: Contenu divertissant + Story quiz

SEMAINE 4:
🔥 Lundi: Contenu tendance + Story sondage
💎 Mercredi: Contenu premium/exclusif + Post call-to-action
🌟 Vendredi: Récap de la semaine + Story remerciements

CONSEILS BONUS:
- Postez aux heures de forte audience (11h-13h, 17h-19h)
- Utilisez 3-5 hashtags stratégiques par post
- Alternez entre contenu informatif, divertissant et promotionnel
- Répondez aux commentaires dans les 2h"""

        return {
            "success": True,
            "calendar": calendar_content,
            "duration": duration_days,
            "business_type": business_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur génération calendrier : {str(e)}"
        }
