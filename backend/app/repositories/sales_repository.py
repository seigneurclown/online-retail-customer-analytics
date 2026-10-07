"""
Repository truy vấn dữ liệu Bán hàng (Sales) từ MongoDB
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Dict, Any, Optional, Tuple
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import Collections
from app.repositories.base import execute_count, execute_find_list


class SalesRepository:
    """Xử lý truy vấn dữ liệu Sales, Invoices, Monthly và Products."""

    @staticmethod
    async def get_monthly_sales(db: AsyncIOMotorDatabase, year: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lấy danh sách doanh thu theo tháng, có thể lọc theo năm (VD: 2010, 2011)."""
        query = {}
        if year:
            query["year_month"] = {"$regex": f"^{year}"}

        cursor = db[Collections.MONTHLY_REVENUE].find(query).sort("year_month", 1)
        docs = await execute_find_list(cursor)
        results = []
        for doc in docs:
            results.append({
                "year_month": doc["year_month"],
                "gross_revenue": round(float(doc.get("gross_revenue", 0.0)), 2),
                "cancelled_revenue": round(float(doc.get("cancelled_revenue", 0.0)), 2),
                "net_revenue": round(float(doc.get("net_revenue", 0.0)), 2),
                "invoice_count": int(doc.get("invoice_count", 0)),
                "total_quantity": int(doc.get("total_quantity", 0)),
            })
        return results

    @staticmethod
    async def get_products_paginated(
        db: AsyncIOMotorDatabase,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        sort_by: str = "total_revenue",
        order: str = "desc",
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Truy vấn danh sách sản phẩm có phân trang, tìm kiếm và sắp xếp."""
        query = {}
        if search:
            query["$or"] = [
                {"description": {"$regex": search, "$options": "i"}},
                {"stock_code": {"$regex": search, "$options": "i"}},
            ]

        total = await execute_count(db[Collections.PRODUCT_REVENUE], query)

        sort_dir = -1 if order.lower() == "desc" else 1
        valid_sort_fields = {"total_revenue", "total_quantity", "order_count", "stock_code"}
        field_to_sort = sort_by if sort_by in valid_sort_fields else "total_revenue"

        skip = (page - 1) * page_size
        cursor = db[Collections.PRODUCT_REVENUE].find(query).sort(field_to_sort, sort_dir).skip(skip).limit(page_size)
        docs = await execute_find_list(cursor, length=page_size)

        items = []
        for doc in docs:
            items.append({
                "stock_code": doc["stock_code"],
                "description": doc.get("description"),
                "total_revenue": round(float(doc.get("total_revenue", 0.0)), 2),
                "total_quantity": int(doc.get("total_quantity", 0)),
                "order_count": int(doc.get("order_count", 0)),
            })
        return items, total

    @staticmethod
    async def get_countries_paginated(
        db: AsyncIOMotorDatabase,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        sort_by: str = "total_revenue",
        order: str = "desc",
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Truy vấn danh sách doanh thu theo quốc gia có phân trang và sắp xếp."""
        query = {}
        if search:
            query["country"] = {"$regex": search, "$options": "i"}

        total = await execute_count(db[Collections.COUNTRY_REVENUE], query)

        sort_dir = -1 if order.lower() == "desc" else 1
        valid_sort_fields = {"total_revenue", "invoice_count", "customer_count", "percentage_share", "country"}
        field_to_sort = sort_by if sort_by in valid_sort_fields else "total_revenue"

        skip = (page - 1) * page_size
        cursor = db[Collections.COUNTRY_REVENUE].find(query).sort(field_to_sort, sort_dir).skip(skip).limit(page_size)
        docs = await execute_find_list(cursor, length=page_size)

        items = []
        for doc in docs:
            items.append({
                "country": doc["country"],
                "total_revenue": round(float(doc.get("total_revenue", 0.0)), 2),
                "invoice_count": int(doc.get("invoice_count", 0)),
                "customer_count": int(doc.get("customer_count", 0)),
                "percentage_share": round(float(doc.get("percentage_share", 0.0)), 2),
            })
        return items, total

    @staticmethod
    async def get_invoices_paginated(
        db: AsyncIOMotorDatabase,
        page: int = 1,
        page_size: int = 20,
        country: Optional[str] = None,
        is_cancelled: Optional[bool] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Truy vấn danh sách hóa đơn theo các bộ lọc linh hoạt từ frontend."""
        query = {}
        if country:
            query["country"] = {"$regex": f"^{country}$", "$options": "i"}
        if is_cancelled is not None:
            query["is_cancelled"] = is_cancelled

        value_filter = {}
        if min_value is not None:
            value_filter["$gte"] = min_value
        if max_value is not None:
            value_filter["$lte"] = max_value
        if value_filter:
            query["invoice_value"] = value_filter

        total = await execute_count(db[Collections.INVOICES], query)

        skip = (page - 1) * page_size
        cursor = db[Collections.INVOICES].find(query).sort("invoice_date", -1).skip(skip).limit(page_size)
        docs = await execute_find_list(cursor, length=page_size)

        items = []
        for doc in docs:
            items.append({
                "invoice_no": doc["invoice_no"],
                "invoice_date": doc["invoice_date"],
                "customer_id": doc.get("customer_id"),
                "country": doc["country"],
                "is_cancelled": doc["is_cancelled"],
                "invoice_value": round(float(doc.get("invoice_value", 0.0)), 2),
                "total_quantity": int(doc.get("total_quantity", 0)),
                "item_count": int(doc.get("item_count", 0)),
            })
        return items, total
