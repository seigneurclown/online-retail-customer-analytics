"""
Bộ kiểm thử QA toàn diện và Edge Cases chuyên sâu (Phase 11)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

import pytest


def test_invalid_sort_order_returns_422(client):
    """Kiểm tra truyền order không phải 'asc' hoặc 'desc' bị chặn lại với HTTP 422."""
    response = client.get("/api/v1/sales/products?order=random_order")
    assert response.status_code == 422
    err = response.json()
    assert "detail" in err


def test_negative_numeric_filters_return_422(client):
    """Kiểm tra truyền số âm cho các trường ge=0 (min_recency, min_frequency, min_value) trả về 422."""
    # min_recency âm
    res1 = client.get("/api/v1/customers?min_recency=-5")
    assert res1.status_code == 422

    # min_frequency âm
    res2 = client.get("/api/v1/customers?min_frequency=-1")
    assert res2.status_code == 422

    # min_value âm
    res3 = client.get("/api/v1/sales/invoices?min_value=-100")
    assert res3.status_code == 422


def test_nonexistent_cluster_returns_404(client):
    """Kiểm tra tra cứu cụm không tồn tại trả về đúng mã lỗi HTTP 404."""
    response = client.get("/api/v1/segmentation/clusters/888")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_invalid_cluster_type_returns_422(client):
    """Kiểm tra truyền cluster_id không phải số nguyên (VD: string 'abc') trả về 422."""
    response = client.get("/api/v1/segmentation/clusters/invalid_cluster_name")
    assert response.status_code == 422


def test_pagination_boundary_single_item(client):
    """Kiểm tra giới hạn trang với page_size = 1."""
    response = client.get("/api/v1/sales/products?page=1&page_size=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["page_size"] == 1
    assert data["total"] == 10
    assert data["total_pages"] == 10


def test_pagination_boundary_max_limit(client):
    """Kiểm tra giới hạn tối đa page_size = 100 thành công."""
    response = client.get("/api/v1/customers?page=1&page_size=100")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 100
    assert data["page_size"] == 100


def test_empty_search_invoices_returns_empty_paginated_list(client):
    """Kiểm tra lọc hóa đơn với giá trị không tưởng (min_value = 999999999) trả về items rỗng 200."""
    response = client.get("/api/v1/sales/invoices?min_value=999999999")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["total_pages"] == 0


def test_openapi_schema_generation(client):
    """Kiểm tra OpenAPI JSON Schema tự động sinh đầy đủ các components và endpoints."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "openapi" in schema
    assert "paths" in schema
    assert "/api/v1/dashboard/summary" in schema["paths"]
    assert "/api/v1/sales/products" in schema["paths"]
    assert "/api/v1/customers/{customer_id}" in schema["paths"]
    assert "/api/v1/segmentation/summary" in schema["paths"]
    assert "/api/v1/statistics/tests" in schema["paths"]
