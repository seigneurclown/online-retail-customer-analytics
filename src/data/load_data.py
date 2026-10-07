"""
load_data.py
Mục đích: đọc file dữ liệu GỐC (Excel) vào pandas DataFrame.
Nguyên tắc: file này CHỈ ĐỌC, không sửa, không ghi đè data/raw/.
"""

import sys
from pathlib import Path

import pandas as pd

# Đảm bảo in tiếng Việt trên Windows console không bị lỗi mã hóa ký tự
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thư mục gốc của project = đi lên 2 cấp từ file này (src/data/load_data.py -> project)
# Dùng đường dẫn tính từ vị trí file để chạy được từ notebook lẫn terminal.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "Online Retail.xlsx"

# Các cột mong đợi theo mô tả dataset
EXPECTED_COLUMNS = [
    "InvoiceNo", "StockCode", "Description", "Quantity",
    "InvoiceDate", "UnitPrice", "CustomerID", "Country",
]


def load_raw_data(path=RAW_FILE) -> pd.DataFrame:
    """
    Mục đích : Đọc dữ liệu gốc từ file Excel.
    Input    : path - đường dẫn tới file .xlsx (mặc định là data/raw/Online Retail.xlsx)
    Output   : DataFrame chứa dữ liệu gốc, chưa xử lý gì.
    Logic    :
      1. Kiểm tra file có tồn tại không (báo lỗi rõ ràng nếu thiếu).
      2. Đọc bằng pd.read_excel, ép InvoiceNo và StockCode về kiểu chuỗi.
      3. Kiểm tra đủ 8 cột mong đợi.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy file dữ liệu: {path}")

    # TẠI SAO ép về str?
    # InvoiceNo có dạng số (536365) lẫn chữ ("C536379" = đơn hủy).
    # StockCode có dạng số (71053) lẫn chữ ("85123A").
    # Nếu để pandas tự đoán, một cột sẽ bị lẫn kiểu int/str, gây lỗi khi lọc
    # bằng .str.startswith("C") ở bước cleaning.
    df = pd.read_excel(path, dtype={"InvoiceNo": str, "StockCode": str})

    missing_cols = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise ValueError(f"File thiếu các cột: {missing_cols}")

    return df


if __name__ == "__main__":
    # Chạy trực tiếp file này để kiểm tra nhanh: python -m src.data.load_data
    data = load_raw_data()
    print("Shape :", data.shape)
    print("\nDtypes:\n", data.dtypes)
    print("\n5 dòng đầu:\n", data.head())
