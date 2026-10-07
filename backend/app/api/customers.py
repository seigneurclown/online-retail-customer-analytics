"""
API Routers cho Khách hàng & RFM (Phase 5)
Prefix: /api/v1/customers
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import get_database
from app.services.customer_service import CustomerService
from app.schemas.customer import CustomerListItem, CustomerDetailResponse
from app.utils.pagination import PaginatedResponse

router = APIRouter()


@router.get(
    "",
    response_model=PaginatedResponse[CustomerListItem],
    summary="Customers List with RFM & Clusters",
    description="Danh sách khách hàng phân trang, hỗ trợ tìm kiếm theo ID, lọc theo cụm K-Means, hạng thành viên và các dải giá trị RFM.",
    status_code=status.HTTP_200_OK,
)
async def get_customers(
    page: int = Query(1, ge=1, description="Số thứ tự trang (>= 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Số bản ghi mỗi trang (1-100)"),
    search: Optional[str] = Query(None, description="Tìm kiếm theo mã Customer ID"),
    cluster: Optional[int] = Query(None, description="Lọc theo mã cụm K-Means (0, 1, 2...)"),
    membership_tier: Optional[str] = Query(None, description="Lọc theo tên hạng thành viên"),
    min_recency: Optional[int] = Query(None, ge=0, description="Recency tối thiểu (ngày)"),
    max_recency: Optional[int] = Query(None, ge=0, description="Recency tối đa (ngày)"),
    min_frequency: Optional[int] = Query(None, ge=0, description="Frequency tối thiểu"),
    max_frequency: Optional[int] = Query(None, ge=0, description="Frequency tối đa"),
    min_monetary: Optional[float] = Query(None, ge=0, description="Monetary tối thiểu (£)"),
    max_monetary: Optional[float] = Query(None, ge=0, description="Monetary tối đa (£)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Lấy danh sách khách hàng phân trang kèm các bộ lọc RFM đa chiều."""
    if min_recency is not None and max_recency is not None and min_recency > max_recency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_recency cannot be greater than max_recency.",
        )
    if min_frequency is not None and max_frequency is not None and min_frequency > max_frequency:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_frequency cannot be greater than max_frequency.",
        )
    if min_monetary is not None and max_monetary is not None and min_monetary > max_monetary:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_monetary cannot be greater than max_monetary.",
        )

    service = CustomerService(db)
    return await service.get_customers_paginated(
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


@router.get(
    "/{customer_id}",
    response_model=CustomerDetailResponse,
    summary="Customer Profile Detail",
    description="Thông tin chi tiết hồ sơ một khách hàng cụ thể bao gồm chỉ số RFM, cụm K-Means phân bổ và quốc gia giao dịch.",
    status_code=status.HTTP_200_OK,
)
async def get_customer_by_id(
    customer_id: str = Path(..., description="Mã Customer ID cần tra cứu (VD: 12347)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Tra cứu chi tiết hồ sơ phân khúc của một khách hàng."""
    service = CustomerService(db)
    return await service.get_customer_detail(customer_id=customer_id)
