"""
Service xử lý Business Logic cho Dashboard (Phase 3)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    RevenueTrendResponse,
    RevenueTrendItem,
    TopProductItem,
    TopCountryItem,
)


class DashboardService:
    """Điều phối nghiệp vụ và định dạng dữ liệu cho Dashboard."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.repo = DashboardRepository()

    async def get_summary(self) -> DashboardSummaryResponse:
        """Lấy 4 chỉ số KPI chính của hệ thống."""
        metrics = await self.repo.get_summary_metrics(self.db)
        return DashboardSummaryResponse(**metrics)

    async def get_revenue_trend(self) -> RevenueTrendResponse:
        """Lấy danh sách doanh thu theo từng tháng."""
        trend_data = await self.repo.get_revenue_trend(self.db)
        items = [RevenueTrendItem(**item) for item in trend_data]
        return RevenueTrendResponse(items=items)

    async def get_top_products(self, limit: int = 10) -> List[TopProductItem]:
        """Lấy top sản phẩm bán chạy nhất."""
        products_data = await self.repo.get_top_products(self.db, limit=limit)
        return [TopProductItem(**item) for item in products_data]

    async def get_top_countries(self, limit: int = 10) -> List[TopCountryItem]:
        """Lấy top quốc gia đóng góp doanh thu cao nhất."""
        countries_data = await self.repo.get_top_countries(self.db, limit=limit)
        return [TopCountryItem(**item) for item in countries_data]
