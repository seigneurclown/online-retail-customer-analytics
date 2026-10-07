"""
Script thực thi xuất báo cáo kinh doanh sang định dạng Excel và PDF
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)

Cách chạy:
    python export_reports.py
"""

import sys
from pathlib import Path

# Đảm bảo UTF-8 cho Windows Terminal
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Thêm đường dẫn thư mục gốc vào sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.export import export_all_reports

if __name__ == "__main__":
    export_all_reports()
