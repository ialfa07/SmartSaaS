
#!/usr/bin/env python3
"""
Vérificateur de configuration pour SmartSaaS
"""

import os
from pathlib import Path

def check_environment():
    """Vérifie la configuration des variables d'environnement"""
    
    print("🔍 Vérification de l'environnement SmartSaaS...")
    print("=" * 50)
    
    required_vars = {
        'SECRET_KEY': 'Clé secrète JWT',
        'DATABASE_URL': 'URL de la base de données',
        'OPENAI_API_KEY': 'Clé API OpenAI',
        'STRIPE_SECRET_KEY': 'Clé secrète Stripe',
        'STRIPE_PUBLISHABLE_KEY': 'Clé publique Stripe',
        'SENDGRID_API_KEY': 'Clé API SendGrid',
        'WEB3_RPC_URL': 'URL RPC Web3',
        'WEB3_PRIVATE_KEY': 'Clé privée Web3',
        'SAAS_TOKEN_CONTRACT': 'Adresse contrat SaaS Token'
    }
    
    optional_vars = {
        'WEB3_CHAIN_ID': 'ID de la chaîne blockchain',
        'EMAIL_FROM': 'Email expéditeur',
        'APP_URL': 'URL de l\'application'
    }
    
    # Charger le fichier .env s'il existe
    env_file = Path('.env')
    env_vars = {}
    
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
        print("✅ Fichier .env trouvé")
    else:
        print("❌ Fichier .env manquant")
    
    print(f"\n📋 VARIABLES REQUISES ({len(required_vars)})")
    missing_required = []
    
    for var, description in required_vars.items():
        value = env_vars.get(var) or os.getenv(var)
        if value:
            # Masquer les valeurs sensibles
            if 'key' in var.lower() or 'secret' in var.lower():
                display_value = f"{value[:8]}..." if len(value) > 8 else "***"
            else:
                display_value = value[:50] + "..." if len(value) > 50 else value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ❌ {var}: MANQUANTE - {description}")
            missing_required.append(var)
    
    print(f"\n📋 VARIABLES OPTIONNELLES ({len(optional_vars)})")
    for var, description in optional_vars.items():
        value = env_vars.get(var) or os.getenv(var)
        if value:
            display_value = value[:50] + "..." if len(value) > 50 else value
            print(f"   ✅ {var}: {display_value}")
        else:
            print(f"   ⚠️  {var}: Non définie - {description}")
    
    # Génerer un fichier .env template si nécessaire
    if missing_required:
        print(f"\n📝 Génération du template .env...")
        with open('.env.template', 'w') as f:
            f.write("# Configuration SmartSaaS\n")
            f.write("# Copiez ce fichier vers .env et remplissez les valeurs\n\n")
            
            f.write("# Base de données\n")
            f.write("DATABASE_URL=postgresql://postgres:password@localhost:5432/smartsaas\n\n")
            
            f.write("# Sécurité\n")
            f.write("SECRET_KEY=your-super-secret-jwt-key-here-change-this\n\n")
            
            f.write("# APIs externes\n")
            f.write("OPENAI_API_KEY=sk-your-openai-api-key\n")
            f.write("STRIPE_SECRET_KEY=sk_test_your-stripe-secret-key\n")
            f.write("STRIPE_PUBLISHABLE_KEY=pk_test_your-stripe-publishable-key\n")
            f.write("SENDGRID_API_KEY=SG.your-sendgrid-api-key\n\n")
            
            f.write("# Web3/Blockchain\n")
            f.write("WEB3_RPC_URL=https://rpc-mumbai.maticvigil.com/\n")
            f.write("WEB3_CHAIN_ID=80001\n")
            f.write("WEB3_PRIVATE_KEY=your-wallet-private-key\n")
            f.write("SAAS_TOKEN_CONTRACT=0x...\n\n")
            
            f.write("# Configuration app\n")
            f.write("APP_URL=http://localhost:3000\n")
            f.write("EMAIL_FROM=noreply@smartsaas.com\n")
            
        print("✅ Template .env.template créé")
    
    print(f"\n📊 RÉSUMÉ")
    print(f"   Variables requises: {len(required_vars) - len(missing_required)}/{len(required_vars)}")
    print(f"   Variables manquantes: {len(missing_required)}")
    
    if missing_required:
        print(f"\n❌ Configuration incomplète!")
        print(f"   Variables manquantes: {', '.join(missing_required)}")
        print(f"   👉 Utilisez le template .env.template pour configurer")
        return False
    else:
        print(f"\n✅ Configuration complète!")
        return True

if __name__ == "__main__":
    check_environment()
