"""Test application endpoints."""
import pytest


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_application(client):
    """Test creating an application."""
    response = client.post(
        "/api/v1/applications",
        json={
            "app_code": "test_app",
            "app_name": "Test Application"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["app_code"] == "test_app"
    assert data["app_name"] == "Test Application"
    assert "id" in data


def test_list_applications(client):
    """Test listing applications."""
    # Create an application first
    client.post(
        "/api/v1/applications",
        json={
            "app_code": "test_app",
            "app_name": "Test Application"
        }
    )
    
    # List applications
    response = client.get("/api/v1/applications")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1


def test_get_application(client):
    """Test getting a specific application."""
    # Create an application
    create_response = client.post(
        "/api/v1/applications",
        json={
            "app_code": "test_app",
            "app_name": "Test Application"
        }
    )
    app_id = create_response.json()["id"]
    
    # Get the application
    response = client.get(f"/api/v1/applications/{app_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == app_id
    assert data["app_code"] == "test_app"
