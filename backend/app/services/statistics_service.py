"""
Service xử lý Business Logic cho Kiểm định Thống kê & Descriptive Summary (Phase 7)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.statistics_repository import StatisticsRepository
from app.schemas.statistics import StatisticalTestItem, InvoiceValueSummaryItem


class StatisticsService:
    """Điều phối nghiệp vụ truy xuất kết quả phân tích thống kê."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.repo = StatisticsRepository()

    async def get_statistical_tests(self) -> List[StatisticalTestItem]:
        """Lấy danh sách các phép kiểm định thống kê và kết luận kinh doanh tương ứng."""
        data = await self.repo.get_statistical_tests(self.db)
        return [StatisticalTestItem(**item) for item in data]

    async def get_invoice_value_summary(self) -> List[InvoiceValueSummaryItem]:
        """Lấy các chỉ số thống kê mô tả phân phối giá trị đơn hàng."""
        data = await self.repo.get_invoice_value_summary(self.db)
        return [InvoiceValueSummaryItem(**item) for item in data]
