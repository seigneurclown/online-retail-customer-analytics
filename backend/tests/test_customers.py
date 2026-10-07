"""
Kiểm thử tự động cho Customer & RFM APIs (Phase 5)
"""

import pytest


def test_get_customers_pagination(client):
    """Kiểm tra phân trang danh sách khách hàng."""
    response = client.get("/api/v1/customers?page=1&page_size=20")
    assert response.status_code == 200
    res = response.json()
    assert res["page"] == 1
    assert res["page_size"] == 20
    assert res["total"] > 4000
    assert len(res["items"]) == 20
    first = res["items"][0]
    assert "customer_id" in first
    assert "recency" in first
    assert "frequency" in first
    assert "monetary" in first
    assert "cluster" in first
    assert "membership_tier" in first


def test_get_customers_filter_by_cluster(client):
    """Kiểm tra lọc khách hàng theo cụm K-Means (VD: cluster 2)."""
    response = client.get("/api/v1/customers?cluster=2&page=1&page_size=10")
    assert response.status_code == 200
    res = response.json()
    assert res["total"] > 0
    for item in res["items"]:
        assert item["cluster"] == 2


def test_get_customer_detail_found(client):
    """Kiểm tra tra cứu chi tiết một khách hàng có thực (VD: customer 12347)."""
    response = client.get("/api/v1/customers/12347")
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == "12347"
    assert data["cluster"] == 2
    assert "Thẻ Vàng" in data["membership_tier"]
    assert data["recency"] == 2
    assert data["frequency"] == 7
    assert data["monetary"] == 4310.0


def test_get_customer_detail_not_found(client):
    """Kiểm tra ném mã lỗi 404 khi tra cứu customer không tồn tại."""
    response = client.get("/api/v1/customers/99999999")
    assert response.status_code == 404
    err = response.json()
    assert "detail" in err
    assert "not found" in err["detail"].lower()
