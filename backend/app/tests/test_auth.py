"""
Test authentication endpoints.
"""

import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient, test_user_data):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["full_name"] == test_user_data["full_name"]
    assert "id" in data


def test_login_user(client: TestClient, test_user_data):
    """Test user login."""
    # First register the user
    client.post("/api/v1/auth/register", json=test_user_data)
    
    # Then login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login/email", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login/email", json=login_data)
    assert response.status_code == 401


def test_get_current_user(client: TestClient, test_user_data):
    """Test getting current user with token."""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post("/api/v1/auth/login/email", json={
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Test token
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/v1/auth/test-token", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user_data["email"]

