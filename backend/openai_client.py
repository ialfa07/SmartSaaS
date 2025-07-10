
import openai
import os
import requests
from typing import Dict, List, Optional

# Configuration OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")

def generate_text(prompt: str, max_tokens: int = 500) -> str:
    """Génère du texte avec GPT-4"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erreur lors de la génération: {str(e)}"

def generate_image(prompt: str, size: str = "1024x1024", quality: str = "standard") -> Dict:
    """Génère une image avec DALL-E 3"""
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1
        )
        
        image_url = response.data[0].url
        return {
            "success": True,
            "image_url": image_url,
            "prompt": prompt,
            "size": size
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur génération image: {str(e)}"
        }

def generate_marketing_content(business_type: str, target_audience: str, platform: str) -> Dict:
    """Génère du contenu marketing adapté"""
    
    prompts = {
        "post": f"""Crée un post engageant pour {platform} pour une entreprise de {business_type} 
                   ciblant {target_audience}. Inclus des émojis et hashtags pertinents.""",
        
        "image": f"""Crée une image marketing attrayante pour {business_type} sur {platform}, 
                    style professionnel et moderne, couleurs vives, {target_audience}""",
        
        "caption": f"""Rédige une légende accrocheuse pour {platform} pour {business_type}, 
                      ton engageant, appel à l'action, hashtags populaires"""
    }
    
    try:
        # Génération du texte
        text_content = generate_text(prompts["post"])
        
        # Génération de l'image
        image_result = generate_image(prompts["image"])
        
        # Génération de la légende
        caption = generate_text(prompts["caption"], max_tokens=150)
        
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
            "error": f"Erreur génération contenu: {str(e)}"
        }

def generate_content_calendar(business_type: str, duration_days: int = 30) -> List[Dict]:
    """Génère un calendrier de contenu pour X jours"""
    
    calendar_prompt = f"""
    Crée un calendrier de contenu marketing pour {duration_days} jours 
    pour une entreprise de {business_type}.
    
    Format JSON avec :
    - date
    - type de contenu (post, story, reel, article)
    - plateforme recommandée
    - sujet principal
    - ton/style
    - call-to-action suggéré
    
    Varie les types de contenu et optimise l'engagement.
    """
    
    try:
        calendar_text = generate_text(calendar_prompt, max_tokens=1500)
        return {
            "success": True,
            "calendar": calendar_text,
            "duration": duration_days,
            "business_type": business_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur génération calendrier: {str(e)}"
        }
