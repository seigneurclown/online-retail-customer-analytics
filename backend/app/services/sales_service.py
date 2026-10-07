"""
Service xử lý Business Logic cho Bán hàng (Sales) (Phase 4)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.sales_repository import SalesRepository
from app.schemas.sales import (
    MonthlySalesItem,
    ProductSalesItem,
    CountrySalesItem,
    InvoiceItem,
)
from app.utils.pagination import PaginatedResponse


class SalesService:
    """Điều phối nghiệp vụ truy vấn bán hàng, sản phẩm, quốc gia và hóa đơn."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.repo = SalesRepository()

    async def get_monthly_sales(self, year: Optional[str] = None) -> List[MonthlySalesItem]:
        """Lấy danh sách doanh thu theo tháng có thể lọc theo năm."""
        data = await self.repo.get_monthly_sales(self.db, year=year)
        return [MonthlySalesItem(**item) for item in data]

    async def get_products_paginated(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        sort_by: str = "total_revenue",
        order: str = "desc",
    ) -> PaginatedResponse[ProductSalesItem]:
        """Lấy danh sách sản phẩm phân trang."""
        items, total = await self.repo.get_products_paginated(
            self.db,
            page=page,
            page_size=page_size,
            search=search,
            sort_by=sort_by,
            order=order,
        )
        data = [ProductSalesItem(**item) for item in items]
        return PaginatedResponse.create(items=data, page=page, page_size=page_size, total=total)

    async def get_countries_paginated(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        sort_by: str = "total_revenue",
        order: str = "desc",
    ) -> PaginatedResponse[CountrySalesItem]:
        """Lấy danh sách doanh thu theo quốc gia phân trang."""
        items, total = await self.repo.get_countries_paginated(
            self.db,
            page=page,
            page_size=page_size,
            search=search,
            sort_by=sort_by,
            order=order,
        )
        data = [CountrySalesItem(**item) for item in items]
        return PaginatedResponse.create(items=data, page=page, page_size=page_size, total=total)

    async def get_invoices_paginated(
        self,
        page: int = 1,
        page_size: int = 20,
        country: Optional[str] = None,
        is_cancelled: Optional[bool] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> PaginatedResponse[InvoiceItem]:
        """Lấy danh sách hóa đơn phân trang kết hợp nhiều bộ lọc."""
        items, total = await self.repo.get_invoices_paginated(
            self.db,
            page=page,
            page_size=page_size,
            country=country,
            is_cancelled=is_cancelled,
            min_value=min_value,
            max_value=max_value,
        )
        data = [InvoiceItem(**item) for item in items]
        return PaginatedResponse.create(items=data, page=page, page_size=page_size, total=total)
