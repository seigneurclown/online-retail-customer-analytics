"""
Điểm khởi động chính của ứng dụng FastAPI (Main Application Entrypoint)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
Đề tài: Phân tích dữ liệu doanh thu và Phân cụm hành vi khách hàng trong lĩnh vực bán lẻ
Cơ sở dữ liệu: MongoDB (NoSQL)
"""

import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pymongo.errors import PyMongoError

from app.core.config import settings
from app.core.mongodb import mongodb_manager
from app.api.dashboard import router as dashboard_router
from app.api.sales import router as sales_router
from app.api.customers import router as customers_router
from app.api.segmentation import router as segmentation_router
from app.api.statistics import router as statistics_router

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s",
)
logger = logging.getLogger("online_retail.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Quản lý vòng đời ứng dụng:
    - Khi khởi động: Kết nối MongoDB
    - Khi kết thúc: Đóng kết nối MongoDB
    """
    logger.info("Khởi động FastAPI server...")
    try:
        mongodb_manager.connect()
        logger.info(f"MongoDB đã được kết nối: {settings.MONGODB_DATABASE}")
    except Exception as e:
        logger.warning(f"Chưa kết nối được MongoDB khi khởi động: {e}")

    yield

    logger.info("Đang tắt FastAPI server...")
    mongodb_manager.close()
    logger.info("Đã đóng kết nối MongoDB an toàn.")


# Khởi tạo FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Backend REST API phục vụ nền tảng phân tích doanh thu và phân cụm khách hàng "
        "(Online Retail Analytics Platform) kết nối với React Frontend. "
        "Sử dụng NoSQL MongoDB và kiến trúc Clean Code phân tầng."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan,
)

# Cấu hình CORS Middleware
if settings.BACKEND_CORS_ORIGINS:
    origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
    allow_all = "*" in origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=not allow_all,
        allow_methods=["*"],
        allow_headers=["*"],
    )


# --- Request Logging Middleware (Mục 38) ---
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    """Ghi nhận log thời gian xử lý và mã trạng thái cho từng HTTP request."""
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(
            f"{request.method} {request.url.path} -> {response.status_code} ({process_time_ms}ms)"
        )
        return response
    except Exception as exc:
        process_time_ms = round((time.time() - start_time) * 1000, 2)
        logger.error(
            f"{request.method} {request.url.path} -> Exception ({process_time_ms}ms): {exc}"
        )
        raise exc


# --- Global Exception Handlers (Mục 31) ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Xử lý lỗi validate query params / request body, trả về JSON chuẩn HTTP 422."""
    logger.warning(f"422 Validation Error tại {request.method} {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.exception_handler(PyMongoError)
async def pymongo_exception_handler(request: Request, exc: PyMongoError):
    """Bắt lỗi cơ sở dữ liệu MongoDB và trả về HTTP 503 thay vì làm sập server."""
    logger.error(f"MongoDB Error tại {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "Database service is temporarily unavailable. Please try again later."},
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Bắt các ngoại lệ không lường trước được, ghi log traceback nội bộ và ẩn chi tiết nhạy cảm khỏi client (HTTP 500)."""
    logger.exception(f"Unhandled Internal Server Error tại {request.method} {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error. Please contact the administrator."},
    )


# --- Đăng ký toàn bộ API Routers ---
app.include_router(dashboard_router, prefix=f"{settings.API_V1_PREFIX}/dashboard", tags=["Dashboard"])
app.include_router(sales_router, prefix=f"{settings.API_V1_PREFIX}/sales", tags=["Sales"])
app.include_router(customers_router, prefix=f"{settings.API_V1_PREFIX}/customers", tags=["Customers"])
app.include_router(segmentation_router, prefix=f"{settings.API_V1_PREFIX}/segmentation", tags=["Segmentation"])
app.include_router(statistics_router, prefix=f"{settings.API_V1_PREFIX}/statistics", tags=["Statistics"])


@app.get(
    "/",
    tags=["Root"],
    summary="Root Information",
    description="Trả về thông tin tổng quan của ứng dụng và link tới tài liệu OpenAPI Swagger.",
)
def root_info():
    """Thông tin cơ bản về hệ thống khi truy cập trang chủ API."""
    return {
        "app_name": settings.APP_NAME,
        "environment": settings.APP_ENV,
        "database": "MongoDB NoSQL",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "api_v1_prefix": settings.API_V1_PREFIX,
        "health_check": "/health",
        "database_health_check": "/health/db",
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Application Health Check",
    description="Endpoint kiểm tra trạng thái hoạt động của Backend server.",
    status_code=status.HTTP_200_OK,
)
def health_check():
    """Kiểm tra server có phản hồi tốt hay không."""
    return {"status": "ok"}


@app.get(
    "/health/db",
    tags=["Health"],
    summary="Database Health Check",
    description="Endpoint kiểm tra trạng thái kết nối tới cơ sở dữ liệu MongoDB NoSQL.",
)
async def health_check_database():
    """Kiểm tra server có ping được tới MongoDB hay không."""
    is_healthy = await mongodb_manager.check_connection()
    if is_healthy:
        return {
            "status": "ok",
            "database": settings.MONGODB_DATABASE,
        }
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "error",
            "database": settings.MONGODB_DATABASE,
            "message": "Không thể kết nối tới MongoDB. Vui lòng kiểm tra MONGODB_URI.",
        },
    )
