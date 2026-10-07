"""
Repository truy vấn dữ liệu Phân cụm khách hàng & Đánh giá KMeans từ MongoDB
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import Collections
from app.repositories.base import execute_find_one, execute_find_list


class SegmentationRepository:
    """Xử lý truy vấn dữ liệu Phân cụm K-Means và các chỉ số Silhouette / Inertia."""

    @staticmethod
    async def get_clusters_summary(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
        """Lấy bảng tổng hợp đặc trưng và phân bổ của tất cả các cụm."""
        cursor = db[Collections.CUSTOMER_SEGMENTS_SUMMARY].find({}).sort("cluster", 1)
        docs = await execute_find_list(cursor)
        items = []
        for doc in docs:
            items.append({
                "cluster": int(doc["cluster"]),
                "membership_tier": str(doc["membership_tier"]),
                "customer_count": int(doc["customer_count"]),
                "customer_pct": round(float(doc["customer_pct"]), 2),
                "recency_mean": round(float(doc["recency_mean"]), 2),
                "recency_median": round(float(doc["recency_median"]), 2),
                "frequency_mean": round(float(doc["frequency_mean"]), 2),
                "frequency_median": round(float(doc["frequency_median"]), 2),
                "monetary_mean": round(float(doc["monetary_mean"]), 2),
                "monetary_median": round(float(doc["monetary_median"]), 2),
                "total_monetary": round(float(doc["total_monetary"]), 2),
                "revenue_share_pct": round(float(doc["revenue_share_pct"]), 2),
            })
        return items

    @staticmethod
    async def get_cluster_by_id(db: AsyncIOMotorDatabase, cluster_id: int) -> Optional[Dict[str, Any]]:
        """Lấy thông tin tổng hợp của một cụm K-Means cụ thể."""
        doc = await execute_find_one(db[Collections.CUSTOMER_SEGMENTS_SUMMARY], {"cluster": cluster_id})
        if not doc:
            return None
        return {
            "cluster": int(doc["cluster"]),
            "membership_tier": str(doc["membership_tier"]),
            "customer_count": int(doc["customer_count"]),
            "customer_pct": round(float(doc["customer_pct"]), 2),
            "recency_mean": round(float(doc["recency_mean"]), 2),
            "recency_median": round(float(doc["recency_median"]), 2),
            "frequency_mean": round(float(doc["frequency_mean"]), 2),
            "frequency_median": round(float(doc["frequency_median"]), 2),
            "monetary_mean": round(float(doc["monetary_mean"]), 2),
            "monetary_median": round(float(doc["monetary_median"]), 2),
            "total_monetary": round(float(doc["total_monetary"]), 2),
            "revenue_share_pct": round(float(doc["revenue_share_pct"]), 2),
        }

    @staticmethod
    async def get_kmeans_evaluation(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
        """Lấy danh sách các chỉ số Elbow WCSS và Silhouette Score theo K."""
        cursor = db[Collections.KMEANS_EVALUATION].find({}).sort("k", 1)
        docs = await execute_find_list(cursor)
        items = []
        for doc in docs:
            items.append({
                "k": int(doc["k"]),
                "inertia": round(float(doc["inertia"]), 2),
                "silhouette_score": round(float(doc["silhouette_score"]), 4),
            })
        return items
