"""
Pydantic Schemas cho Customer & RFM APIs (Phase 5)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class CustomerListItem(BaseModel):
    """Thông tin khách hàng kèm chỉ số RFM và Phân cụm hiển thị trong bảng."""
    customer_id: str = Field(..., description="Mã khách hàng định danh duy nhất")
    countries: List[str] = Field(default_factory=list, description="Danh sách quốc gia phát sinh giao dịch")
    recency: Optional[int] = Field(None, description="Số ngày kể từ lần mua gần nhất")
    frequency: Optional[int] = Field(None, description="Tổng số lần đặt hàng thành công")
    monetary: Optional[float] = Field(None, description="Tổng số tiền đã chi tiêu (GBP)")
    cluster: Optional[int] = Field(None, description="Mã cụm K-Means phân bổ (0, 1, 2...)")
    membership_tier: Optional[str] = Field(None, description="Tên hạng thành viên trong kết quả analytics")


class CustomerDetailResponse(BaseModel):
    """Thông tin chi tiết một khách hàng cụ thể."""
    customer_id: str = Field(..., description="Mã khách hàng")
    countries: List[str] = Field(default_factory=list, description="Danh sách quốc gia của khách hàng")
    recency: int = Field(..., description="Recency (ngày)")
    frequency: int = Field(..., description="Frequency (số đơn)")
    monetary: float = Field(..., description="Monetary (tổng tiền)")
    cluster: int = Field(..., description="Cụm K-Means phân bổ")
    membership_tier: str = Field(..., description="Hạng thành viên chính xác từ dữ liệu phân tích")
