"""
src/analysis/revenue_analysis.py
Mục đích : Phân tích hoạt động doanh thu (Revenue Analysis) của doanh nghiệp theo:
           1. Thời gian (Time: Month, Year-Month)
           2. Sản phẩm (Product: StockCode, Description)
           3. Quốc gia (Country)
           4. Hóa đơn (Invoice Value distribution)
Nguyên tắc quan trọng:
  - Phân biệt rõ:
      + Revenue: Doanh thu ở cấp độ từng dòng giao dịch.
      + InvoiceValue: Tổng giá trị tiền tệ của một hóa đơn (SUM Revenue).
  - TUYỆT ĐỐI KHÔNG gọi Revenue là Profit (Lợi nhuận), vì dữ liệu không có thông tin chi phí (Cost/COGS).
  - Không suy diễn vô căn cứ (ví dụ: không gán doanh thu tăng do chiến dịch marketing nếu dữ liệu không có).
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi mã hóa ký tự
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"


def analyze_monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mục đích:
        Tổng hợp và phân tích doanh thu theo từng tháng (Year-Month).

    Input:
        df (pd.DataFrame): Bảng dữ liệu giao dịch sạch (retail_cleaned.csv),
                           đã có các cột 'InvoiceDate', 'Revenue', 'IsCancelled', 'InvoiceNo', 'Quantity'.

    Output:
        pd.DataFrame: Bảng tóm tắt theo tháng gồm:
          - YearMonth: Định dạng YYYY-MM
          - GrossRevenue: Doanh thu từ các đơn mua hợp lệ
          - CancelledRevenue: Giá trị hoàn tiền từ các đơn hủy (âm)
          - NetRevenue: Doanh thu thuần thực tế = Gross + Cancelled
          - InvoiceCount: Số lượng hóa đơn phát sinh
          - TotalQuantity: Tổng số lượng sản phẩm bán ra
    """
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["InvoiceDate"]):
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    monthly_summary = (
        df.groupby("YearMonth")
        .apply(
            lambda g: pd.Series({
                "GrossRevenue": g.loc[~g["IsCancelled"], "Revenue"].sum(),
                "CancelledRevenue": g.loc[g["IsCancelled"], "Revenue"].sum(),
                "NetRevenue": g["Revenue"].sum(),
                "InvoiceCount": g["InvoiceNo"].nunique(),
                "TotalQuantity": g["Quantity"].sum(),
            }),
            include_groups=False,
        )
        .reset_index()
    )

    return monthly_summary


def analyze_product_revenue(
    df: pd.DataFrame,
    top_n: int = 10,
    exclude_special_codes: bool = True,
) -> pd.DataFrame:
    """
    Mục đích:
        Phân tích Top N sản phẩm đóng góp doanh thu cao nhất.

    Input:
        df (pd.DataFrame): Dữ liệu giao dịch sạch.
        top_n (int): Số lượng sản phẩm đầu bảng cần trích xuất (mặc định 10).
        exclude_special_codes (bool): Có loại bỏ mã bưu phí/dịch vụ (POST, DOT, M...) không.
                                      TẠI SAO: Những mã này không phải sản phẩm vật lý bán lẻ,
                                      loại bỏ giúp phản ánh chính xác mặt hàng bán chạy.

    Output:
        pd.DataFrame: Bảng xếp hạng Top sản phẩm gồm:
          - StockCode, Description, TotalRevenue, TotalQuantity, OrderCount.
    """
    df_filtered = df[~df["IsCancelled"]].copy()

    if exclude_special_codes:
        # Lọc các mã chỉ gồm chữ cái (như POST, DOT, M, AMAZONFEE, D...)
        is_service_code = df_filtered["StockCode"].astype(str).str.match(r"^[A-Za-z]+$", na=False)
        df_filtered = df_filtered[~is_service_code]

    product_summary = (
        df_filtered.groupby("StockCode")
        .agg(
            Description=("Description", lambda s: s.dropna().iloc[0] if s.notna().any() else "Unknown"),
            TotalRevenue=("Revenue", "sum"),
            TotalQuantity=("Quantity", "sum"),
            OrderCount=("InvoiceNo", "nunique"),
        )
        .reset_index()
        .sort_values(by="TotalRevenue", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return product_summary


def analyze_country_revenue(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Mục đích:
        Phân tích cơ cấu doanh thu theo quốc gia (Country).

    Input:
        df (pd.DataFrame): Dữ liệu giao dịch sạch.
        top_n (int): Số lượng quốc gia hiển thị chi tiết (mặc định 10).

    Output:
        pd.DataFrame: Bảng thống kê doanh thu theo nước, gồm:
          - Country, TotalRevenue, PercentageShare (%), InvoiceCount, CustomerCount.
    """
    country_summary = (
        df.groupby("Country")
        .agg(
            TotalRevenue=("Revenue", "sum"),
            InvoiceCount=("InvoiceNo", "nunique"),
            CustomerCount=("CustomerID", "nunique"),
        )
        .reset_index()
        .sort_values(by="TotalRevenue", ascending=False)
    )

    total_global_rev = country_summary["TotalRevenue"].sum()
    country_summary["PercentageShare"] = (country_summary["TotalRevenue"] / total_global_rev) * 100

    return country_summary.head(top_n).reset_index(drop=True)


def analyze_invoice_value_distribution(invoice_df: pd.DataFrame) -> pd.DataFrame:
    """
    Mục đích:
        Thống kê phân phối giá trị hóa đơn (InvoiceValue) ở mức độ đơn hàng.

    Input:
        invoice_df (pd.DataFrame): Bảng invoice_data.csv chứa thông tin từng hóa đơn.

    Output:
        pd.DataFrame: Bảng chỉ số thống kê mô tả (Mean, Std, Median, IQR, Skewness...).
    """
    # Chỉ xét các hóa đơn mua hàng thông thường (loại trừ hóa đơn hủy đơn thuần)
    normal_invoices = invoice_df[~invoice_df["IsCancelled"]]["InvoiceValue"]

    stats_dict = {
        "Chi số": [
            "Số lượng hóa đơn (Count)",
            "Giá trị trung bình (Mean)",
            "Độ lệch chuẩn (Std)",
            "Giá trị nhỏ nhất (Min)",
            "Phân vị 25% (Q1)",
            "Trung vị (Median / Q2)",
            "Phân vị 75% (Q3)",
            "Khoảng tứ phân vị (IQR)",
            "Giá trị lớn nhất (Max)",
            "Hệ số bất đối xứng (Skewness)",
        ],
        "Giá trị (£)": [
            len(normal_invoices),
            normal_invoices.mean(),
            normal_invoices.std(),
            normal_invoices.min(),
            normal_invoices.quantile(0.25),
            normal_invoices.median(),
            normal_invoices.quantile(0.75),
            normal_invoices.quantile(0.75) - normal_invoices.quantile(0.25),
            normal_invoices.max(),
            normal_invoices.skew(),
        ],
    }

    return pd.DataFrame(stats_dict)


def export_revenue_reports(output_dir: Path | str = TABLES_DIR) -> None:
    """
    Hàm thực thi toàn bộ phân tích doanh thu và lưu các bảng kết quả sang outputs/tables/.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clean_file = PROJECT_ROOT / "data" / "processed" / "retail_cleaned.csv"
    invoice_file = PROJECT_ROOT / "data" / "processed" / "invoice_data.csv"

    print("Đang nạp dữ liệu sạch từ data/processed/...")
    df = pd.read_csv(clean_file)
    inv_df = pd.read_csv(invoice_file)

    print("\n1. Phân tích doanh thu theo tháng...")
    monthly_df = analyze_monthly_revenue(df)
    monthly_df.to_csv(output_dir / "monthly_revenue.csv", index=False)
    print("-> Đã xuất: outputs/tables/monthly_revenue.csv")

    print("\n2. Phân tích Top sản phẩm theo doanh thu...")
    product_df = analyze_product_revenue(df, top_n=10)
    product_df.to_csv(output_dir / "top_products_revenue.csv", index=False)
    print("-> Đã xuất: outputs/tables/top_products_revenue.csv")

    print("\n3. Phân tích doanh thu theo quốc gia...")
    country_df = analyze_country_revenue(df, top_n=10)
    country_df.to_csv(output_dir / "country_revenue.csv", index=False)
    print("-> Đã xuất: outputs/tables/country_revenue.csv")

    print("\n4. Phân tích phân phối giá trị hóa đơn (Invoice Value)...")
    inv_stats_df = analyze_invoice_value_distribution(inv_df)
    inv_stats_df.to_csv(output_dir / "invoice_value_summary.csv", index=False)
    print("-> Đã xuất: outputs/tables/invoice_value_summary.csv")

    print("\n=== HOÀN TẤT BÁO CÁO DOANH THU (PHASE 4) ===")


if __name__ == "__main__":
    # Chạy trực tiếp từ dòng lệnh: python -m src.analysis.revenue_analysis
    export_revenue_reports()
