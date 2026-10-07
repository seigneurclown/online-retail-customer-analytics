"""
Database Seeding Script (Data Ingestion cho MongoDB NoSQL)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
Đề tài: Phân tích dữ liệu doanh thu và Phân cụm hành vi khách hàng trong lĩnh vực bán lẻ

Mục tiêu:
Đọc dữ liệu từ data/processed/ và outputs/tables/, kiểm tra tính hợp lệ của schema,
và nạp dữ liệu một cách an toàn (idempotent) vào MongoDB.
"""

import os
import sys
import time
import logging
import argparse
from pathlib import Path
from typing import Optional, Any
import pandas as pd
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError

# Đảm bảo đường dẫn import app.* hoạt động từ thư mục backend
CURRENT_DIR = Path(__file__).resolve().parent
BACKEND_DIR = CURRENT_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.config import settings
from app.core.mongodb import Collections, create_mongo_indexes

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("seed_database")

# Đường dẫn dữ liệu từ gốc dự án
PROJECT_ROOT = BACKEND_DIR.parent
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
OUTPUTS_TABLES = PROJECT_ROOT / "outputs" / "tables"


def check_file_exists(file_path: Path) -> bool:
    """Kiểm tra sự tồn tại của file dữ liệu nguồn."""
    if not file_path.exists():
        logger.error(f"Không tìm thấy file nguồn: {file_path}")
        return False
    return True


def seed_customers(db: Database, invoice_df: pd.DataFrame) -> int:
    """
    Nạp dữ liệu vào collection 'customers'.
    Trích xuất danh sách khách hàng duy nhất và các quốc gia họ phát sinh giao dịch.
    """
    logger.info("Đang nạp collection 'customers'...")
    collection = db[Collections.CUSTOMERS]
    collection.drop()

    # Lọc khách hàng có CustomerID hợp lệ
    valid_customers = invoice_df[invoice_df["CustomerID"].notna()].copy()
    valid_customers["CustomerID"] = valid_customers["CustomerID"].astype(float).astype(int).astype(str)

    customer_docs = []
    grouped = valid_customers.groupby("CustomerID")["Country"].unique()

    for customer_id, countries in grouped.items():
        customer_docs.append({
            "customer_id": str(customer_id),
            "countries": [str(c).strip() for c in countries],
        })

    if customer_docs:
        collection.insert_many(customer_docs)
    logger.info(f"-> Hoàn tất 'customers': {len(customer_docs)} bản ghi.")
    return len(customer_docs)


def seed_invoices(db: Database, invoice_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'invoices'."""
    logger.info("Đang nạp collection 'invoices'...")
    collection = db[Collections.INVOICES]
    collection.drop()

    docs = []
    for _, row in invoice_df.iterrows():
        cust_id = str(int(float(row["CustomerID"]))) if pd.notna(row["CustomerID"]) else None
        docs.append({
            "invoice_no": str(row["InvoiceNo"]).strip(),
            "invoice_date": str(row["InvoiceDate"]).strip(),
            "customer_id": cust_id,
            "country": str(row["Country"]).strip(),
            "is_cancelled": bool(row["IsCancelled"]),
            "invoice_value": round(float(row["InvoiceValue"]), 2),
            "total_quantity": int(row["TotalQuantity"]),
            "item_count": int(row["ItemCount"]),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'invoices': {len(docs)} bản ghi.")
    return len(docs)


def seed_customer_rfm(db: Database, rfm_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'customer_rfm'."""
    logger.info("Đang nạp collection 'customer_rfm'...")
    collection = db[Collections.CUSTOMER_RFM]
    collection.drop()

    docs = []
    for _, row in rfm_df.iterrows():
        docs.append({
            "customer_id": str(int(float(row["CustomerID"]))),
            "recency": int(row["Recency"]),
            "frequency": int(row["Frequency"]),
            "monetary": round(float(row["Monetary"]), 2),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'customer_rfm': {len(docs)} bản ghi.")
    return len(docs)


def seed_customer_segments(db: Database, segments_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'customer_segments'."""
    logger.info("Đang nạp collection 'customer_segments'...")
    collection = db[Collections.CUSTOMER_SEGMENTS]
    collection.drop()

    docs = []
    for _, row in segments_df.iterrows():
        docs.append({
            "customer_id": str(int(float(row["CustomerID"]))),
            "recency": int(row["Recency"]),
            "frequency": int(row["Frequency"]),
            "monetary": round(float(row["Monetary"]), 2),
            "cluster": int(row["Cluster"]),
            "membership_tier": str(row["MembershipTier"]).strip(),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'customer_segments': {len(docs)} bản ghi.")
    return len(docs)


def seed_monthly_revenue(db: Database, monthly_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'monthly_revenue'."""
    logger.info("Đang nạp collection 'monthly_revenue'...")
    collection = db[Collections.MONTHLY_REVENUE]
    collection.drop()

    docs = []
    for _, row in monthly_df.iterrows():
        docs.append({
            "year_month": str(row["YearMonth"]).strip(),
            "gross_revenue": round(float(row["GrossRevenue"]), 2),
            "cancelled_revenue": round(float(row["CancelledRevenue"]), 2),
            "net_revenue": round(float(row["NetRevenue"]), 2),
            "invoice_count": int(row["InvoiceCount"]),
            "total_quantity": int(row["TotalQuantity"]),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'monthly_revenue': {len(docs)} bản ghi.")
    return len(docs)


def seed_country_revenue(db: Database, country_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'country_revenue'."""
    logger.info("Đang nạp collection 'country_revenue'...")
    collection = db[Collections.COUNTRY_REVENUE]
    collection.drop()

    docs = []
    for _, row in country_df.iterrows():
        docs.append({
            "country": str(row["Country"]).strip(),
            "total_revenue": round(float(row["TotalRevenue"]), 2),
            "invoice_count": int(row["InvoiceCount"]),
            "customer_count": int(row["CustomerCount"]),
            "percentage_share": round(float(row["PercentageShare"]), 4),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'country_revenue': {len(docs)} bản ghi.")
    return len(docs)


def seed_product_revenue(db: Database, products_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'product_revenue'."""
    logger.info("Đang nạp collection 'product_revenue'...")
    collection = db[Collections.PRODUCT_REVENUE]
    collection.drop()

    docs = []
    for _, row in products_df.iterrows():
        docs.append({
            "stock_code": str(row["StockCode"]).strip(),
            "description": str(row["Description"]).strip() if pd.notna(row["Description"]) else None,
            "total_revenue": round(float(row["TotalRevenue"]), 2),
            "total_quantity": int(row["TotalQuantity"]),
            "order_count": int(row["OrderCount"]),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'product_revenue': {len(docs)} bản ghi.")
    return len(docs)


def seed_statistical_tests(db: Database, stats_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'statistical_tests'."""
    logger.info("Đang nạp collection 'statistical_tests'...")
    collection = db[Collections.STATISTICAL_TESTS]
    collection.drop()

    docs = []
    for idx, row in stats_df.iterrows():
        if pd.isna(row.get("Câu hỏi nghiên cứu")):
            continue
        p_val = float(row["p-value"]) if pd.notna(row["p-value"]) else None
        docs.append({
            "id": idx + 1,
            "research_question": str(row["Câu hỏi nghiên cứu"]).strip(),
            "test_name": str(row["Kiểm định sử dụng"]).strip(),
            "reason": str(row["Lý do chọn test"]).strip(),
            "test_statistic": str(row["Thống kê kiểm định"]).strip(),
            "p_value": p_val,
            "significance_level": str(row["Mức ý nghĩa"]).strip(),
            "conclusion": str(row["Kết luận"]).strip(),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'statistical_tests': {len(docs)} bản ghi.")
    return len(docs)


def seed_kmeans_evaluation(db: Database, kmeans_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'kmeans_evaluation'."""
    logger.info("Đang nạp collection 'kmeans_evaluation'...")
    collection = db[Collections.KMEANS_EVALUATION]
    collection.drop()

    docs = []
    for _, row in kmeans_df.iterrows():
        docs.append({
            "k": int(row["K"]),
            "inertia": round(float(row["Inertia (WCSS)"]), 2),
            "silhouette_score": round(float(row["Silhouette Score"]), 4),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'kmeans_evaluation': {len(docs)} bản ghi.")
    return len(docs)


def seed_customer_segments_summary(db: Database, seg_summary_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'customer_segments_summary'."""
    logger.info("Đang nạp collection 'customer_segments_summary'...")
    collection = db[Collections.CUSTOMER_SEGMENTS_SUMMARY]
    collection.drop()

    docs = []
    for _, row in seg_summary_df.iterrows():
        if pd.isna(row.get("Cluster")):
            continue
        docs.append({
            "membership_tier": str(row["MembershipTier"]).strip(),
            "cluster": int(row["Cluster"]),
            "customer_count": int(row["CustomerCount"]),
            "customer_pct": round(float(row["Customer_Pct"]), 2),
            "recency_mean": round(float(row["Recency_Mean"]), 2),
            "recency_median": round(float(row["Recency_Median"]), 2),
            "frequency_mean": round(float(row["Frequency_Mean"]), 2),
            "frequency_median": round(float(row["Frequency_Median"]), 2),
            "monetary_mean": round(float(row["Monetary_Mean"]), 2),
            "monetary_median": round(float(row["Monetary_Median"]), 2),
            "total_monetary": round(float(row["TotalMonetary"]), 2),
            "revenue_share_pct": round(float(row["Revenue_Share_Pct"]), 2),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'customer_segments_summary': {len(docs)} bản ghi.")
    return len(docs)


def seed_invoice_value_summary(db: Database, invoice_summary_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'invoice_value_summary'."""
    logger.info("Đang nạp collection 'invoice_value_summary'...")
    collection = db[Collections.INVOICE_VALUE_SUMMARY]
    collection.drop()

    docs = []
    for _, row in invoice_summary_df.iterrows():
        if pd.isna(row.get("Chi số")):
            continue
        docs.append({
            "metric": str(row["Chi số"]).strip(),
            "value": round(float(row["Giá trị (£)"]), 4),
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'invoice_value_summary': {len(docs)} bản ghi.")
    return len(docs)


def seed_products(db: Database, retail_cleaned_df: pd.DataFrame) -> int:
    """Nạp dữ liệu vào collection 'products' (danh mục sản phẩm duy nhất)."""
    logger.info("Đang trích xuất và nạp collection 'products'...")
    collection = db[Collections.PRODUCTS]
    collection.drop()

    # Lấy các cặp StockCode và Description duy nhất
    products_unique = retail_cleaned_df.dropna(subset=["StockCode"]).drop_duplicates(subset=["StockCode"])
    docs = []
    for _, row in products_unique.iterrows():
        docs.append({
            "stock_code": str(row["StockCode"]).strip(),
            "description": str(row["Description"]).strip() if pd.notna(row["Description"]) else None,
        })

    if docs:
        collection.insert_many(docs)
    logger.info(f"-> Hoàn tất 'products': {len(docs)} sản phẩm duy nhất.")
    return len(docs)


def run_seed_pipeline(db: Database, skip_heavy_items: bool = False) -> dict:
    """
    Hàm thực thi pipeline nạp dữ liệu toàn diện.
    Hỗ trợ cả môi trường production MongoDB và mock testing.
    """
    start_time = time.time()
    summary = {}

    # 1. invoice_data.csv -> customers & invoices
    invoice_path = DATA_PROCESSED / "invoice_data.csv"
    if check_file_exists(invoice_path):
        invoice_df = pd.read_csv(invoice_path)
        summary["customers"] = seed_customers(db, invoice_df)
        summary["invoices"] = seed_invoices(db, invoice_df)

    # 2. rfm_data.csv -> customer_rfm
    rfm_path = DATA_PROCESSED / "rfm_data.csv"
    if check_file_exists(rfm_path):
        rfm_df = pd.read_csv(rfm_path)
        summary["customer_rfm"] = seed_customer_rfm(db, rfm_df)

    # 3. customer_segments.csv -> customer_segments
    segments_path = DATA_PROCESSED / "customer_segments.csv"
    if check_file_exists(segments_path):
        segments_df = pd.read_csv(segments_path)
        summary["customer_segments"] = seed_customer_segments(db, segments_df)

    # 4. monthly_revenue.csv -> monthly_revenue
    monthly_path = OUTPUTS_TABLES / "monthly_revenue.csv"
    if check_file_exists(monthly_path):
        monthly_df = pd.read_csv(monthly_path)
        summary["monthly_revenue"] = seed_monthly_revenue(db, monthly_df)

    # 5. country_revenue.csv -> country_revenue
    country_path = OUTPUTS_TABLES / "country_revenue.csv"
    if check_file_exists(country_path):
        country_df = pd.read_csv(country_path)
        summary["country_revenue"] = seed_country_revenue(db, country_df)

    # 6. top_products_revenue.csv -> product_revenue
    top_prod_path = OUTPUTS_TABLES / "top_products_revenue.csv"
    if check_file_exists(top_prod_path):
        top_prod_df = pd.read_csv(top_prod_path)
        summary["product_revenue"] = seed_product_revenue(db, top_prod_df)

    # 7. statistical_tests_summary.csv -> statistical_tests
    stats_path = OUTPUTS_TABLES / "statistical_tests_summary.csv"
    if check_file_exists(stats_path):
        stats_df = pd.read_csv(stats_path)
        summary["statistical_tests"] = seed_statistical_tests(db, stats_df)

    # 8. kmeans_evaluation_metrics.csv -> kmeans_evaluation
    kmeans_path = OUTPUTS_TABLES / "kmeans_evaluation_metrics.csv"
    if check_file_exists(kmeans_path):
        kmeans_df = pd.read_csv(kmeans_path)
        summary["kmeans_evaluation"] = seed_kmeans_evaluation(db, kmeans_df)

    # 9. customer_segments_summary.csv -> customer_segments_summary
    seg_summary_path = OUTPUTS_TABLES / "customer_segments_summary.csv"
    if check_file_exists(seg_summary_path):
        seg_summary_df = pd.read_csv(seg_summary_path)
        summary["customer_segments_summary"] = seed_customer_segments_summary(db, seg_summary_df)

    # 10. invoice_value_summary.csv -> invoice_value_summary
    invoice_val_path = OUTPUTS_TABLES / "invoice_value_summary.csv"
    if check_file_exists(invoice_val_path):
        invoice_val_df = pd.read_csv(invoice_val_path)
        summary["invoice_value_summary"] = seed_invoice_value_summary(db, invoice_val_df)

    # 11. retail_cleaned.csv -> products (danh mục chuẩn)
    retail_path = DATA_PROCESSED / "retail_cleaned.csv"
    if check_file_exists(retail_path):
        # Đọc 2 cột cần thiết để tối ưu bộ nhớ
        retail_df = pd.read_csv(retail_path, usecols=["StockCode", "Description"])
        summary["products"] = seed_products(db, retail_df)

    # Tạo Indexes
    create_mongo_indexes(db)

    duration = round(time.time() - start_time, 2)
    logger.info(f"=== ĐÃ HOÀN TẤT SEED DATABASE TRONG {duration} GIÂY ===")
    return summary


def main():
    """Hàm chạy từ terminal command-line interface."""
    parser = argparse.ArgumentParser(description="Seed Database Script cho Online Retail Analytics")
    parser.add_argument("--uri", default=settings.MONGODB_URI, help="MongoDB Connection URI")
    parser.add_argument("--db", default=settings.MONGODB_DATABASE, help="Target Database Name")
    parser.add_argument("--mock", action="store_true", help="Chạy seed với in-memory mongomock để kiểm thử")
    args = parser.parse_args()

    if args.mock:
        import mongomock
        logger.info(f"Đang chạy Seed Pipeline với in-memory MongoMock Database: '{args.db}'...")
        client = mongomock.MongoClient()
        db = client[args.db]
        summary = run_seed_pipeline(db)
        logger.info(f"Kết quả Mock Ingestion: {summary}")
        return

    logger.info(f"Kết nối tới MongoDB tại: {args.uri} | Database: {args.db}")
    try:
        client = MongoClient(args.uri, serverSelectionTimeoutMS=10000)
        # Ping kiểm tra kết nối
        client.admin.command("ping")
        logger.info("Kết nối MongoDB thành công. Bắt đầu nạp dữ liệu...")
        db = client[args.db]
        summary = run_seed_pipeline(db)
        logger.info("Chi tiết số lượng bản ghi đã nạp:")
        for coll, count in summary.items():
            logger.info(f"  - {coll}: {count} documents")
    except ServerSelectionTimeoutError:
        logger.warning(
            "\n[CẢNH BÁO] Không thể kết nối tới MongoDB tại " + args.uri + "!\n"
            "Server MongoDB có thể chưa được bật trên máy local.\n"
            "Gợi ý giải pháp:\n"
            "  1. Khởi động MongoDB service trên máy: 'net start MongoDB' (Windows)\n"
            "  2. Hoặc khởi động Docker MongoDB: 'docker compose up -d mongodb'\n"
            "  3. Để kiểm thử pipeline mà không cần MongoDB server, chạy: 'python scripts/seed_database.py --mock'\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
