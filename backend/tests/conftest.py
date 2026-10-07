"""
Pytest Test Fixtures cho Online Retail Backend (MongoDB NoSQL)
Tạo môi trường test hoàn toàn cô lập sử dụng mongomock và nạp dữ liệu mẫu từ analytics pipeline.
"""

import pytest
import mongomock
from fastapi.testclient import TestClient
from app.main import app
from app.core.mongodb import get_database
from scripts.seed_database import run_seed_pipeline


@pytest.fixture(scope="session")
def mock_db():
    """Khởi tạo một database MongoMock trong bộ nhớ và nạp dữ liệu một lần cho cả phiên test."""
    client = mongomock.MongoClient()
    db = client["online_retail_test"]
    run_seed_pipeline(db)
    return db


@pytest.fixture(scope="session")
def client(mock_db):
    """
    TestClient FastAPI với dependency override get_database trỏ tới mock_db.
    Đảm bảo 100% API tests chạy siêu tốc và độc lập không cần bật MongoDB service bên ngoài.
    """
    app.dependency_overrides[get_database] = lambda: mock_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
