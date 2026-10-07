"""
API Routers cho màn hình Dashboard (Phase 3)
Prefix: /api/v1/dashboard
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List
from fastapi import APIRouter, Depends, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import get_database
from app.services.dashboard_service import DashboardService
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    RevenueTrendResponse,
    TopProductItem,
    TopCountryItem,
)

router = APIRouter()


@router.get(
    "/summary",
    response_model=DashboardSummaryResponse,
    summary="Dashboard KPI Summary",
    description="Trả về 4 chỉ số cốt lõi: tổng doanh thu, tổng số đơn hàng, tổng số khách hàng và giá trị trung bình đơn (AOV).",
    status_code=status.HTTP_200_OK,
)
async def get_dashboard_summary(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Lấy số liệu KPI tổng quan cho màn hình Dashboard."""
    service = DashboardService(db)
    return await service.get_summary()


@router.get(
    "/revenue-trend",
    response_model=RevenueTrendResponse,
    summary="Monthly Revenue Trend",
    description="Trả về chuỗi doanh thu theo tháng phục vụ vẽ biểu đồ đường (Line Chart) trên frontend.",
    status_code=status.HTTP_200_OK,
)
async def get_revenue_trend(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Lấy dữ liệu xu hướng doanh thu qua các tháng."""
    service = DashboardService(db)
    return await service.get_revenue_trend()


@router.get(
    "/top-products",
    response_model=List[TopProductItem],
    summary="Top Selling Products",
    description="Trả về danh sách các sản phẩm đóng góp doanh thu lớn nhất, có thể giới hạn số lượng bằng query param 'limit'.",
    status_code=status.HTTP_200_OK,
)
async def get_top_products(
    limit: int = Query(10, ge=1, le=100, description="Số lượng sản phẩm cần lấy (1-100)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Lấy danh sách top sản phẩm doanh thu cao."""
    service = DashboardService(db)
    return await service.get_top_products(limit=limit)


@router.get(
    "/top-countries",
    response_model=List[TopCountryItem],
    summary="Top Contributing Countries",
    description="Trả về danh sách các quốc gia có doanh thu cao nhất kèm tỷ trọng phần trăm đóng góp.",
    status_code=status.HTTP_200_OK,
)
async def get_top_countries(
    limit: int = Query(10, ge=1, le=100, description="Số lượng quốc gia cần lấy (1-100)"),
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """Lấy danh sách top quốc gia theo doanh thu."""
    service = DashboardService(db)
    return await service.get_top_countries(limit=limit)
