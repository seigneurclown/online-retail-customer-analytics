"""
Repository truy vấn dữ liệu Khách hàng & RFM từ MongoDB
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

from typing import List, Dict, Any, Optional, Tuple
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import Collections
from app.repositories.base import execute_count, execute_find_one, execute_find_list


class CustomerRepository:
    """Xử lý truy vấn dữ liệu Customer, RFM và Phân cụm Segmentation."""

    @staticmethod
    async def get_customers_paginated(
        db: AsyncIOMotorDatabase,
        page: int = 1,
        page_size: int = 20,
        search: Optional[str] = None,
        cluster: Optional[int] = None,
        membership_tier: Optional[str] = None,
        min_recency: Optional[int] = None,
        max_recency: Optional[int] = None,
        min_frequency: Optional[int] = None,
        max_frequency: Optional[int] = None,
        min_monetary: Optional[float] = None,
        max_monetary: Optional[float] = None,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Lọc và phân trang danh sách khách hàng kết hợp chỉ số RFM và Cụm K-Means."""
        query = {}

        if search:
            query["customer_id"] = {"$regex": search, "$options": "i"}
        if cluster is not None:
            query["cluster"] = cluster
        if membership_tier:
            query["membership_tier"] = {"$regex": membership_tier, "$options": "i"}

        # Lọc theo dải Recency
        rec_filter = {}
        if min_recency is not None:
            rec_filter["$gte"] = min_recency
        if max_recency is not None:
            rec_filter["$lte"] = max_recency
        if rec_filter:
            query["recency"] = rec_filter

        # Lọc theo dải Frequency
        freq_filter = {}
        if min_frequency is not None:
            freq_filter["$gte"] = min_frequency
        if max_frequency is not None:
            freq_filter["$lte"] = max_frequency
        if freq_filter:
            query["frequency"] = freq_filter

        # Lọc theo dải Monetary
        mon_filter = {}
        if min_monetary is not None:
            mon_filter["$gte"] = min_monetary
        if max_monetary is not None:
            mon_filter["$lte"] = max_monetary
        if mon_filter:
            query["monetary"] = mon_filter

        total = await execute_count(db[Collections.CUSTOMER_SEGMENTS], query)

        skip = (page - 1) * page_size
        cursor = db[Collections.CUSTOMER_SEGMENTS].find(query).sort("monetary", -1).skip(skip).limit(page_size)
        docs = await execute_find_list(cursor, length=page_size)

        items = []
        customer_ids = []
        for doc in docs:
            cid = doc["customer_id"]
            customer_ids.append(cid)
            items.append({
                "customer_id": cid,
                "countries": [],
                "recency": doc.get("recency"),
                "frequency": doc.get("frequency"),
                "monetary": round(float(doc.get("monetary", 0.0)), 2),
                "cluster": doc.get("cluster"),
                "membership_tier": doc.get("membership_tier"),
            })

        # Nạp quốc gia tương ứng từ collection customers để hiển thị đầy đủ
        if customer_ids:
            cust_cursor = db[Collections.CUSTOMERS].find({"customer_id": {"$in": customer_ids}})
            cust_docs = await execute_find_list(cust_cursor)
            country_map = {}
            for cdoc in cust_docs:
                country_map[cdoc["customer_id"]] = cdoc.get("countries", [])

            for item in items:
                item["countries"] = country_map.get(item["customer_id"], [])

        return items, total

    @staticmethod
    async def get_customer_by_id(db: AsyncIOMotorDatabase, customer_id: str) -> Optional[Dict[str, Any]]:
        """Lấy thông tin chi tiết một khách hàng cụ thể."""
        clean_cid = str(customer_id).strip()
        doc = await execute_find_one(db[Collections.CUSTOMER_SEGMENTS], {"customer_id": clean_cid})
        if not doc:
            return None

        # Lấy thông tin quốc gia từ collection customers
        cust_doc = await execute_find_one(db[Collections.CUSTOMERS], {"customer_id": clean_cid})
        countries = cust_doc.get("countries", []) if cust_doc else []

        return {
            "customer_id": doc["customer_id"],
            "countries": countries,
            "recency": doc["recency"],
            "frequency": doc["frequency"],
            "monetary": round(float(doc.get("monetary", 0.0)), 2),
            "cluster": doc["cluster"],
            "membership_tier": doc["membership_tier"],
        }
