"""
Kiểm thử tự động cho Customer Segmentation & KMeans Evaluation APIs (Phase 6)
"""

import pytest


def test_get_clusters_summary(client):
    """Kiểm tra endpoint /api/v1/segmentation/summary trả về đầy đủ 3 cụm chuẩn."""
    response = client.get("/api/v1/segmentation/summary")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) == 3

    # Kiểm tra các trường dữ liệu quan trọng
    first = items[0]
    assert "cluster" in first
    assert "membership_tier" in first
    assert "customer_count" in first
    assert "customer_pct" in first
    assert "recency_mean" in first
    assert "frequency_mean" in first
    assert "monetary_mean" in first
    assert "total_monetary" in first
    assert "revenue_share_pct" in first


def test_get_cluster_detail_found(client):
    """Kiểm tra tra cứu chi tiết cụm 2 (Gold / Champions)."""
    response = client.get("/api/v1/segmentation/clusters/2")
    assert response.status_code == 200
    data = response.json()
    assert data["cluster"] == 2
    assert "Gold" in data["membership_tier"] or "Vàng" in data["membership_tier"]
    assert data["customer_count"] > 700
    assert data["revenue_share_pct"] > 60.0


def test_get_cluster_detail_not_found(client):
    """Kiểm tra ném mã lỗi 404 khi tra cứu cụm không tồn tại (VD: cluster 99)."""
    response = client.get("/api/v1/segmentation/clusters/99")
    assert response.status_code == 404
    err = response.json()
    assert "detail" in err
    assert "not found" in err["detail"].lower()


def test_get_kmeans_evaluation(client):
    """Kiểm tra endpoint /api/v1/segmentation/evaluation trả về danh sách K và điểm số."""
    response = client.get("/api/v1/segmentation/evaluation")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 5
    for item in items:
        assert "k" in item
        assert "inertia" in item
        assert "silhouette_score" in item
        assert item["inertia"] > 0
