"""
Service xử lý Business Logic cho Customer & RFM (Phase 5)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import Optional
from fastapi import HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerListItem, CustomerDetailResponse
from app.utils.pagination import PaginatedResponse


class CustomerService:
    """Điều phối nghiệp vụ truy vấn danh sách khách hàng và thông tin chi tiết RFM."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.repo = CustomerRepository()

    async def get_customers_paginated(
        self,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        cluster: Optional[int] = None,
        membership_tier: Optional[str] = None,
        min_recency: Optional[int] = None,
        max_recency: Optional[int] = None,
        min_frequency: Optional[int] = None,
        max_frequency: Optional[int] = None,
        min_monetary: Optional[float] = None,
        max_monetary: Optional[float] = None,
    ) -> PaginatedResponse[CustomerListItem]:
        """Truy vấn danh sách khách hàng có phân trang và bộ lọc chuyên sâu."""
        items, total = await self.repo.get_customers_paginated(
            self.db,
            page=page,
            page_size=page_size,
            search=search,
            cluster=cluster,
            membership_tier=membership_tier,
            min_recency=min_recency,
            max_recency=max_recency,
            min_frequency=min_frequency,
            max_frequency=max_frequency,
            min_monetary=min_monetary,
            max_monetary=max_monetary,
        )
        data = [CustomerListItem(**item) for item in items]
        return PaginatedResponse.create(items=data, page=page, page_size=page_size, total=total)

    async def get_customer_detail(self, customer_id: str) -> CustomerDetailResponse:
        """Lấy chi tiết một khách hàng. Ném lỗi 404 nếu không tìm thấy."""
        doc = await self.repo.get_customer_by_id(self.db, customer_id=customer_id)
        if not doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Customer with ID '{customer_id}' not found in segmentation data.",
            )
        return CustomerDetailResponse(**doc)
