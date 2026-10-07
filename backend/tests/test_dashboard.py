"""
Kiểm thử tự động cho Dashboard APIs (Phase 3)
"""

import pytest


def test_get_dashboard_summary(client):
    """Kiểm tra endpoint /api/v1/dashboard/summary trả về đầy đủ 4 KPI quan trọng."""
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code == 200
    data = response.json()
    assert "total_revenue" in data
    assert "total_orders" in data
    assert "total_customers" in data
    assert "average_order_value" in data
    assert data["total_revenue"] > 8000000.0
    assert data["total_orders"] == 19960
    assert data["total_customers"] > 4000
    assert data["average_order_value"] > 500.0


def test_get_revenue_trend(client):
    """Kiểm tra endpoint /api/v1/dashboard/revenue-trend trả về danh sách tháng kèm doanh thu."""
    response = client.get("/api/v1/dashboard/revenue-trend")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 12
    first_item = data["items"][0]
    assert "year_month" in first_item
    assert "revenue" in first_item


def test_get_top_products(client):
    """Kiểm tra endpoint /api/v1/dashboard/top-products có thể giới hạn bằng query limit."""
    response = client.get("/api/v1/dashboard/top-products?limit=5")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) <= 5
    assert len(items) > 0
    top1 = items[0]
    assert "stock_code" in top1
    assert "total_revenue" in top1
    assert top1["total_revenue"] > 0


def test_get_top_countries(client):
    """Kiểm tra endpoint /api/v1/dashboard/top-countries."""
    response = client.get("/api/v1/dashboard/top-countries?limit=5")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) <= 5
    assert len(items) > 0
    top1 = items[0]
    assert top1["country"] == "United Kingdom"
    assert top1["percentage_share"] > 50.0
