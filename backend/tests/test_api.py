
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from tests.test_auth import client, override_get_db  # Réutiliser la config de test

def get_auth_token():
    """Helper pour obtenir un token d'authentification"""
    response = client.post(
        "/auth/register",
        json={"email": "test_api@example.com", "password": "password123"},
    )
    return response.json()["access_token"]

@patch('openai_client.generate_text')
def test_generate_text_success(mock_generate):
    """Teste la génération de texte avec succès"""
    mock_generate.return_value = "Contenu IA généré"
    token = get_auth_token()
    
    response = client.post(
        "/generate",
        json={"prompt": "Écris un article sur l'IA"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    assert "credits_left" in data

def test_generate_without_credits():
    """Teste la génération sans crédits suffisants"""
    token = get_auth_token()
    
    # Épuiser les crédits en faisant plusieurs requêtes
    for _ in range(6):  # Plus que les 5 crédits par défaut
        try:
            client.post(
                "/generate",
                json={"prompt": "Test"},
                headers={"Authorization": f"Bearer {token}"}
            )
        except:
            pass  # Ignorer les erreurs pour ce test
    
    response = client.post(
        "/generate",
        json={"prompt": "Test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403
    assert "insuffisants" in response.json()["detail"]

def test_get_plans():
    """Teste la récupération des plans d'abonnement"""
    response = client.get("/plans")
    assert response.status_code == 200
    data = response.json()
    assert "plans" in data
    assert "starter" in data["plans"]
    assert "pro" in data["plans"]
    assert "business" in data["plans"]

def test_get_token_rewards():
    """Teste la récupération des récompenses de tokens"""
    response = client.get("/tokens/rewards")
    assert response.status_code == 200
    data = response.json()
    assert "daily_actions" in data
    assert "achievements" in data
    assert "referral" in data
    assert "exchange_rate" in data
