"""
API Router cho quản lý hệ thống & Nạp dữ liệu trực tiếp từ Website
Prefix: /api/v1/system
"""

import logging
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from pydantic import BaseModel

from app.services.seed_service import SeedService

logger = logging.getLogger("system_api")
router = APIRouter()


class SeedResponse(BaseModel):
    status: str
    message: str
    duration_seconds: Optional[float] = None
    total_inserted: Optional[int] = None
    summary: Optional[dict] = None


@router.get(
    "/status",
    summary="Kiểm tra trạng thái cơ sở dữ liệu và số lượng bản ghi",
    description="Trả về thông tin kết nối MongoDB và số lượng document trong từng collection.",
    status_code=status.HTTP_200_OK,
)
async def get_system_status():
    """Lấy trạng thái kết nối và số lượng dữ liệu hiện có."""
    service = SeedService()
    res = service.get_status()
    return res


@router.post(
    "/seed",
    response_model=SeedResponse,
    summary="Nạp dữ liệu mẫu 1-Click từ Website",
    description="Chạy pipeline nạp toàn bộ dữ liệu chuẩn (Khách hàng, Hóa đơn, Doanh thu, Phân cụm RFM/K-Means) vào MongoDB Atlas.",
    status_code=status.HTTP_200_OK,
)
async def trigger_seed_database():
    """Kích hoạt nạp dữ liệu mẫu vào cơ sở dữ liệu."""
    try:
        service = SeedService()
        result = service.seed_all()
        return SeedResponse(
            status="success",
            message=f"Đã nạp thành công {result['total_inserted']:,} bản ghi vào MongoDB!",
            duration_seconds=result.get("duration_seconds"),
            total_inserted=result.get("total_inserted"),
            summary=result.get("summary"),
        )
    except Exception as e:
        logger.error(f"Lỗi khi seed database qua web: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Không thể nạp dữ liệu: {str(e)}",
        )


@router.post(
    "/upload",
    summary="Tải lên và nạp file CSV trực tiếp",
    description="Nhận file CSV từ giao diện người dùng và nạp vào collection tương ứng.",
    status_code=status.HTTP_200_OK,
)
async def upload_csv_file(
    file: UploadFile = File(..., description="File CSV dữ liệu"),
    collection_type: str = Form("invoices", description="Loại dữ liệu (invoices, segments, generic)"),
):
    """Tải lên file CSV để nạp trực tiếp vào Database."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chỉ hỗ trợ file định dạng .csv",
        )
    
    try:
        content = await file.read()
        service = SeedService()
        res = service.ingest_uploaded_csv(content, file.filename, collection_type)
        return {
            "status": "success",
            "message": f"Đã nạp thành công {res['inserted_count']} bản ghi từ {file.filename}!",
            "details": res,
        }
    except Exception as e:
        logger.error(f"Lỗi khi xử lý file tải lên: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi xử lý file: {str(e)}",
        )
