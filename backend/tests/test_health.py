"""
Kiểm thử tự động cho Health Check, Root Endpoint và MongoDB Health (Phase 1)
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Kiểm tra endpoint root '/' trả về thông tin hệ thống và status code 200."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "app_name" in data
    assert "docs_url" in data
    assert data["docs_url"] == "/docs"
    assert data["health_check"] == "/health"
    assert data["database_health_check"] == "/health/db"


def test_health_check_endpoint():
    """Kiểm tra endpoint health '/health' trả về status: ok và status code 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_swagger_docs_accessible():
    """Kiểm tra trang Swagger UI '/docs' có thể truy cập thành công."""
    response = client.get("/docs")
    assert response.status_code == 200


@pytest.mark.anyio
async def test_database_health_connected():
    """Kiểm tra endpoint '/health/db' khi kết nối MongoDB thành công."""
    with patch("app.main.mongodb_manager.check_connection", new_callable=AsyncMock) as mock_ping:
        mock_ping.return_value = True
        response = client.get("/health/db")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["database"] == "online_retail"


@pytest.mark.anyio
async def test_database_health_disconnected():
    """Kiểm tra endpoint '/health/db' khi không thể kết nối MongoDB (HTTP 503)."""
    with patch("app.main.mongodb_manager.check_connection", new_callable=AsyncMock) as mock_ping:
        mock_ping.return_value = False
        response = client.get("/health/db")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "error"
        assert data["database"] == "online_retail"
        assert "message" in data
