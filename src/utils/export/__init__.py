"""
Gói công cụ xuất báo cáo định dạng cao cấp (Excel & PDF)
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

import sys
from pathlib import Path
from typing import Dict, Optional

# Đảm bảo UTF-8 cho Windows Terminal
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .excel_exporter import export_excel_report
from .pdf_exporter import export_pdf_report

DEFAULT_ROOT = Path(__file__).resolve().parents[3]
REPORTS_DIR = DEFAULT_ROOT / "outputs" / "reports"


def export_all_reports(reports_dir: Optional[Path] = None) -> Dict[str, Path]:
    """
    Thực hiện xuất cả file Excel (.xlsx) và PDF (.pdf) đồng thời vào thư mục outputs/reports.
    """
    if reports_dir is None:
        reports_dir = REPORTS_DIR
    reports_dir = Path(reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)

    excel_file = reports_dir / "Online_Retail_Analysis_Report.xlsx"
    pdf_file = reports_dir / "Technical_Report.pdf"

    print("=" * 60)
    print("BẮT ĐẦU XUẤT TOÀN BỘ BÁO CÁO (EXCEL & PDF)")
    print("=" * 60)

    out_excel = export_excel_report(excel_file)
    out_pdf = export_pdf_report(output_file=pdf_file)

    print("=" * 60)
    print("XUẤT BÁO CÁO HOÀN TẤT THÀNH CÔNG!")
    print(f"1. Excel Report : {out_excel}")
    print(f"2. PDF Report   : {out_pdf}")
    print("=" * 60)

    return {
        "excel": out_excel,
        "pdf": out_pdf,
    }


__all__ = [
    "export_excel_report",
    "export_pdf_report",
    "export_all_reports",
]
