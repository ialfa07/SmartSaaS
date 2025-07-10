
# 📋 Pré-requis - SmartSaaS

## 🎯 Vue d'ensemble
SmartSaaS est une plateforme SaaS complète avec IA, blockchain et système de récompenses. Ce document liste tous les pré-requis pour le développement et la production.

## 🔧 Technologies principales

### Backend (FastAPI)
- **Python 3.12+** ✅ (déjà configuré dans Replit)
- **PostgreSQL** pour la base de données
- **Redis** (optionnel) pour le cache
- **OpenAI API** pour l'IA
- **Stripe API** pour les paiements
- **SendGrid** pour les emails

### Frontend (Next.js)
- **Node.js 20+** ✅ (déjà configuré dans Replit)
- **React 18+**
- **Next.js 14+**
- **Tailwind CSS**

### Blockchain (Web3)
- **Ethereum/Polygon** compatible
- **Solidity** pour les smart contracts
- **Web3.py** pour l'intégration

## 🔑 Variables d'environnement requises

### Configuration générale
```bash
# Application
SECRET_KEY=your-secret-key-here
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1,*.replit.dev

# Base de données
DATABASE_URL=postgresql://user:password@localhost:5432/smartsaas
```

### APIs externes
```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# SendGrid
SENDGRID_API_KEY=SG....
FROM_EMAIL=noreply@smartsaas.com
```

### Blockchain/Web3
```bash
# Web3 Configuration
WEB3_RPC_URL=https://polygon-mainnet.infura.io/v3/YOUR_PROJECT_ID
WEB3_CHAIN_ID=137
WEB3_PRIVATE_KEY=your_private_key_here
SAAS_TOKEN_CONTRACT=0x...
```

## 📦 Dépendances système

### Backend Python
```bash
# Installation automatique via requirements.txt
pip install -r backend/requirements.txt
```

**Paquets principaux :**
- `fastapi` - Framework web moderne
- `uvicorn` - Serveur ASGI
- `sqlalchemy` - ORM
- `psycopg2-binary` - Driver PostgreSQL
- `openai` - Client OpenAI
- `stripe` - Paiements
- `web3` - Intégration blockchain
- `python-jose` - JWT tokens
- `passlib` - Hachage mots de passe
- `sendgrid` - Service email

### Frontend Node.js
```bash
# Installation automatique via package.json
npm install
```

**Paquets principaux :**
- `next` - Framework React
- `react` - Bibliothèque UI
- `tailwindcss` - CSS utility
- `framer-motion` - Animations
- `axios` - Client HTTP
- `react-hot-toast` - Notifications

## 🗄️ Base de données

### PostgreSQL Setup
```sql
-- Créer la base de données
CREATE DATABASE smartsaas;

-- Créer un utilisateur
CREATE USER smartsaas_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE smartsaas TO smartsaas_user;
```

### Tables requises
- `users` - Utilisateurs
- `saas_tokens` - Jetons de récompense
- `referrals` - Système de parrainage
- `payments` - Historique des paiements
- `content_generations` - Historique IA

## 🔒 Configuration sécurité

### Clés et secrets
1. **SECRET_KEY** - Clé secrète pour JWT (256 bits minimum)
2. **Mots de passe** - Hashés avec bcrypt
3. **API Keys** - Stockées en variables d'environnement
4. **CORS** - Configuré pour les domaines autorisés

### Limites de taux
- 100 requêtes/minute par IP
- Protection contre les attaques DDoS
- Validation des entrées utilisateur

## 🌐 Configuration réseau

### Ports utilisés
- **Frontend** : 3000 (Next.js dev)
- **Backend** : 8000 (FastAPI)
- **Base de données** : 5432 (PostgreSQL)
- **Production** : 80/443 (via Replit)

### Domaines
- **Développement** : `*.replit.dev`
- **Production** : `smartsaas.com` (à configurer)

## 📧 Configuration Email

### SendGrid
1. Créer un compte SendGrid
2. Vérifier le domaine d'expédition
3. Configurer les templates d'email
4. Obtenir la clé API

### Templates requis
- Email de bienvenue
- Notifications de jetons
- Rappels quotidiens
- Confirmations de paiement

## 🔗 Configuration Blockchain

### Prérequis Web3
1. **Wallet MetaMask** pour les tests
2. **Compte Infura/Alchemy** pour RPC
3. **Faucet tokens** pour les tests
4. **Contrat déployé** sur le réseau choisi

### Réseaux supportés
- **Ethereum Mainnet** (coûteux)
- **Polygon** (recommandé)
- **Ethereum Sepolia** (tests)
- **Polygon Mumbai** (tests)

## ⚙️ Configuration Replit

### Modules système
```toml
# .replit
modules = ["nodejs-20", "python-3.12", "bash", "web"]
```

### Secrets à configurer
Dans l'onglet "Secrets" de Replit :
- `OPENAI_API_KEY`
- `STRIPE_SECRET_KEY`
- `SENDGRID_API_KEY`
- `WEB3_PRIVATE_KEY`
- `SECRET_KEY`

## 🚀 Déploiement

### Étapes de déploiement
1. **Configurer les variables d'environnement**
2. **Installer les dépendances**
3. **Initialiser la base de données**
4. **Déployer les smart contracts**
5. **Tester les endpoints**
6. **Configurer les webhooks**

### Commandes de démarrage
```bash
# Backend
cd backend && python start.py

# Frontend
cd frontend && npm run dev

# Full Stack
npm run dev  # Via package.json racine
```

## 🧪 Tests et validation

### Tests backend
```bash
cd backend && python -m pytest test_api.py
```

### Tests frontend
```bash
cd frontend && npm test
```

### Validation des APIs
- OpenAI : Test génération de texte
- Stripe : Test paiement sandbox
- SendGrid : Test envoi email
- Web3 : Test connexion blockchain

## 📊 Monitoring

### Métriques importantes
- Temps de réponse API
- Utilisation des crédits
- Taux de conversion
- Erreurs système

### Logs à surveiller
- Erreurs FastAPI
- Échecs de paiement
- Problèmes blockchain
- Erreurs d'email

## 🔄 Maintenance

### Mises à jour régulières
- Dépendances Python/Node.js
- Clés API (rotation)
- Certificats SSL
- Sauvegardes base de données

### Sauvegardes
- Base de données quotidienne
- Configuration système
- Clés privées (sécurisées)

---

## ✅ Checklist de démarrage

- [ ] Python 3.12+ installé
- [ ] Node.js 20+ installé
- [ ] PostgreSQL configuré
- [ ] Variables d'environnement définies
- [ ] Dépendances installées
- [ ] Base de données initialisée
- [ ] APIs testées
- [ ] Smart contracts déployés
- [ ] Frontend/Backend connectés
- [ ] Tests passés avec succès

**🎯 Une fois cette checklist complétée, votre SmartSaaS est prêt à fonctionner !**
