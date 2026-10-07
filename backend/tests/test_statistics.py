"""
Kiểm thử tự động cho Statistical Tests & Descriptive Summary APIs (Phase 7)
"""

import pytest


def test_get_statistical_tests(client):
    """Kiểm tra endpoint /api/v1/statistics/tests trả về danh sách các phép kiểm định."""
    response = client.get("/api/v1/statistics/tests")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 2

    # Kiểm tra phép kiểm định Mann-Whitney U và Chi-Square
    test_names = [t["test_name"] for t in items]
    assert any("Mann-Whitney" in name for name in test_names)
    assert any("Chi-Square" in name for name in test_names)

    first = items[0]
    assert "research_question" in first
    assert "reason" in first
    assert "test_statistic" in first
    assert "p_value" in first
    assert "significance_level" in first
    assert "conclusion" in first


def test_get_invoice_value_summary(client):
    """Kiểm tra endpoint /api/v1/statistics/invoice-value-summary trả về thống kê mô tả."""
    response = client.get("/api/v1/statistics/invoice-value-summary")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 8

    metrics = {item["metric"]: item["value"] for item in items}
    # Tìm kiếm các chỉ số cơ bản
    has_mean = any("Mean" in k for k in metrics.keys())
    has_median = any("Median" in k for k in metrics.keys())
    has_count = any("Count" in k for k in metrics.keys())
    assert has_mean
    assert has_median
    assert has_count
