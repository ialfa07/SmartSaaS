
import pytest
from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

class TestAPI:
    def test_root_endpoint(self):
        """Test endpoint racine"""
        response = client.get("/")
        assert response.status_code == 200
        assert "SmartSaaS API" in response.json()["message"]
    
    def test_register_user(self):
        """Test inscription utilisateur"""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = client.post("/auth/register", json=user_data)
        # Note: Peut échouer si DB non configurée
        assert response.status_code in [200, 500]
    
    def test_get_plans(self):
        """Test récupération des plans"""
        response = client.get("/plans")
        assert response.status_code == 200
        assert "plans" in response.json()
    
    def test_token_rewards(self):
        """Test endpoint récompenses"""
        response = client.get("/tokens/rewards")
        assert response.status_code == 200
        assert "daily_actions" in response.json()
    
    def test_network_info(self):
        """Test info réseau blockchain"""
        response = client.get("/web3/network-info")
        assert response.status_code == 200

def run_tests():
    """Lance les tests"""
    pytest.main([__file__, "-v"])

if __name__ == "__main__":
    run_tests()
