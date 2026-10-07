"""
Cấu hình ứng dụng tập trung (Application Settings) sử dụng Pydantic v2 Settings.
Đọc cấu hình từ biến môi trường hoặc file .env
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Toàn bộ cấu hình hệ thống Backend.
    Hỗ trợ đọc từ biến môi trường hoặc file .env
    """

    # --- Thông tin chung ---
    APP_NAME: str = "Online Retail Analytics API"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # --- Cấu hình Server ---
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # --- Cấu hình MongoDB NoSQL ---
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DATABASE: str = "online_retail"
    MONGODB_TEST_DATABASE: str = "online_retail_test"

    # --- Cấu hình CORS (Cho phép React Frontend kết nối) ---
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Chuẩn hóa danh sách origins từ chuỗi JSON hoặc chuỗi ngăn cách bằng dấu phẩy."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Singleton settings instance
settings = Settings()
