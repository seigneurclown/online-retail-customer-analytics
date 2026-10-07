"""
Tiện ích phân trang (Pagination Utility)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
Định dạng response chuẩn cho tất cả các API phân trang theo quy định Mục 10 & Mục 27.
"""

from typing import Generic, TypeVar, List
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Mô hình dữ liệu trả về cho danh sách có phân trang."""
    items: List[T] = Field(..., description="Danh sách các bản ghi của trang hiện tại")
    page: int = Field(..., ge=1, description="Số thứ tự trang hiện tại (bắt đầu từ 1)")
    page_size: int = Field(..., ge=1, le=100, description="Số lượng bản ghi trên một trang (tối đa 100)")
    total: int = Field(..., ge=0, description="Tổng số bản ghi thỏa mãn điều kiện lọc")
    total_pages: int = Field(..., ge=0, description="Tổng số trang có thể xem")

    @classmethod
    def create(cls, items: List[T], page: int, page_size: int, total: int):
        """Hàm khởi tạo tiện lợi tự động tính tổng số trang."""
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        return cls(
            items=items,
            page=page,
            page_size=page_size,
            total=total,
            total_pages=total_pages,
        )
