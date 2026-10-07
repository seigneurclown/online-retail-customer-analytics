"""
API Routers cho Bán hàng & Doanh thu (Phase 4)
Prefix: /api/v1/sales
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import get_database
from app.services.sales_service import SalesService
from app.schemas.sales import (
    MonthlySalesItem,
    ProductSalesItem,
    CountrySalesItem,
    InvoiceItem,
)
from app.utils.pagination import PaginatedResponse

router = APIRouter()


@router.get(
    "/monthly",
    response_model=List[MonthlySalesItem],
    summary="Monthly Sales Breakdown",
    description="Lấy chi tiết doanh thu theo từng tháng (gross, cancelled, net, order count). Có thể lọc theo năm (VD: ?year=2011).",
    status_code=status.HTTP_200_OK,
)
async def get_monthly_sales(
    year: Optional[str] = Query(None, description="Lọc theo năm 4 chữ số (VD: 2010 hoặc 2011)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Lấy dữ liệu phân tích doanh thu theo tháng."""
    service = SalesService(db)
    return await service.get_monthly_sales(year=year)


@router.get(
    "/products",
    response_model=PaginatedResponse[ProductSalesItem],
    summary="Products Sales List",
    description="Danh sách sản phẩm có phân trang, tìm kiếm theo tên/mã và sắp xếp theo doanh thu hoặc số lượng bán.",
    status_code=status.HTTP_200_OK,
)
async def get_products_sales(
    page: int = Query(1, ge=1, description="Số thứ tự trang (>= 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Số bản ghi mỗi trang (1-100)"),
    search: Optional[str] = Query(None, description="Từ khóa tìm kiếm theo tên hoặc mã sản phẩm"),
    sort_by: str = Query("total_revenue", description="Trường cần sắp xếp: total_revenue, total_quantity, order_count"),
    order: str = Query("desc", pattern="^(asc|desc)$", description="Thứ tự: 'asc' hoặc 'desc'"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Lấy danh sách sản phẩm phân trang phục vụ bảng dữ liệu frontend."""
    service = SalesService(db)
    return await service.get_products_paginated(
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        order=order,
    )


@router.get(
    "/countries",
    response_model=PaginatedResponse[CountrySalesItem],
    summary="Country Revenue List",
    description="Danh sách doanh thu theo quốc gia có phân trang, tìm kiếm theo tên nước và sắp xếp.",
    status_code=status.HTTP_200_OK,
)
async def get_country_sales(
    page: int = Query(1, ge=1, description="Số thứ tự trang (>= 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Số bản ghi mỗi trang (1-100)"),
    search: Optional[str] = Query(None, description="Từ khóa tìm kiếm tên quốc gia"),
    sort_by: str = Query("total_revenue", description="Trường sắp xếp: total_revenue, invoice_count, customer_count"),
    order: str = Query("desc", pattern="^(asc|desc)$", description="Thứ tự: 'asc' hoặc 'desc'"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Lấy danh sách doanh thu các quốc gia có phân trang."""
    service = SalesService(db)
    return await service.get_countries_paginated(
        page=page,
        page_size=page_size,
        search=search,
        sort_by=sort_by,
        order=order,
    )


@router.get(
    "/invoices",
    response_model=PaginatedResponse[InvoiceItem],
    summary="Invoice Transactions List",
    description="Danh sách hóa đơn bán lẻ có phân trang kết hợp các bộ lọc quốc gia, trạng thái hủy đơn và khoảng giá trị.",
    status_code=status.HTTP_200_OK,
)
async def get_invoices(
    page: int = Query(1, ge=1, description="Số thứ tự trang (>= 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Số bản ghi mỗi trang (1-100)"),
    country: Optional[str] = Query(None, description="Lọc chính xác theo tên quốc gia"),
    is_cancelled: Optional[bool] = Query(None, description="Lọc theo trạng thái hủy (true/false)"),
    min_value: Optional[float] = Query(None, ge=0, description="Giá trị đơn hàng tối thiểu (£)"),
    max_value: Optional[float] = Query(None, ge=0, description="Giá trị đơn hàng tối đa (£)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Lấy danh sách các đơn hàng giao dịch có phân trang."""
    if min_value is not None and max_value is not None and min_value > max_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_value cannot be greater than max_value.",
        )

    service = SalesService(db)
    return await service.get_invoices_paginated(
        page=page,
        page_size=page_size,
        country=country,
        is_cancelled=is_cancelled,
        min_value=min_value,
        max_value=max_value,
    )
