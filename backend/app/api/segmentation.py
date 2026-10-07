"""
API Routers cho Phân cụm khách hàng & Đánh giá KMeans (Phase 6)
Prefix: /api/v1/segmentation
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List
from fastapi import APIRouter, Depends, Path, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import get_database
from app.services.segmentation_service import SegmentationService
from app.schemas.segmentation import ClusterSummaryItem, KMeansEvaluationItem

router = APIRouter()


@router.get(
    "/summary",
    response_model=List[ClusterSummaryItem],
    summary="Customer Segments Summary",
    description="Trả về bảng tổng hợp các nhóm khách hàng theo cụm K-Means kèm đặc trưng Recency, Frequency, Monetary và tỷ trọng doanh thu.",
    status_code=status.HTTP_200_OK,
)
async def get_clusters_summary(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Lấy số liệu tổng hợp tất cả các cụm phân khúc khách hàng."""
    service = SegmentationService(db)
    return await service.get_clusters_summary()


@router.get(
    "/clusters/{cluster_id}",
    response_model=ClusterSummaryItem,
    summary="Specific Cluster Profile",
    description="Lấy thông tin chi tiết một cụm K-Means cụ thể theo mã cluster (0, 1, 2...). Trả về 404 nếu mã cụm không tồn tại.",
    status_code=status.HTTP_200_OK,
)
async def get_cluster_detail(
    cluster_id: int = Path(..., ge=0, description="Mã cụm K-Means (VD: 0, 1, hoặc 2)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Tra cứu chi tiết đặc trưng của một cụm phân khúc."""
    service = SegmentationService(db)
    return await service.get_cluster_detail(cluster_id=cluster_id)


@router.get(
    "/evaluation",
    response_model=List[KMeansEvaluationItem],
    summary="K-Means Evaluation Metrics (Elbow & Silhouette)",
    description="Trả về bảng đánh giá thuật toán K-Means qua các giá trị K: độ phân tán WCSS (Inertia) và điểm hệ số tách biệt Silhouette Score.",
    status_code=status.HTTP_200_OK,
)
async def get_kmeans_evaluation(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Lấy dữ liệu đồ thị Elbow Curve và Silhouette Score phục vụ trực quan hóa."""
    service = SegmentationService(db)
    return await service.get_kmeans_evaluation()
