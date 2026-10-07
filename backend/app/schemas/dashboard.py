"""
Pydantic Schemas cho Dashboard APIs (Phase 3)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class DashboardSummaryResponse(BaseModel):
    """Schema dữ liệu tổng quan cho KPI cards trên Dashboard."""
    total_revenue: float = Field(..., description="Tổng doanh thu thuần từ khách hàng (GBP)")
    total_orders: int = Field(..., description="Tổng số đơn hàng thành công")
    total_customers: int = Field(..., description="Tổng số lượng khách hàng duy nhất")
    average_order_value: float = Field(..., description="Giá trị trung bình trên một đơn hàng (AOV)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total_revenue": 8291748.56,
                "total_orders": 19960,
                "total_customers": 4339,
                "average_order_value": 533.17
            }
        }
    }


class RevenueTrendItem(BaseModel):
    """Mỗi điểm dữ liệu biểu đồ xu hướng doanh thu theo tháng."""
    year_month: str = Field(..., description="Năm-tháng (YYYY-MM)")
    revenue: float = Field(..., description="Doanh thu thực tế (NetRevenue)")


class RevenueTrendResponse(BaseModel):
    """Schema danh sách xu hướng doanh thu theo tháng."""
    items: List[RevenueTrendItem] = Field(..., description="Danh sách các tháng kèm doanh thu")


class TopProductItem(BaseModel):
    """Dữ liệu sản phẩm bán chạy nhất."""
    stock_code: str = Field(..., description="Mã sản phẩm")
    description: Optional[str] = Field(None, description="Tên sản phẩm")
    total_revenue: float = Field(..., description="Tổng doanh thu mang lại (GBP)")
    total_quantity: int = Field(..., description="Tổng số lượng sản phẩm bán ra")
    order_count: int = Field(..., description="Số lượng đơn hàng chứa sản phẩm này")


class TopCountryItem(BaseModel):
    """Dữ liệu quốc gia đóng góp doanh thu lớn nhất."""
    country: str = Field(..., description="Tên quốc gia")
    total_revenue: float = Field(..., description="Tổng doanh thu từ quốc gia này (GBP)")
    invoice_count: int = Field(..., description="Tổng số lượng hóa đơn")
    customer_count: int = Field(..., description="Số lượng khách hàng")
    percentage_share: float = Field(..., description="Tỷ trọng đóng góp doanh thu (%)")
