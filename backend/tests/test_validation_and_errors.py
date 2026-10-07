"""
Kiểm thử tự động cho Validation, Phân trang và Error Handling (Phase 8 & 9)
"""

import pytest


def test_invalid_page_returns_422(client):
    """Kiểm tra truyền page < 1 bị FastAPI Pydantic chặn lại với mã lỗi 422."""
    response = client.get("/api/v1/customers?page=0")
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_invalid_page_size_returns_422(client):
    """Kiểm tra truyền page_size > 100 bị chặn lại với mã lỗi 422."""
    response = client.get("/api/v1/sales/products?page_size=200")
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_invalid_invoice_value_range_returns_400(client):
    """Kiểm tra min_value > max_value ném mã lỗi 400 Bad Request."""
    response = client.get("/api/v1/sales/invoices?min_value=1000&max_value=200")
    assert response.status_code == 400
    err = response.json()
    assert "detail" in err
    assert "min_value cannot be greater than max_value" in err["detail"]


def test_invalid_recency_range_returns_400(client):
    """Kiểm tra min_recency > max_recency ném mã lỗi 400 Bad Request."""
    response = client.get("/api/v1/customers?min_recency=100&max_recency=10")
    assert response.status_code == 400
    err = response.json()
    assert "detail" in err
    assert "min_recency cannot be greater than max_recency" in err["detail"]


def test_invalid_frequency_range_returns_400(client):
    """Kiểm tra min_frequency > max_frequency ném mã lỗi 400 Bad Request."""
    response = client.get("/api/v1/customers?min_frequency=50&max_frequency=5")
    assert response.status_code == 400
    err = response.json()
    assert "detail" in err
    assert "min_frequency cannot be greater than max_frequency" in err["detail"]


def test_invalid_monetary_range_returns_400(client):
    """Kiểm tra min_monetary > max_monetary ném mã lỗi 400 Bad Request."""
    response = client.get("/api/v1/customers?min_monetary=10000&max_monetary=500")
    assert response.status_code == 400
    err = response.json()
    assert "detail" in err
    assert "min_monetary cannot be greater than max_monetary" in err["detail"]


def test_empty_filter_results_returns_200_empty_list(client):
    """Kiểm tra khi bộ lọc không có bản ghi nào khớp thì trả về list rỗng, total = 0 và status 200 (không bị crash 500)."""
    response = client.get("/api/v1/customers?search=NON_EXISTENT_ID_9999999")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["total_pages"] == 0


def test_nonexistent_endpoint_returns_404(client):
    """Kiểm tra gọi endpoint không tồn tại trả về 404 chuẩn."""
    response = client.get("/api/v1/non_existent_route")
    assert response.status_code == 404
