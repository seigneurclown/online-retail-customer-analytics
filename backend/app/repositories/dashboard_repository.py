"""
Repository truy vấn dữ liệu Dashboard từ MongoDB
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import Collections
from app.repositories.base import execute_count, execute_find_one, execute_find_list


class DashboardRepository:
    """Xử lý toàn bộ thao tác truy vấn dữ liệu MongoDB cho màn hình Dashboard."""

    @staticmethod
    async def get_summary_metrics(db: AsyncIOMotorDatabase) -> Dict[str, Any]:
        """
        Lấy các chỉ số KPI tóm tắt.
        Ưu tiên đọc các giá trị đã được tổng hợp chính xác từ analytics pipeline.
        """
        # 1. Lấy total_revenue từ customer_segments_summary (hoặc tổng monetary)
        total_revenue = 0.0
        seg_docs = await execute_find_list(db[Collections.CUSTOMER_SEGMENTS_SUMMARY].find({}))
        for doc in seg_docs:
            total_revenue += float(doc.get("total_monetary", 0.0))

        if total_revenue == 0.0:
            # Fallback tính tổng net_revenue từ monthly_revenue
            month_docs = await execute_find_list(db[Collections.MONTHLY_REVENUE].find({}))
            for doc in month_docs:
                total_revenue += float(doc.get("net_revenue", 0.0))

        # 2. Lấy total_orders và average_order_value từ invoice_value_summary
        total_orders = 0
        aov = 0.0
        inv_summary = db[Collections.INVOICE_VALUE_SUMMARY]
        count_doc = await execute_find_one(inv_summary, {"metric": {"$regex": "Count", "$options": "i"}})
        if count_doc:
            total_orders = int(float(count_doc.get("value", 0)))
        else:
            total_orders = await execute_count(db[Collections.INVOICES], {"is_cancelled": False})

        mean_doc = await execute_find_one(inv_summary, {"metric": {"$regex": "Mean", "$options": "i"}})
        if mean_doc:
            aov = round(float(mean_doc.get("value", 0.0)), 2)
        elif total_orders > 0:
            aov = round(total_revenue / total_orders, 2)

        # 3. Lấy total_customers
        total_customers = await execute_count(db[Collections.CUSTOMER_SEGMENTS], {})
        if total_customers == 0:
            total_customers = await execute_count(db[Collections.CUSTOMERS], {})

        return {
            "total_revenue": round(total_revenue, 2),
            "total_orders": total_orders,
            "total_customers": total_customers,
            "average_order_value": aov,
        }

    @staticmethod
    async def get_revenue_trend(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
        """Lấy chuỗi doanh thu theo tháng từ monthly_revenue."""
        cursor = db[Collections.MONTHLY_REVENUE].find({}).sort("year_month", 1)
        docs = await execute_find_list(cursor)
        results = []
        for doc in docs:
            results.append({
                "year_month": doc["year_month"],
                "revenue": round(float(doc.get("net_revenue", doc.get("gross_revenue", 0.0))), 2),
            })
        return results

    @staticmethod
    async def get_top_products(db: AsyncIOMotorDatabase, limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy top sản phẩm doanh thu cao nhất từ product_revenue."""
        cursor = db[Collections.PRODUCT_REVENUE].find({}).sort("total_revenue", -1).limit(limit)
        docs = await execute_find_list(cursor, length=limit)
        results = []
        for doc in docs:
            results.append({
                "stock_code": doc["stock_code"],
                "description": doc.get("description"),
                "total_revenue": round(float(doc.get("total_revenue", 0.0)), 2),
                "total_quantity": int(doc.get("total_quantity", 0)),
                "order_count": int(doc.get("order_count", 0)),
            })
        return results

    @staticmethod
    async def get_top_countries(db: AsyncIOMotorDatabase, limit: int = 10) -> List[Dict[str, Any]]:
        """Lấy top quốc gia đóng góp doanh thu lớn nhất từ country_revenue."""
        cursor = db[Collections.COUNTRY_REVENUE].find({}).sort("total_revenue", -1).limit(limit)
        docs = await execute_find_list(cursor, length=limit)
        results = []
        for doc in docs:
            results.append({
                "country": doc["country"],
                "total_revenue": round(float(doc.get("total_revenue", 0.0)), 2),
                "invoice_count": int(doc.get("invoice_count", 0)),
                "customer_count": int(doc.get("customer_count", 0)),
                "percentage_share": round(float(doc.get("percentage_share", 0.0)), 2),
            })
        return results
