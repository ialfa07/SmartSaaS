
# 🚀 Guide de configuration rapide - SmartSaaS

## 1. Configuration initiale (5 minutes)

### Étape 1 : Cloner et installer
```bash
# Les dépendances sont déjà configurées dans Replit
# Vérifier que tout est installé
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

### Étape 2 : Variables d'environnement
Créer un fichier `.env` à la racine :
```bash
# Copier le template
cp .env.example .env
```

## 2. Configuration des APIs (10 minutes)

### OpenAI
1. Aller sur https://platform.openai.com/
2. Créer une clé API
3. Ajouter dans `.env` : `OPENAI_API_KEY=sk-...`

### Stripe
1. Aller sur https://dashboard.stripe.com/
2. Récupérer les clés test
3. Ajouter dans `.env` :
   ```
   STRIPE_SECRET_KEY=sk_test_...
   STRIPE_PUBLISHABLE_KEY=pk_test_...
   ```

### SendGrid
1. Créer un compte sur https://sendgrid.com/
2. Créer une clé API
3. Ajouter dans `.env` : `SENDGRID_API_KEY=SG...`

## 3. Base de données (2 minutes)

### PostgreSQL
```bash
# Initialiser la base
cd backend && python init_db.py
```

## 4. Démarrage (1 minute)

### Option 1 : Utiliser le bouton Run
Cliquer sur le bouton "Run" dans Replit

### Option 2 : Manuel
```bash
# Terminal 1 - Backend
cd backend && python start.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

## 5. Vérification

### Tests rapides
- Backend : http://localhost:8000/docs
- Frontend : http://localhost:3000
- Base de données : http://localhost:8000/user-info

### Endpoints critiques
```bash
# Test OpenAI
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"prompt": "Hello world"}'

# Test Stripe
curl -X GET "http://localhost:8000/plans"
```

## 6. Configuration avancée (optionnel)

### Blockchain
```bash
# Configurer Web3
WEB3_RPC_URL=https://polygon-mainnet.infura.io/v3/YOUR_PROJECT_ID
WEB3_CHAIN_ID=137
```

### Monitoring
```bash
# Vérifier les logs
tail -f backend/logs/app.log
```

---

## 🔧 Dépannage rapide

### Problèmes courants

**Erreur "Module not found"**
```bash
cd backend && pip install -r requirements.txt
cd frontend && npm install
```

**Base de données inaccessible**
```bash
# Vérifier PostgreSQL
python backend/init_db.py
```

**API non fonctionnelle**
```bash
# Vérifier les variables d'environnement
cat .env
```

**Port déjà utilisé**
```bash
# Changer le port dans start.py
# Port 8000 -> 8001
```

---

## ✅ Checklist de validation

- [ ] Backend démarre sur port 8000
- [ ] Frontend démarre sur port 3000
- [ ] Base de données connectée
- [ ] OpenAI API fonctionnelle
- [ ] Stripe API fonctionnelle
- [ ] SendGrid API fonctionnelle
- [ ] Tests API passent
- [ ] Interface utilisateur chargée

**🎉 Félicitations ! Votre SmartSaaS est opérationnel !**

### Étapes suivantes
1. Créer votre premier utilisateur
2. Tester la génération de contenu
3. Configurer les paiements
4. Personnaliser l'interface
5. Déployer en production
