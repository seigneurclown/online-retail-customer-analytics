"""
Base Repository Utilities hỗ trợ truy vấn tương thích bất đồng bộ (Motor) và đồng bộ (MongoMock/PyMongo)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

import inspect
from typing import Any, Dict, List, Optional


async def execute_count(collection: Any, query: Dict[str, Any]) -> int:
    """Đếm số lượng documents trong collection, tương thích cả Motor async và sync mock."""
    result = collection.count_documents(query)
    if inspect.isawaitable(result):
        return await result
    return int(result)


async def execute_find_one(collection: Any, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Tìm một document trong collection, tương thích cả Motor async và sync mock."""
    result = collection.find_one(query)
    if inspect.isawaitable(result):
        return await result
    return result


async def execute_find_list(cursor: Any, length: Optional[int] = None) -> List[Dict[str, Any]]:
    """Chuyển đổi Cursor thành list, tương thích cả Motor AsyncIOMotorCursor (to_list) và sync Cursor."""
    if hasattr(cursor, "to_list") and callable(getattr(cursor, "to_list")):
        return await cursor.to_list(length=length)
    items = list(cursor)
    if length is not None:
        return items[:length]
    return items
