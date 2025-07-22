
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
    print("ℹ️  L'initialisation de la base de données et la création des tables")
    print("ℹ️  sont gérées au démarrage de l'application dans main.py.")
    print("ℹ️  Pour une configuration manuelle de PostgreSQL, exécutez : python backend/init_db.py")
    
    # Démarrer le serveur
    uvicorn.run(**config)

if __name__ == "__main__":
    main()
