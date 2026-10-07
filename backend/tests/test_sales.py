"""
Kiểm thử tự động cho Sales APIs (Phase 4)
"""

import pytest


def test_get_monthly_sales_all(client):
    """Kiểm tra lấy toàn bộ doanh thu các tháng."""
    response = client.get("/api/v1/sales/monthly")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 12
    for item in data:
        assert "year_month" in item
        assert "gross_revenue" in item
        assert "net_revenue" in item


def test_get_monthly_sales_filtered_by_year(client):
    """Kiểm tra lọc doanh thu theo năm cụ thể (VD: 2011)."""
    response = client.get("/api/v1/sales/monthly?year=2011")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    for item in data:
        assert item["year_month"].startswith("2011")


def test_get_products_pagination_and_search(client):
    """Kiểm tra phân trang và tìm kiếm sản phẩm."""
    # Phân trang
    response = client.get("/api/v1/sales/products?page=1&page_size=10")
    assert response.status_code == 200
    res = response.json()
    assert res["page"] == 1
    assert res["page_size"] == 10
    assert res["total"] > 0
    assert len(res["items"]) <= 10

    # Tìm kiếm
    search_res = client.get("/api/v1/sales/products?search=HEART")
    assert search_res.status_code == 200
    s_data = search_res.json()
    assert s_data["total"] >= 1


def test_get_countries_pagination(client):
    """Kiểm tra danh sách doanh thu theo quốc gia có phân trang."""
    response = client.get("/api/v1/sales/countries?page=1&page_size=5")
    assert response.status_code == 200
    res = response.json()
    assert res["page"] == 1
    assert res["page_size"] == 5
    assert len(res["items"]) <= 5


def test_get_invoices_pagination_and_filter(client):
    """Kiểm tra phân trang hóa đơn và bộ lọc trạng thái hủy đơn."""
    response = client.get("/api/v1/sales/invoices?page=1&page_size=15&is_cancelled=false")
    assert response.status_code == 200
    res = response.json()
    assert res["page"] == 1
    assert res["page_size"] == 15
    assert res["total"] > 10000
    for item in res["items"]:
        assert item["is_cancelled"] is False
