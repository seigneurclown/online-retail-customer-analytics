"""
Pydantic Schemas cho Customer Segmentation & KMeans Evaluation (Phase 6)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List
from pydantic import BaseModel, Field


class ClusterSummaryItem(BaseModel):
    """Thông tin tổng hợp đặc trưng và phân phối doanh thu của một cụm khách hàng."""
    cluster: int = Field(..., description="Mã số cụm K-Means phân bổ (0, 1, 2...)")
    membership_tier: str = Field(..., description="Tên hạng thành viên phản ánh trong kết quả analytics")
    customer_count: int = Field(..., description="Số lượng khách hàng trong cụm")
    customer_pct: float = Field(..., description="Tỷ lệ % khách hàng của cụm so với toàn bộ")
    recency_mean: float = Field(..., description="Recency trung bình (ngày)")
    recency_median: float = Field(..., description="Recency trung vị (ngày)")
    frequency_mean: float = Field(..., description="Frequency trung bình")
    frequency_median: float = Field(..., description="Frequency trung vị")
    monetary_mean: float = Field(..., description="Monetary trung bình (GBP)")
    monetary_median: float = Field(..., description="Monetary trung vị (GBP)")
    total_monetary: float = Field(..., description="Tổng giá trị chi tiêu đóng góp của cụm (GBP)")
    revenue_share_pct: float = Field(..., description="Tỷ trọng doanh thu đóng góp (%)")


class KMeansEvaluationItem(BaseModel):
    """Chỉ số đánh giá thuật toán phân cụm K-Means theo từng giá trị K (Elbow & Silhouette)."""
    k: int = Field(..., description="Số lượng cụm K được thử nghiệm")
    inertia: float = Field(..., description="WCSS (Inertia) đo lường độ phân tán nội cụm")
    silhouette_score: float = Field(..., description="Hệ số Silhouette đo lường mức độ phân tách giữa các cụm")
