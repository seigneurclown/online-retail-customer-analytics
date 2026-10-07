"""
API Routers cho Kiểm định thống kê & Thống kê mô tả (Phase 7)
Prefix: /api/v1/statistics
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List
from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import get_database
from app.services.statistics_service import StatisticsService
from app.schemas.statistics import StatisticalTestItem, InvoiceValueSummaryItem

router = APIRouter()


@router.get(
    "/tests",
    response_model=List[StatisticalTestItem],
    summary="Hypothesis Statistical Tests",
    description="Trả về danh sách các phép kiểm định giả thuyết thống kê đã thực hiện (Mann-Whitney U, Chi-Square Independence...) kèm p-value và kết luận.",
    status_code=status.HTTP_200_OK,
)
async def get_statistical_tests(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Lấy danh sách các phép kiểm định thống kê của đề tài."""
    service = StatisticsService(db)
    return await service.get_statistical_tests()


@router.get(
    "/invoice-value-summary",
    response_model=List[InvoiceValueSummaryItem],
    summary="Descriptive Statistics of Invoice Value",
    description="Trả về bảng thống kê mô tả phân phối giá trị hóa đơn (Count, Mean, Std, Min, Q1, Median, Q3, IQR, Max, Skewness).",
    status_code=status.HTTP_200_OK,
)
async def get_invoice_value_summary(db: AsyncIOMotorDatabase = Depends(get_database)):
    """Lấy bảng thống kê mô tả phân phối giá trị đơn hàng."""
    service = StatisticsService(db)
    return await service.get_invoice_value_summary()
