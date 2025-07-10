
#!/bin/bash

# Script de démarrage PostgreSQL pour Replit
echo "🚀 Démarrage de PostgreSQL..."

# Créer le répertoire de données s'il n'existe pas
if [ ! -d "/tmp/postgresql" ]; then
    echo "📁 Création du répertoire PostgreSQL..."
    initdb -D /tmp/postgresql
    echo "listen_addresses = '*'" >> /tmp/postgresql/postgresql.conf
    echo "port = 5432" >> /tmp/postgresql/postgresql.conf
    echo "host all all 0.0.0.0/0 md5" >> /tmp/postgresql/pg_hba.conf
fi

# Démarrer PostgreSQL
pg_ctl -D /tmp/postgresql -l /tmp/postgresql/server.log start

# Attendre que PostgreSQL soit prêt
sleep 3

# Créer l'utilisateur postgres s'il n'existe pas
createuser -s postgres 2>/dev/null || true

# Définir le mot de passe
psql -c "ALTER USER postgres PASSWORD 'password';" 2>/dev/null || true

echo "✅ PostgreSQL démarré avec succès"
