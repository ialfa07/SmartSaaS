
#!/usr/bin/env python3
"""
Script de démarrage optimisé pour SmartSaaS
"""

import uvicorn
import sys
import os
from pathlib import Path

# Ajouter le répertoire backend au path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def main():
    """Démarre l'application avec configuration optimisée"""
    
    # Configuration du serveur
    config = {
        "app": "main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "reload": os.getenv("DEBUG", "False").lower() == "true",
        "workers": 1 if os.getenv("DEBUG", "False").lower() == "true" else 4,
        "log_level": "info",
        "access_log": True
    }
    
    print("🚀 Démarrage de SmartSaaS API...")
    print(f"📍 Serveur: http://0.0.0.0:{config['port']}")
    print(f"🔧 Mode debug: {config['reload']}")
    print(f"⚡ Workers: {config['workers']}")
    
    # Initialiser la base de données
    try:
        from init_db import setup_postgresql, create_tables
        setup_postgresql()
        create_tables()
        print("✅ Base de données initialisée")
    except Exception as e:
        print(f"⚠️ Erreur init DB: {e}")
    
    # Démarrer le serveur
    uvicorn.run(**config)

if __name__ == "__main__":
    main()
