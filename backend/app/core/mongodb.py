"""
MongoDB Connection Manager (NoSQL Database)
Quản lý kết nối Motor (Async) và PyMongo (Sync) cùng hệ thống Indexing
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
Đề tài: Phân tích dữ liệu doanh thu và Phân cụm hành vi khách hàng trong lĩnh vực bán lẻ
"""

import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings

logger = logging.getLogger("online_retail.mongodb")


class Collections:
    """Tên các collections trong MongoDB theo đúng thiết kế NoSQL."""
    CUSTOMERS = "customers"
    INVOICES = "invoices"
    INVOICE_ITEMS = "invoice_items"
    PRODUCTS = "products"
    CUSTOMER_RFM = "customer_rfm"
    CUSTOMER_SEGMENTS = "customer_segments"
    MONTHLY_REVENUE = "monthly_revenue"
    COUNTRY_REVENUE = "country_revenue"
    PRODUCT_REVENUE = "product_revenue"
    STATISTICAL_TESTS = "statistical_tests"
    KMEANS_EVALUATION = "kmeans_evaluation"
    CUSTOMER_SEGMENTS_SUMMARY = "customer_segments_summary"
    INVOICE_VALUE_SUMMARY = "invoice_value_summary"


class MongoDBManager:
    """Quản lý vòng đời kết nối tới MongoDB Async Motor Client."""

    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db: Optional[AsyncIOMotorDatabase] = None

    def connect(self, uri: Optional[str] = None, db_name: Optional[str] = None) -> None:
        """Khởi tạo kết nối tới MongoDB."""
        mongo_uri = uri or settings.MONGODB_URI
        target_db = db_name or settings.MONGODB_DATABASE

        if self.client is None:
            logger.info(f"Đang kết nối MongoDB: {mongo_uri}")
            self.client = AsyncIOMotorClient(
                mongo_uri,
                serverSelectionTimeoutMS=5000,
            )
            self.db = self.client[target_db]
            logger.info(f"Đã kết nối cơ sở dữ liệu: {target_db}")

    def close(self) -> None:
        """Đóng kết nối MongoDB khi ứng dụng dừng."""
        if self.client is not None:
            self.client.close()
            self.client = None
            self.db = None
            logger.info("Đã đóng kết nối MongoDB an toàn.")

    async def check_connection(self) -> bool:
        """Kiểm tra tình trạng sống của MongoDB qua lệnh ping."""
        try:
            if self.client is None:
                self.connect()
            # Thực thi lệnh ping
            await self.client.admin.command("ping")
            return True
        except Exception as e:
            logger.warning(f"Lỗi kết nối MongoDB: {e}")
            return False


# Singleton MongoDB Manager
mongodb_manager = MongoDBManager()


async def get_database() -> AsyncIOMotorDatabase:
    """FastAPI Dependency: Cung cấp Async MongoDB Database cho Routers & Services."""
    if mongodb_manager.db is None:
        mongodb_manager.connect()
    return mongodb_manager.db


def get_sync_database(uri: Optional[str] = None, db_name: Optional[str] = None) -> Database:
    """Cung cấp đồng bộ MongoClient cho scripts (seed, backup)."""
    mongo_uri = uri or settings.MONGODB_URI
    target_db = db_name or settings.MONGODB_DATABASE
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
    return client[target_db]


def create_mongo_indexes(db: Database) -> None:
    """
    Tạo các chỉ mục (Indexes) bắt buộc trong MongoDB theo quy chuẩn Mục 16:
    - customers: customer_id
    - invoices: invoice_no, customer_id, invoice_date, country, is_cancelled
    - invoice_items: invoice_no, stock_code
    - products: stock_code
    - customer_rfm: customer_id
    - customer_segments: customer_id, cluster, membership_tier
    - monthly_revenue: year_month
    - country_revenue: country
    - product_revenue: stock_code
    - statistical_tests: id
    - kmeans_evaluation: k
    """
    logger.info("Bắt đầu tạo MongoDB Indexes...")

    # 1. customers
    db[Collections.CUSTOMERS].create_index("customer_id", unique=True)

    # 2. invoices
    db[Collections.INVOICES].create_index("invoice_no", unique=True)
    db[Collections.INVOICES].create_index("customer_id")
    db[Collections.INVOICES].create_index("invoice_date")
    db[Collections.INVOICES].create_index("country")
    db[Collections.INVOICES].create_index("is_cancelled")

    # 3. invoice_items
    db[Collections.INVOICE_ITEMS].create_index("invoice_no")
    db[Collections.INVOICE_ITEMS].create_index("stock_code")

    # 4. products
    db[Collections.PRODUCTS].create_index("stock_code", unique=True)

    # 5. customer_rfm
    db[Collections.CUSTOMER_RFM].create_index("customer_id", unique=True)

    # 6. customer_segments
    db[Collections.CUSTOMER_SEGMENTS].create_index("customer_id", unique=True)
    db[Collections.CUSTOMER_SEGMENTS].create_index("cluster")
    db[Collections.CUSTOMER_SEGMENTS].create_index("membership_tier")

    # 7. monthly_revenue
    db[Collections.MONTHLY_REVENUE].create_index("year_month", unique=True)

    # 8. country_revenue
    db[Collections.COUNTRY_REVENUE].create_index("country", unique=True)

    # 9. product_revenue
    db[Collections.PRODUCT_REVENUE].create_index("stock_code", unique=True)

    # 10. statistical_tests & kmeans_evaluation
    db[Collections.STATISTICAL_TESTS].create_index("id", unique=True)
    db[Collections.KMEANS_EVALUATION].create_index("k", unique=True)

    logger.info("Tất cả MongoDB Indexes đã được tạo thành công.")
