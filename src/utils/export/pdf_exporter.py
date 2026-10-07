"""
Module xuất báo cáo nghiên cứu sang định dạng PDF (.pdf) chuẩn in ấn A4
Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

# Đường dẫn mặc định trong project
DEFAULT_ROOT = Path(__file__).resolve().parents[3]
REPORTS_DIR = DEFAULT_ROOT / "outputs" / "reports"
REPORT_MD_PATH = DEFAULT_ROOT / "report" / "technical_report.md"


def get_edge_path() -> Optional[Path]:
    """Tìm đường dẫn tới file thực thi Microsoft Edge trên hệ điều hành Windows."""
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "Edge" / "Application" / "msedge.exe",
    ]
    for p in candidates:
        if p.is_file():
            return p
    system_edge = shutil.which("msedge")
    if system_edge:
        return Path(system_edge)
    return None


def export_pdf_report(
    markdown_path: Optional[Path] = None,
    output_file: Optional[Path] = None
) -> Path:
    """
    Chuyển đổi báo cáo Markdown kỹ thuật sang file PDF ấn tượng, chuẩn học thuật
    sử dụng công cụ Microsoft Edge Headless tích hợp sẵn trên hệ điều hành Windows.
    """
    import markdown

    if markdown_path is None:
        markdown_path = REPORT_MD_PATH
    markdown_path = Path(markdown_path)

    if not markdown_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file markdown báo cáo tại: {markdown_path}")

    if output_file is None:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        output_file = REPORTS_DIR / "Technical_Report.pdf"
    else:
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

    edge_bin = get_edge_path()
    if not edge_bin:
        raise RuntimeError("Không tìm thấy Microsoft Edge trên hệ thống để thực hiện in PDF.")

    # Đọc nội dung Markdown
    md_content = markdown_path.read_text(encoding="utf-8")

    # Chuyển Markdown sang HTML với các phần mở rộng tables, fenced_code
    html_body = markdown.markdown(
        md_content,
        extensions=["extra", "tables", "fenced_code", "nl2br"]
    )

    # CSS Chuyên nghiệp tối ưu cho In Ấn A4
    html_document = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo Cáo Kỹ Thuật - Online Retail Data Analysis</title>
<style>
    @page {{
        size: A4 portrait;
        margin: 18mm 15mm 20mm 15mm;
        @bottom-right {{
            content: "Trang " counter(page);
        }}
    }}
    
    * {{
        box-sizing: border-box;
    }}
    
    body {{
        font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
        color: #1F2937;
        line-height: 1.6;
        font-size: 13px;
        background-color: #FFFFFF;
        margin: 0;
        padding: 0;
    }}
    
    /* Headings */
    h1 {{
        color: #1F4E79;
        font-size: 24px;
        font-weight: 700;
        border-bottom: 2px solid #1F4E79;
        padding-bottom: 8px;
        margin-top: 24px;
        margin-bottom: 16px;
        page-break-after: avoid;
    }}
    
    h2 {{
        color: #1E3A8A;
        font-size: 18px;
        font-weight: 700;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 6px;
        margin-top: 22px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }}
    
    h3 {{
        color: #374151;
        font-size: 15px;
        font-weight: 600;
        margin-top: 16px;
        margin-bottom: 8px;
        page-break-after: avoid;
    }}
    
    p, li {{
        margin-bottom: 6px;
        text-align: justify;
    }}
    
    /* Blockquotes / Callout Boxes */
    blockquote {{
        margin: 12px 0;
        padding: 10px 16px;
        background-color: #F8FAFC;
        border-left: 4px solid #1F4E79;
        color: #334155;
        border-radius: 0 4px 4px 0;
        page-break-inside: avoid;
    }}
    
    blockquote p {{
        margin: 4px 0;
    }}
    
    /* Tables */
    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 14px 0;
        font-size: 11.5px;
        page-break-inside: avoid;
    }}
    
    th, td {{
        padding: 7px 10px;
        border: 1px solid #D1D5DB;
        vertical-align: middle;
    }}
    
    th {{
        background-color: #1F4E79;
        color: #FFFFFF;
        font-weight: 600;
        text-align: center;
    }}
    
    tr:nth-child(even) {{
        background-color: #F9FAFB;
    }}
    
    tr:hover {{
        background-color: #F3F4F6;
    }}
    
    /* Code and ASCII diagrams */
    pre {{
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 6px;
        padding: 12px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 11px;
        line-height: 1.4;
        overflow-x: auto;
        page-break-inside: avoid;
    }}
    
    code {{
        background-color: #F1F5F9;
        color: #0F172A;
        padding: 2px 4px;
        border-radius: 4px;
        font-family: 'Consolas', 'Courier New', monospace;
        font-size: 12px;
    }}
    
    /* Links */
    a {{
        color: #2563EB;
        text-decoration: none;
    }}
    
    /* Horizontal rule */
    hr {{
        border: 0;
        height: 1px;
        background: #E5E7EB;
        margin: 20px 0;
    }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

    temp_html_path = REPORTS_DIR / "_temp_report_render.html"
    temp_html_path.write_text(html_document, encoding="utf-8")

    try:
        cmd = [
            str(edge_bin),
            "--headless",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_file.resolve()}",
            f"file:///{temp_html_path.resolve()}",
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        if not output_file.exists() or output_file.stat().st_size == 0:
            raise RuntimeError(f"Edge tạo PDF thất bại. Chi tiết: {res.stderr}")

        print(f"[PDF EXPORT] Đã xuất thành công file PDF báo cáo: {output_file} ({output_file.stat().st_size / 1024:.1f} KB)")
        return output_file
    finally:
        if temp_html_path.exists():
            try:
                temp_html_path.unlink()
            except Exception:
                pass
