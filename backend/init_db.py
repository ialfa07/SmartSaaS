
import os
import subprocess
import psycopg2
from psycopg2 import sql
from models import Base, engine
import time

def setup_postgresql():
    """Configure PostgreSQL sur Replit"""
    print("🔧 Configuration de PostgreSQL...")
    
    # Démarrer PostgreSQL
    try:
        subprocess.run(["pg_ctl", "-D", "/tmp/postgresql", "-l", "/tmp/postgresql/server.log", "start"], 
                      check=False, capture_output=True)
        time.sleep(2)
    except Exception as e:
        print(f"PostgreSQL déjà démarré ou erreur: {e}")
    
    # Créer la base de données
    try:
        # Connexion à PostgreSQL pour créer la base
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="password",
            database="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Créer la base de données smartsaas
        cursor.execute("DROP DATABASE IF EXISTS smartsaas;")
        cursor.execute("CREATE DATABASE smartsaas;")
        
        cursor.close()
        conn.close()
        
        print("✅ Base de données 'smartsaas' créée avec succès")
        
    except Exception as e:
        print(f"⚠️ Erreur création base: {e}")
        # Fallback vers SQLite si PostgreSQL échoue
        print("🔄 Basculement vers SQLite...")
        os.environ["DATABASE_URL"] = "sqlite:///./smartsaas.db"
        
def create_tables():
    """Crée toutes les tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès")
    except Exception as e:
        print(f"❌ Erreur création tables: {e}")

if __name__ == "__main__":
    setup_postgresql()
    create_tables()
