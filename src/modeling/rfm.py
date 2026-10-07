"""
src/modeling/rfm.py
Mục đích : Xây dựng bảng đặc trưng hành vi khách hàng RFM (Recency, Frequency, Monetary)
           ở CẤP ĐỘ KHÁCH HÀNG (Customer Level).
Nguyên tắc cốt lõi:
  - RFM != K-Means: RFM là bảng biểu diễn hành vi, K-Means là thuật toán gom cụm.
  - Tuyệt đối KHÔNG chạy K-Means trực tiếp trên từng dòng giao dịch riêng lẻ (transaction rows),
    mà phải gom theo mã khách hàng (CustomerID).
  - Trước khi tạo RFM, kiểm tra và xử lý triệt để:
      + Thiếu CustomerID (loại bỏ vì không thể gán hành vi cho ai).
      + Đơn hủy (Cancellation): Chỉ tính Frequency trên các đơn mua thành công;
        Monetary tính giá trị ròng sau khi trừ tiền hoàn lại (Net Spend).
      + Khách hàng có Monetary <= 0 (loại bỏ vì không có giá trị chi tiêu thực tế).
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
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"


def build_rfm_table(
    df: pd.DataFrame,
    reference_date: pd.Timestamp | None = None,
) -> pd.DataFrame:
    """
    Mục đích:
        Tổng hợp dữ liệu giao dịch thành ma trận RFM theo từng CustomerID.

    Input:
        df (pd.DataFrame): Bảng retail_cleaned.csv chứa các giao dịch sạch.
        reference_date (pd.Timestamp, optional): Ngày tham chiếu để tính Recency.
            Mặc định là ngày giao dịch muộn nhất trong dữ liệu cộng thêm 1 ngày.

    Output:
        pd.DataFrame: Bảng RFM gồm đúng 4 cột:
          - CustomerID: Mã định danh khách hàng (kiểu số nguyên).
          - Recency: Số ngày kể từ lần mua hàng thành công cuối cùng đến ReferenceDate (ngày).
          - Frequency: Số lượng hóa đơn mua hàng thành công (nunique InvoiceNo).
          - Monetary: Tổng chi tiêu thuần của khách hàng sau khi đã trừ đơn hoàn hủy (£).

    Logic xử lý & Giải thích TẠI SAO:
        1. Lọc bỏ các dòng thiếu CustomerID:
           - TẠI SAO: Không thể phân tích hành vi khách hàng nếu không biết người mua là ai.
        2. Xác định ReferenceDate:
           - Lấy ngày phát sinh giao dịch cuối cùng của dataset + 1 ngày (2011-12-10).
           - TẠI SAO: Tránh trường hợp Recency = 0 ngày đối với khách mua vào ngày cuối cùng.
        3. Tính Recency (R):
           - Lấy ngày mua hàng cuối cùng của các đơn mua hợp lệ (~IsCancelled).
           - R = (ReferenceDate - LastPurchaseDate).days.
           - Ý nghĩa: R càng nhỏ chứng tỏ khách hàng mới mua gần đây (khách còn hoạt động).
        4. Tính Frequency (F):
           - Đếm số hóa đơn duy nhất của các đơn mua hợp lệ (~IsCancelled).
           - F = nunique(InvoiceNo).
           - Ý nghĩa: F càng lớn chứng tỏ khách hàng quay lại mua sắm nhiều lần (trung thành).
        5. Tính Monetary (M):
           - Tổng doanh thu thuần: M = SUM(Revenue) trên toàn bộ giao dịch của khách hàng đó
             (bao gồm cả đơn hủy với Revenue âm để trừ tiền hoàn trả thực tế).
           - Ý nghĩa: M càng lớn thể hiện giá trị đóng góp tiền tệ của khách hàng càng cao.
        6. Lọc bỏ khách hàng có Monetary <= 0:
           - TẠI SAO: Một số ít khách hàng mua hàng trước kỳ quan sát (trước 12/2010)
             nhưng sang năm 2011 mới thực hiện hoàn trả toàn bộ, dẫn đến Monetary âm hoặc bằng 0.
             Những quan sát này không đại diện cho giá trị thương mại dương và sẽ gây lỗi
             khi chuẩn hóa Log-transform/Scaling ở Phase 8 (K-Means).
    """
    print("--- Bắt đầu xây dựng bảng RFM ở Cấp độ Khách hàng (Customer Level) ---")

    # 1. Lọc các dòng có CustomerID
    df_valid = df[df["CustomerID"].notna()].copy()
    df_valid["CustomerID"] = df_valid["CustomerID"].astype(int)
    df_valid["InvoiceDate"] = pd.to_datetime(df_valid["InvoiceDate"])
    print(f"1. Số dòng giao dịch có định danh CustomerID: {len(df_valid):,} dòng")

    # 2. Xác định ReferenceDate
    if reference_date is None:
        reference_date = df_valid["InvoiceDate"].max() + pd.Timedelta(days=1)
    print(f"2. Ngày mốc tham chiếu (Reference Date): {reference_date.strftime('%Y-%m-%d %H:%M:%S')}")

    # Tách dữ liệu đơn mua hàng hợp lệ
    purchases = df_valid[~df_valid["IsCancelled"]]

    # 3. Tính Recency: khoảng cách ngày từ lần mua gần nhất đến reference_date
    recency = (
        purchases.groupby("CustomerID")["InvoiceDate"]
        .max()
        .apply(lambda last_date: (reference_date - last_date).days)
    )

    # 4. Tính Frequency: số hóa đơn mua sắm thành công
    frequency = purchases.groupby("CustomerID")["InvoiceNo"].nunique()

    # 5. Tính Monetary: tổng doanh thu ròng (mua trừ đi hủy)
    monetary = df_valid.groupby("CustomerID")["Revenue"].sum().round(2)

    # 6. Ghép thành bảng RFM hoàn chỉnh
    rfm = pd.DataFrame({
        "CustomerID": recency.index,
        "Recency": recency.values,
        "Frequency": frequency.values,
        "Monetary": monetary.loc[recency.index].values,
    })

    initial_cust_count = len(rfm)
    print(f"3. Tổng số khách hàng ban đầu có phát sinh đơn mua: {initial_cust_count:,}")

    # 7. Lọc bỏ khách hàng có Monetary <= 0
    rfm_cleaned = rfm[rfm["Monetary"] > 0].copy().reset_index(drop=True)
    excluded_count = initial_cust_count - len(rfm_cleaned)
    print(f"4. Đã loại bỏ {excluded_count} khách hàng có tổng chi tiêu Monetary <= 0 (do hoàn trả hết hàng)")
    print(f"-> Số lượng khách hàng hợp lệ đưa vào phân tích RFM: {len(rfm_cleaned):,} khách hàng")

    return rfm_cleaned


def summarize_rfm_distributions(rfm_df: pd.DataFrame) -> pd.DataFrame:
    """
    Mục đích:
        Thống kê mô tả toàn diện về độ biến thiên và độ lệch phân phối của 3 biến R, F, M.

    Input:
        rfm_df (pd.DataFrame): Bảng RFM đã tạo.

    Output:
        pd.DataFrame: Bảng tóm tắt chỉ số thống kê (Count, Mean, Std, Min, 25%, Median, 75%, Max, Skewness).
    """
    desc = rfm_df[["Recency", "Frequency", "Monetary"]].describe().T
    desc["IQR"] = desc["75%"] - desc["25%"]
    desc["Skewness"] = rfm_df[["Recency", "Frequency", "Monetary"]].skew()

    rename_map = {
        "count": "Số lượng (Count)",
        "mean": "Trung bình (Mean)",
        "std": "Độ lệch chuẩn (Std)",
        "min": "Nhỏ nhất (Min)",
        "25%": "Phân vị 25% (Q1)",
        "50%": "Trung vị (Median)",
        "75%": "Phân vị 75% (Q3)",
    }
    desc = desc.rename(columns=rename_map)
    return desc.round(2)


def export_rfm_pipeline() -> pd.DataFrame:
    """
    Hàm điều phối toàn bộ quá trình tính toán RFM và xuất file kết quả:
      retail_cleaned.csv -> build_rfm_table -> rfm_data.csv & rfm_summary.csv.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    clean_file = PROCESSED_DIR / "retail_cleaned.csv"
    print("Đang nạp dữ liệu từ retail_cleaned.csv...")
    df = pd.read_csv(clean_file)

    # Xây dựng bảng RFM
    rfm_df = build_rfm_table(df)

    # Lưu bảng RFM cấp khách hàng
    rfm_output_file = PROCESSED_DIR / "rfm_data.csv"
    rfm_df.to_csv(rfm_output_file, index=False)
    print(f"\n-> Đã lưu bảng RFM chính thức: {rfm_output_file.name} ({len(rfm_df):,} dòng)")

    # Thống kê và lưu bảng phân phối RFM
    summary_df = summarize_rfm_distributions(rfm_df)
    summary_output_file = TABLES_DIR / "rfm_summary.csv"
    summary_df.to_csv(summary_output_file)
    print(f"-> Đã lưu bảng thống kê phân phối: {summary_output_file.name}")

    print("\n--- BẢNG THỐNG KÊ MÔ TẢ PHÂN PHỐI RFM ---")
    print(summary_df)

    print("\n=== HOÀN TẤT XÂY DỰNG BẢNG RFM (PHASE 7) ===")
    return rfm_df


if __name__ == "__main__":
    # Chạy trực tiếp từ dòng lệnh: python -m src.modeling.rfm
    export_rfm_pipeline()
