"""
Database Seeding & Ingestion Service
Quản lý nạp dữ liệu mẫu và tải lên dữ liệu trực tiếp từ giao diện Web.
"""

import os
import io
import time
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import pandas as pd
from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings
from app.core.mongodb import Collections, create_mongo_indexes

logger = logging.getLogger("seed_service")

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BACKEND_DIR.parent


def get_data_directories():
    """Xác định đường dẫn dữ liệu với cơ chế fallback thông minh."""
    if (BACKEND_DIR / "data" / "processed").exists():
        data_processed = BACKEND_DIR / "data" / "processed"
    else:
        data_processed = PROJECT_ROOT / "data" / "processed"

    if (BACKEND_DIR / "outputs" / "tables").exists():
        outputs_tables = BACKEND_DIR / "outputs" / "tables"
    else:
        outputs_tables = PROJECT_ROOT / "outputs" / "tables"

    return data_processed, outputs_tables


class SeedService:
    def __init__(self, uri: Optional[str] = None, db_name: Optional[str] = None):
        self.uri = uri or settings.MONGODB_URI
        self.db_name = db_name or settings.MONGODB_DATABASE

    def get_client_and_db(self):
        client = MongoClient(self.uri, serverSelectionTimeoutMS=10000)
        db = client[self.db_name]
        return client, db

    def get_status(self) -> Dict[str, Any]:
        """Lấy trạng thái kết nối và số lượng bản ghi trong từng collection."""
        try:
            client, db = self.get_client_and_db()
            client.admin.command("ping")
            
            data_proc, out_tbl = get_data_directories()
            has_files = (data_proc / "customer_segments.csv").exists() or (data_proc / "invoice_data.csv").exists()

            stats = {
                "connected": True,
                "database_name": self.db_name,
                "has_seed_files": has_files,
                "collections": {
                    "customers": db[Collections.CUSTOMERS].count_documents({}),
                    "invoices": db[Collections.INVOICES].count_documents({}),
                    "customer_rfm": db[Collections.CUSTOMER_RFM].count_documents({}),
                    "customer_segments": db[Collections.CUSTOMER_SEGMENTS].count_documents({}),
                    "monthly_revenue": db[Collections.MONTHLY_REVENUE].count_documents({}),
                    "country_revenue": db[Collections.COUNTRY_REVENUE].count_documents({}),
                    "product_revenue": db[Collections.PRODUCT_REVENUE].count_documents({}),
                    "products": db[Collections.PRODUCTS].count_documents({}),
                    "statistical_tests": db[Collections.STATISTICAL_TESTS].count_documents({}),
                    "kmeans_evaluation": db[Collections.KMEANS_EVALUATION].count_documents({}),
                    "customer_segments_summary": db[Collections.CUSTOMER_SEGMENTS_SUMMARY].count_documents({}),
                    "invoice_value_summary": db[Collections.INVOICE_VALUE_SUMMARY].count_documents({}),
                }
            }
            stats["total_records"] = sum(stats["collections"].values())
            client.close()
            return stats
        except Exception as e:
            return {
                "connected": False,
                "database_name": self.db_name,
                "has_seed_files": False,
                "error": str(e),
                "collections": {},
                "total_records": 0,
            }

    def seed_all(self) -> Dict[str, Any]:
        """Thực thi pipeline nạp toàn bộ dữ liệu mẫu."""
        start_time = time.time()
        client, db = self.get_client_and_db()
        client.admin.command("ping")
        
        data_proc, out_tbl = get_data_directories()
        summary = {}

        # 1. customers & invoices
        inv_path = data_proc / "invoice_data.csv"
        if inv_path.exists():
            inv_df = pd.read_csv(inv_path)
            
            # Seed customers
            cust_col = db[Collections.CUSTOMERS]
            cust_col.drop()
            valid_customers = inv_df[inv_df["CustomerID"].notna()].copy()
            valid_customers["CustomerID"] = valid_customers["CustomerID"].astype(float).astype(int).astype(str)
            cust_docs = []
            for cust_id, countries in valid_customers.groupby("CustomerID")["Country"].unique().items():
                cust_docs.append({
                    "customer_id": str(cust_id),
                    "countries": [str(c).strip() for c in countries],
                })
            if cust_docs:
                cust_col.insert_many(cust_docs)
            summary["customers"] = len(cust_docs)

            # Seed invoices
            inv_col = db[Collections.INVOICES]
            inv_col.drop()
            inv_docs = []
            for _, row in inv_df.iterrows():
                cust_id = str(int(float(row["CustomerID"]))) if pd.notna(row["CustomerID"]) else None
                inv_docs.append({
                    "invoice_no": str(row["InvoiceNo"]).strip(),
                    "invoice_date": str(row["InvoiceDate"]).strip(),
                    "customer_id": cust_id,
                    "country": str(row["Country"]).strip(),
                    "is_cancelled": bool(row["IsCancelled"]),
                    "invoice_value": round(float(row["InvoiceValue"]), 2),
                    "total_quantity": int(row["TotalQuantity"]),
                    "item_count": int(row["ItemCount"]),
                })
            if inv_docs:
                inv_col.insert_many(inv_docs)
            summary["invoices"] = len(inv_docs)

        # 2. customer_rfm
        rfm_path = data_proc / "rfm_data.csv"
        if rfm_path.exists():
            rfm_df = pd.read_csv(rfm_path)
            rfm_col = db[Collections.CUSTOMER_RFM]
            rfm_col.drop()
            docs = []
            for _, row in rfm_df.iterrows():
                docs.append({
                    "customer_id": str(int(float(row["CustomerID"]))),
                    "recency": int(row["Recency"]),
                    "frequency": int(row["Frequency"]),
                    "monetary": round(float(row["Monetary"]), 2),
                })
            if docs:
                rfm_col.insert_many(docs)
            summary["customer_rfm"] = len(docs)

        # 3. customer_segments
        seg_path = data_proc / "customer_segments.csv"
        if seg_path.exists():
            seg_df = pd.read_csv(seg_path)
            seg_col = db[Collections.CUSTOMER_SEGMENTS]
            seg_col.drop()
            docs = []
            for _, row in seg_df.iterrows():
                docs.append({
                    "customer_id": str(int(float(row["CustomerID"]))),
                    "recency": int(row["Recency"]),
                    "frequency": int(row["Frequency"]),
                    "monetary": round(float(row["Monetary"]), 2),
                    "cluster": int(row["Cluster"]),
                    "membership_tier": str(row["MembershipTier"]).strip(),
                })
            if docs:
                seg_col.insert_many(docs)
            summary["customer_segments"] = len(docs)

        # 4. monthly_revenue
        m_path = out_tbl / "monthly_revenue.csv"
        if m_path.exists():
            m_df = pd.read_csv(m_path)
            col = db[Collections.MONTHLY_REVENUE]
            col.drop()
            docs = []
            for _, row in m_df.iterrows():
                docs.append({
                    "year_month": str(row["YearMonth"]).strip(),
                    "total_revenue": round(float(row["TotalRevenue"]), 2),
                    "invoice_count": int(row["InvoiceCount"]),
                    "customer_count": int(row["CustomerCount"]),
                    "aov": round(float(row["AOV"]), 2),
                    "mom_growth_pct": round(float(row["MoM_Growth_Pct"]), 2) if pd.notna(row["MoM_Growth_Pct"]) else None,
                })
            if docs:
                col.insert_many(docs)
            summary["monthly_revenue"] = len(docs)

        # 5. country_revenue
        c_path = out_tbl / "country_revenue.csv"
        if c_path.exists():
            c_df = pd.read_csv(c_path)
            col = db[Collections.COUNTRY_REVENUE]
            col.drop()
            docs = []
            for _, row in c_df.iterrows():
                docs.append({
                    "country": str(row["Country"]).strip(),
                    "total_revenue": round(float(row["TotalRevenue"]), 2),
                    "invoice_count": int(row["InvoiceCount"]),
                    "customer_count": int(row["CustomerCount"]),
                    "revenue_share_pct": round(float(row["RevenueSharePct"]), 2),
                })
            if docs:
                col.insert_many(docs)
            summary["country_revenue"] = len(docs)

        # 6. top_products_revenue
        p_path = out_tbl / "top_products_revenue.csv"
        if p_path.exists():
            p_df = pd.read_csv(p_path)
            col = db[Collections.PRODUCT_REVENUE]
            col.drop()
            docs = []
            for _, row in p_df.iterrows():
                docs.append({
                    "stock_code": str(row["StockCode"]).strip(),
                    "description": str(row["Description"]).strip() if pd.notna(row["Description"]) else None,
                    "total_quantity": int(row["TotalQuantity"]),
                    "total_revenue": round(float(row["TotalRevenue"]), 2),
                    "invoice_count": int(row["InvoiceCount"]),
                })
            if docs:
                col.insert_many(docs)
            summary["product_revenue"] = len(docs)

        # 7. statistical_tests_summary
        st_path = out_tbl / "statistical_tests_summary.csv"
        if st_path.exists():
            st_df = pd.read_csv(st_path)
            col = db[Collections.STATISTICAL_TESTS]
            col.drop()
            docs = []
            for _, row in st_df.iterrows():
                docs.append({
                    "test_name": str(row["TestName"]).strip(),
                    "statistic": round(float(row["Statistic"]), 4),
                    "p_value": float(row["P_Value"]),
                    "conclusion": str(row["Conclusion"]).strip(),
                    "hypothesis": str(row["Hypothesis"]).strip() if "Hypothesis" in row and pd.notna(row["Hypothesis"]) else None,
                })
            if docs:
                col.insert_many(docs)
            summary["statistical_tests"] = len(docs)

        # 8. kmeans_evaluation_metrics
        km_path = out_tbl / "kmeans_evaluation_metrics.csv"
        if km_path.exists():
            km_df = pd.read_csv(km_path)
            col = db[Collections.KMEANS_EVALUATION]
            col.drop()
            docs = []
            for _, row in km_df.iterrows():
                docs.append({
                    "k": int(row["K"]),
                    "inertia": round(float(row["Inertia"]), 2),
                    "silhouette_score": round(float(row["SilhouetteScore"]), 4),
                    "davies_bouldin_index": round(float(row["DaviesBouldinIndex"]), 4),
                })
            if docs:
                col.insert_many(docs)
            summary["kmeans_evaluation"] = len(docs)

        # 9. customer_segments_summary
        css_path = out_tbl / "customer_segments_summary.csv"
        if css_path.exists():
            css_df = pd.read_csv(css_path)
            col = db[Collections.CUSTOMER_SEGMENTS_SUMMARY]
            col.drop()
            docs = []
            for _, row in css_df.iterrows():
                docs.append({
                    "cluster": int(row["Cluster"]),
                    "membership_tier": str(row["MembershipTier"]).strip(),
                    "customer_count": int(row["CustomerCount"]),
                    "percentage": round(float(row["Percentage"]), 2),
                    "avg_recency": round(float(row["AvgRecency"]), 2),
                    "avg_frequency": round(float(row["AvgFrequency"]), 2),
                    "avg_monetary": round(float(row["AvgMonetary"]), 2),
                })
            if docs:
                col.insert_many(docs)
            summary["customer_segments_summary"] = len(docs)

        # 10. invoice_value_summary
        ivs_path = out_tbl / "invoice_value_summary.csv"
        if ivs_path.exists():
            ivs_df = pd.read_csv(ivs_path)
            col = db[Collections.INVOICE_VALUE_SUMMARY]
            col.drop()
            docs = []
            for _, row in ivs_df.iterrows():
                docs.append({
                    "metric": str(row["Metric"]).strip(),
                    "value": round(float(row["Value"]), 2),
                })
            if docs:
                col.insert_many(docs)
            summary["invoice_value_summary"] = len(docs)

        # 11. products
        prod_path = data_proc / "products.csv"
        if not prod_path.exists():
            prod_path = data_proc / "retail_cleaned.csv"

        if prod_path.exists():
            col = db[Collections.PRODUCTS]
            col.drop()
            df = pd.read_csv(prod_path, usecols=["StockCode", "Description"])
            df_unique = df.dropna(subset=["StockCode"]).drop_duplicates(subset=["StockCode"])
            docs = []
            for _, row in df_unique.iterrows():
                docs.append({
                    "stock_code": str(row["StockCode"]).strip(),
                    "description": str(row["Description"]).strip() if pd.notna(row["Description"]) else None,
                })
            if docs:
                col.insert_many(docs)
            summary["products"] = len(docs)

        # Create indexes
        create_mongo_indexes(db)
        client.close()

        duration = round(time.time() - start_time, 2)
        return {
            "status": "success",
            "duration_seconds": duration,
            "summary": summary,
            "total_inserted": sum(summary.values()),
        }

    def ingest_uploaded_csv(self, file_content: bytes, file_name: str, collection_type: str) -> Dict[str, Any]:
        """Xử lý nạp file CSV do người dùng tải lên trực tiếp từ Website."""
        client, db = self.get_client_and_db()
        client.admin.command("ping")
        df = pd.read_csv(io.BytesIO(file_content))
        
        inserted_count = 0
        col_type = collection_type.lower().strip()

        if col_type == "invoices" or "invoice" in file_name.lower():
            col = db[Collections.INVOICES]
            docs = []
            for _, row in df.iterrows():
                cust_id = str(int(float(row["CustomerID"]))) if ("CustomerID" in row and pd.notna(row["CustomerID"])) else None
                docs.append({
                    "invoice_no": str(row.get("InvoiceNo", "")).strip(),
                    "invoice_date": str(row.get("InvoiceDate", "")).strip(),
                    "customer_id": cust_id,
                    "country": str(row.get("Country", "")).strip(),
                    "is_cancelled": bool(row.get("IsCancelled", False)),
                    "invoice_value": round(float(row.get("InvoiceValue", 0)), 2),
                    "total_quantity": int(row.get("TotalQuantity", 0)),
                    "item_count": int(row.get("ItemCount", 0)),
                })
            if docs:
                col.insert_many(docs)
            inserted_count = len(docs)

        elif col_type == "segments" or "segment" in file_name.lower():
            col = db[Collections.CUSTOMER_SEGMENTS]
            docs = []
            for _, row in df.iterrows():
                docs.append({
                    "customer_id": str(int(float(row["CustomerID"]))),
                    "recency": int(row.get("Recency", 0)),
                    "frequency": int(row.get("Frequency", 0)),
                    "monetary": round(float(row.get("Monetary", 0)), 2),
                    "cluster": int(row.get("Cluster", 0)),
                    "membership_tier": str(row.get("MembershipTier", "")).strip(),
                })
            if docs:
                col.insert_many(docs)
            inserted_count = len(docs)

        else:
            # Generic ingestion
            target_col_name = col_type if col_type else "uploaded_data"
            col = db[target_col_name]
            records = df.to_dict(orient="records")
            if records:
                col.insert_many(records)
            inserted_count = len(records)

        client.close()
        return {
            "status": "success",
            "file_name": file_name,
            "collection": col_type,
            "inserted_count": inserted_count,
        }
