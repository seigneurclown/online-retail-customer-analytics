"""
Pydantic Schemas cho Statistical Tests & Descriptive Analytics (Phase 7)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import Optional
from pydantic import BaseModel, Field


class StatisticalTestItem(BaseModel):
    """Chi tiết kết quả một phép kiểm định giả thuyết thống kê đã thực hiện."""
    id: int = Field(..., description="Mã định danh kiểm định (1, 2...)")
    research_question: str = Field(..., description="Câu hỏi nghiên cứu kinh doanh")
    test_name: str = Field(..., description="Tên phép kiểm định thống kê (VD: Mann-Whitney U, Chi-Square)")
    reason: str = Field(..., description="Lý do lựa chọn phép kiểm định phù hợp bản chất phân phối dữ liệu")
    test_statistic: str = Field(..., description="Giá trị đại lượng thống kê kiểm định")
    p_value: Optional[float] = Field(None, description="Giá trị p-value kiểm định")
    significance_level: str = Field(..., description="Mức ý nghĩa alpha (VD: alpha = 0.05)")
    conclusion: str = Field(..., description="Kết luận ý nghĩa thống kê và bài học kinh doanh")


class InvoiceValueSummaryItem(BaseModel):
    """Chỉ số thống kê mô tả phân phối giá trị hóa đơn (Mean, Std, Median, IQR, Max, Skewness)."""
    metric: str = Field(..., description="Tên chỉ số thống kê mô tả (VD: Count, Mean, Median, Skewness)")
    value: float = Field(..., description="Giá trị của chỉ số tương ứng")
