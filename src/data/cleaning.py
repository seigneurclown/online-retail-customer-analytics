"""
src/data/cleaning.py
Mục đích : Làm sạch dữ liệu giao dịch bán lẻ và tạo các biến phái sinh (Derived Variables).
Nguyên tắc:
  - Dữ liệu thô (raw) được giữ nguyên vẹn, không chỉnh sửa file gốc.
  - Mọi quyết định lọc bỏ dòng đều có căn cứ và giải thích lý do rõ ràng (TẠI SAO).
  - Không tự ý xóa dòng thiếu CustomerID ở bước này (giữ lại cho phân tích doanh thu tổng).
  - Kết quả làm sạch được lưu vào thư mục data/processed/.
"""

import sys
from pathlib import Path
import pandas as pd

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi mã hóa ký tự
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Xác định đường dẫn thư mục gốc project (đi lên 2 cấp: src/data/cleaning.py -> project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def clean_retail_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mục đích:
        Làm sạch dữ liệu thô ở cấp độ từng dòng giao dịch và tạo các cột phái sinh.

    Input:
        df (pd.DataFrame): DataFrame dữ liệu gốc chứa 8 cột chuẩn từ load_raw_data().

    Output:
        pd.DataFrame: Bảng dữ liệu đã được làm sạch, gồm các cột gốc kèm 'IsCancelled' và 'Revenue'.

    Logic xử lý & Giải thích TẠI SAO:
        1. Xóa các dòng trùng lặp hoàn toàn (drop_duplicates):
           - TẠI SAO: 5.268 dòng trùng lặp 100% trên cả 8 cột trong cùng thời điểm
             là lỗi hệ thống ghi nhận đúp, không phải khách mua lặp lại hợp lệ.
        2. Tạo biến cờ đơn hủy 'IsCancelled':
           - Quy tắc: InvoiceNo bắt đầu bằng chữ cái "C" (ví dụ: C536379).
           - TẠI SAO: Không xóa ngay các đơn hủy. Việc gắn cờ giúp tách biệt đơn mua
             và đơn hủy, phục vụ bài toán kiểm định thống kê hủy đơn ở Phase 6.
        3. Lọc bỏ các dòng không phải giao dịch thương mại:
           - Điều kiện 1: UnitPrice > 0.
             TẠI SAO: Loại bỏ 2 dòng có giá âm ('Adjust bad debt' - bút toán điều chỉnh kế toán)
             và 2.515 dòng có giá bằng 0 (hàng tặng kèm, mẫu thử hoặc lỗi ghi sổ).
           - Điều kiện 2: Loại bỏ dòng Quantity < 0 mà KHÔNG PHẢI đơn hủy (~IsCancelled).
             TẠI SAO: 1.336 dòng này là điều chỉnh kho hư hỏng, mất mát nội bộ
             (Description thường ghi: 'damaged', 'lost', 'thrown away'), không phải mua bán.
           - Ghi chú về Description: Các dòng thiếu Description đều có UnitPrice = 0,
             nên đã tự động được lọc sạch qua điều kiện UnitPrice > 0.
           - Ghi chú về CustomerID: KHÔNG xóa dòng thiếu CustomerID (~24,9% dữ liệu).
             TẠI SAO: Doanh thu của doanh nghiệp đến từ cả khách vãng lai. Nếu xóa ngay,
             tổng doanh thu sẽ bị mất 1/4. Chỉ lọc CustomerID khi thực hiện RFM (Phase 7).
        4. Tạo biến phái sinh Revenue:
           - Công thức: Revenue = Quantity * UnitPrice.
           - Với đơn hủy (IsCancelled=True), Quantity âm nên Revenue mang giá trị âm,
             phản ánh chính xác giá trị hoàn tiền (refund).
    """
    print("--- Bắt đầu quy trình làm sạch dữ liệu giao dịch ---")
    initial_rows = len(df)
    print(f"Số dòng ban đầu: {initial_rows:,}")

    # Bước 1: Xóa trùng lặp
    df_clean = df.drop_duplicates().copy()
    duplicates_removed = initial_rows - len(df_clean)
    print(f"1. Đã xóa dòng trùng lặp: {duplicates_removed:,} dòng")

    # Bước 2: Tạo biến cờ đơn hủy IsCancelled
    # Chuyển InvoiceNo về str để kiểm tra ký tự bắt đầu
    df_clean["IsCancelled"] = df_clean["InvoiceNo"].astype(str).str.startswith("C", na=False)
    cancelled_count = df_clean["IsCancelled"].sum()
    print(f"2. Gắn cờ IsCancelled: {cancelled_count:,} dòng đơn hủy")

    # Bước 3: Lọc bỏ dòng không hợp lệ
    # - UnitPrice phải > 0
    # - Không lấy dòng Quantity < 0 nếu không phải đơn hủy
    valid_mask = (df_clean["UnitPrice"] > 0) & ~(
        (df_clean["Quantity"] < 0) & (~df_clean["IsCancelled"])
    )
    df_clean = df_clean[valid_mask].copy()
    invalid_removed = (initial_rows - duplicates_removed) - len(df_clean)
    print(f"3. Đã loại bỏ dòng bất thường (giá <= 0, điều chỉnh kho): {invalid_removed:,} dòng")

    # Bước 4: Tạo biến Revenue
    df_clean["Revenue"] = df_clean["Quantity"] * df_clean["UnitPrice"]
    print("4. Đã tạo biến doanh thu: Revenue = Quantity * UnitPrice")

    # Đảm bảo kiểu dữ liệu chuẩn xác
    df_clean["InvoiceDate"] = pd.to_datetime(df_clean["InvoiceDate"])

    print(f"-> Số dòng sau khi làm sạch: {len(df_clean):,} (giữ lại {len(df_clean)/initial_rows*100:.2f}%)")
    return df_clean


def create_invoice_level_data(df_clean: pd.DataFrame) -> pd.DataFrame:
    """
    Mục đích:
        Tổng hợp dữ liệu từ cấp độ dòng sản phẩm lên cấp độ từng hóa đơn (Invoice level).

    Input:
        df_clean (pd.DataFrame): DataFrame đã làm sạch từ hàm clean_retail_data().

    Output:
        pd.DataFrame: Bảng dữ liệu cấp hóa đơn, mỗi dòng đại diện cho một InvoiceNo duy nhất.

    Logic xử lý:
        1. Nhóm theo 'InvoiceNo'.
        2. Tính toán các chỉ số:
           - InvoiceDate: Thời điểm lập hóa đơn (lấy giá trị đầu tiên).
           - CustomerID: Mã khách hàng của hóa đơn đó.
           - Country: Quốc gia phát sinh hóa đơn.
           - IsCancelled: Hóa đơn có phải đơn hủy hay không.
           - InvoiceValue: Tổng giá trị hóa đơn = SUM(Revenue).
             (LƯU Ý: Phân biệt rõ Revenue ở mức dòng và InvoiceValue ở mức hóa đơn).
           - TotalQuantity: Tổng số lượng sản phẩm trong đơn = SUM(Quantity).
           - ItemCount: Số loại mặt hàng khác nhau trong đơn = COUNT(StockCode).
    """
    print("\n--- Bắt đầu tổng hợp dữ liệu cấp độ Hóa đơn (Invoice level) ---")

    invoice_df = (
        df_clean.groupby("InvoiceNo")
        .agg(
            InvoiceDate=("InvoiceDate", "min"),
            CustomerID=("CustomerID", "first"),
            Country=("Country", "first"),
            IsCancelled=("IsCancelled", "first"),
            InvoiceValue=("Revenue", "sum"),
            TotalQuantity=("Quantity", "sum"),
            ItemCount=("StockCode", "count"),
        )
        .reset_index()
    )

    print(f"-> Tổng số hóa đơn duy nhất: {len(invoice_df):,}")
    print(f"   - Hóa đơn mua hàng hợp lệ: {(~invoice_df['IsCancelled']).sum():,}")
    print(f"   - Hóa đơn hủy (cancellation): {invoice_df['IsCancelled'].sum():,}")
    return invoice_df


def save_processed_data(
    df_clean: pd.DataFrame,
    df_invoice: pd.DataFrame,
    output_dir: Path | str = PROCESSED_DIR,
) -> None:
    """
    Mục đích:
        Lưu các DataFrame đã làm sạch sang định dạng file CSV trong data/processed/.

    Input:
        df_clean (pd.DataFrame): Dữ liệu giao dịch đã làm sạch.
        df_invoice (pd.DataFrame): Dữ liệu tổng hợp theo hóa đơn.
        output_dir (Path | str): Thư mục lưu trữ kết quả.

    Output:
        Ghi 2 file CSV vào ổ đĩa:
          - retail_cleaned.csv
          - invoice_data.csv
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    clean_file = output_dir / "retail_cleaned.csv"
    invoice_file = output_dir / "invoice_data.csv"

    print(f"\n--- Đang lưu dữ liệu đã xử lý vào: {output_dir} ---")
    df_clean.to_csv(clean_file, index=False)
    print(f"-> Đã lưu: {clean_file.name} ({clean_file.stat().st_size / (1024*1024):.2f} MB)")

    df_invoice.to_csv(invoice_file, index=False)
    print(f"-> Đã lưu: {invoice_file.name} ({invoice_file.stat().st_size / (1024*1024):.2f} MB)")


def run_cleaning_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Hàm điều phối toàn bộ pipeline của Phase 3:
      Nạp raw data -> Làm sạch -> Tạo invoice data -> Lưu vào data/processed/.
    """
    from src.data.load_data import load_raw_data

    print("Bước 1: Nạp dữ liệu thô...")
    raw_df = load_raw_data()

    print("\nBước 2: Tiến hành làm sạch dữ liệu giao dịch...")
    df_clean = clean_retail_data(raw_df)

    print("\nBước 3: Tạo bảng tổng hợp cấp hóa đơn...")
    df_invoice = create_invoice_level_data(df_clean)

    print("\nBước 4: Lưu dữ liệu ra file processed...")
    save_processed_data(df_clean, df_invoice)

    print("\n=== HOÀN TẤT PIPELINE PHASE 3 THÀNH CÔNG ===")
    return df_clean, df_invoice


if __name__ == "__main__":
    # Chạy trực tiếp từ dòng lệnh: python -m src.data.cleaning
    run_cleaning_pipeline()
