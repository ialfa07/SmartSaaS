
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db
from models import Base

# Base de données de test en mémoire
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False,
    },
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    """Remplace la dépendance get_db pour utiliser la BDD de test."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_register_user():
    """Teste l'inscription d'un nouvel utilisateur."""
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["credits"] == 5  # Crédits par défaut

def test_register_duplicate_email():
    """Teste l'inscription avec un email déjà utilisé."""
    # Premier utilisateur
    client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "password123"},
    )
    
    # Tentative de doublon
    response = client.post(
        "/auth/register",
        json={"email": "duplicate@example.com", "password": "password456"},
    )
    assert response.status_code == 400
    assert "déjà utilisé" in response.json()["detail"]

def test_login_success():
    """Teste la connexion avec des identifiants valides."""
    # Créer un utilisateur d'abord
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password123"},
    )
    
    # Connexion
    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials():
    """Teste la connexion avec des identifiants invalides."""
    response = client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"]

def test_protected_route_without_token():
    """Teste l'accès à une route protégée sans token."""
    response = client.get("/user-info")
    assert response.status_code == 401

def test_protected_route_with_token():
    """Teste l'accès à une route protégée avec token valide."""
    # Créer et connecter un utilisateur
    register_response = client.post(
        "/auth/register",
        json={"email": "protected@example.com", "password": "password123"},
    )
    token = register_response.json()["access_token"]
    
    # Accéder à la route protégée
    response = client.get(
        "/user-info",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "protected@example.com"
    assert "credits" in data
    assert "plan" in data
