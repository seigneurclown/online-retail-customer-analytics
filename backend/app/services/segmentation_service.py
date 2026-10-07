"""
Service xử lý Business Logic cho Phân cụm khách hàng (Phase 6)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.segmentation_repository import SegmentationRepository
from app.schemas.segmentation import ClusterSummaryItem, KMeansEvaluationItem


class SegmentationService:
    """Điều phối nghiệp vụ phân cụm khách hàng và đánh giá mô hình K-Means."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.repo = SegmentationRepository()

    async def get_clusters_summary(self) -> List[ClusterSummaryItem]:
        """Lấy danh sách tổng hợp tất cả các cụm phân khúc."""
        data = await self.repo.get_clusters_summary(self.db)
        return [ClusterSummaryItem(**item) for item in data]

    async def get_cluster_detail(self, cluster_id: int) -> ClusterSummaryItem:
        """Lấy thông tin chi tiết một cụm K-Means. Ném mã 404 nếu không tìm thấy."""
        doc = await self.repo.get_cluster_by_id(self.db, cluster_id=cluster_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Cluster with ID '{cluster_id}' not found in segmentation summary.",
            )
        return ClusterSummaryItem(**doc)

    async def get_kmeans_evaluation(self) -> List[KMeansEvaluationItem]:
        """Lấy các chỉ số đánh giá thuật toán K-Means qua các giá trị K."""
        data = await self.repo.get_kmeans_evaluation(self.db)
        return [KMeansEvaluationItem(**item) for item in data]
