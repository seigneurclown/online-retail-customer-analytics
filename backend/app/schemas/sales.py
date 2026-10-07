"""
Pydantic Schemas cho Sales APIs (Phase 4)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import Optional
from pydantic import BaseModel, Field


class MonthlySalesItem(BaseModel):
    """Chi tiết doanh thu một tháng theo quy chuẩn analytics."""
    year_month: str = Field(..., description="Tháng năm (YYYY-MM)")
    gross_revenue: float = Field(..., description="Tổng doanh thu thô")
    cancelled_revenue: float = Field(..., description="Doanh thu từ đơn bị hủy (số âm)")
    net_revenue: float = Field(..., description="Doanh thu thực tế")
    invoice_count: int = Field(..., description="Số lượng hóa đơn")
    total_quantity: int = Field(..., description="Tổng số lượng sản phẩm bán ra")


class ProductSalesItem(BaseModel):
    """Thông tin bán hàng theo từng sản phẩm."""
    stock_code: str = Field(..., description="Mã sản phẩm")
    description: Optional[str] = Field(None, description="Tên / mô tả sản phẩm")
    total_revenue: float = Field(..., description="Doanh thu tạo ra")
    total_quantity: int = Field(..., description="Số lượng đã bán")
    order_count: int = Field(..., description="Số lần đặt hàng")


class CountrySalesItem(BaseModel):
    """Thông tin doanh thu theo quốc gia."""
    country: str = Field(..., description="Tên quốc gia")
    total_revenue: float = Field(..., description="Tổng doanh thu")
    invoice_count: int = Field(..., description="Số hóa đơn")
    customer_count: int = Field(..., description="Số khách hàng")
    percentage_share: float = Field(..., description="Tỷ lệ % doanh thu")


class InvoiceItem(BaseModel):
    """Chi tiết một đơn hàng trong danh sách hóa đơn."""
    invoice_no: str = Field(..., description="Mã hóa đơn")
    invoice_date: str = Field(..., description="Thời điểm phát sinh đơn")
    customer_id: Optional[str] = Field(None, description="Mã khách hàng")
    country: str = Field(..., description="Quốc gia")
    is_cancelled: bool = Field(..., description="Trạng thái hủy đơn")
    invoice_value: float = Field(..., description="Tổng giá trị đơn hàng (GBP)")
    total_quantity: int = Field(..., description="Tổng số lượng sản phẩm")
    item_count: int = Field(..., description="Số lượng mặt hàng khác nhau")
