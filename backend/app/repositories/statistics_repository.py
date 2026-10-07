"""
Repository truy vấn dữ liệu Kiểm định thống kê & Thống kê mô tả từ MongoDB
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import Collections
from app.repositories.base import execute_find_list


class StatisticsRepository:
    """Xử lý truy vấn kết quả kiểm định thống kê và thống kê mô tả phân phối hóa đơn."""

    @staticmethod
    async def get_statistical_tests(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
        """Lấy danh sách các phép kiểm định thống kê đã thực hiện trong nghiên cứu."""
        cursor = db[Collections.STATISTICAL_TESTS].find({}).sort("id", 1)
        docs = await execute_find_list(cursor)
        items = []
        for doc in docs:
            items.append({
                "id": int(doc["id"]),
                "research_question": str(doc["research_question"]),
                "test_name": str(doc["test_name"]),
                "reason": str(doc["reason"]),
                "test_statistic": str(doc["test_statistic"]),
                "p_value": float(doc["p_value"]) if doc.get("p_value") is not None else None,
                "significance_level": str(doc["significance_level"]),
                "conclusion": str(doc["conclusion"]),
            })
        return items

    @staticmethod
    async def get_invoice_value_summary(db: AsyncIOMotorDatabase) -> List[Dict[str, Any]]:
        """Lấy bảng thống kê mô tả phân phối giá trị hóa đơn (Count, Mean, Std, Median, IQR, Max...)."""
        cursor = db[Collections.INVOICE_VALUE_SUMMARY].find({})
        docs = await execute_find_list(cursor)
        items = []
        for doc in docs:
            items.append({
                "metric": str(doc["metric"]),
                "value": round(float(doc["value"]), 4),
            })
        return items
