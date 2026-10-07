"""
Unit Tests cho Seed Database Pipeline và Indexes (Phase 2)
"""

import pytest
import mongomock
from app.core.mongodb import Collections
from scripts.seed_database import run_seed_pipeline


def test_seed_pipeline_with_mock():
    """Kiểm tra pipeline nạp dữ liệu nạp đầy đủ các collections và tạo indexes."""
    client = mongomock.MongoClient()
    db = client["online_retail_test"]

    summary = run_seed_pipeline(db)

    # Kiểm tra tất cả các collection đều có dữ liệu
    assert summary["customers"] > 4000
    assert summary["invoices"] > 20000
    assert summary["customer_rfm"] > 4000
    assert summary["customer_segments"] > 4000
    assert summary["monthly_revenue"] >= 12
    assert summary["country_revenue"] >= 5
    assert summary["product_revenue"] >= 5
    assert summary["statistical_tests"] >= 2
    assert summary["kmeans_evaluation"] >= 5
    assert summary["customer_segments_summary"] == 3
    assert summary["products"] > 3000

    # Kiểm tra mẫu dữ liệu trong collection customers
    sample_cust = db[Collections.CUSTOMERS].find_one({"customer_id": "12347"})
    assert sample_cust is not None
    assert "countries" in sample_cust
    assert len(sample_cust["countries"]) > 0

    # Kiểm tra mẫu dữ liệu trong customer_segments
    sample_seg = db[Collections.CUSTOMER_SEGMENTS].find_one({"customer_id": "12347"})
    assert sample_seg is not None
    assert sample_seg["cluster"] == 2
    assert sample_seg["membership_tier"] == "Thẻ Vàng - Kim Cương (Gold)"

    # Kiểm tra mẫu dữ liệu monthly_revenue
    sample_monthly = db[Collections.MONTHLY_REVENUE].find_one({"year_month": "2010-12"})
    assert sample_monthly is not None
    assert sample_monthly["net_revenue"] > 0
