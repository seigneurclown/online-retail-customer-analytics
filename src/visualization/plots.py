"""
src/visualization/plots.py
Mục đích : Module trực quan hóa dữ liệu (Visualization) bằng Matplotlib & Seaborn.
Bám sát syllabus CHAPTER 3:
  - Line chart (xu hướng theo thời gian)
  - Bar chart / Horizontal bar (xếp hạng danh mục)
  - Histogram & Boxplot (phân phối biến liên tục)
Nguyên tắc trực quan hóa:
  - Mỗi biểu đồ phải trả lời một câu hỏi nghiên cứu cụ thể (Question).
  - Không vẽ biểu đồ chỉ để trang trí.
  - Phải có đầy đủ: Question -> Chart -> Observation -> Insight.
  - Chú thích rõ các điểm giới hạn của dữ liệu (Data Limitations).
"""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend an toàn cho xuất file hàng loạt
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi mã hóa ký tự
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"


def setup_plot_theme() -> None:
    """
    Mục đích:
        Thiết lập giao diện thẩm mỹ chuẩn cho toàn bộ biểu đồ trong dự án.
    """
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 11,
        "axes.labelweight": "semibold",
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })


def plot_monthly_revenue_trend(
    monthly_df: pd.DataFrame,
    save_path: Path | str | None = None,
) -> plt.Figure:
    """
    1. Question:
       Doanh thu thuần (Net Revenue) biến động như thế nào qua từng tháng trong giai đoạn 2010 - 2011?

    2. Chart Type:
       Line Chart kết hợp điểm mốc (Marker) và đường nối.

    3. Observation:
       - Doanh thu dao động ổn định quanh £500k - £700k trong nửa đầu 2011.
       - Tăng trưởng bứt phá từ tháng 9/2011 (>£1.01M) và đạt đỉnh tại tháng 11/2011 (>£1.45M).
       - Tháng 12/2011 giảm mạnh xuống £432k do chỉ thu thập dữ liệu đến ngày 09/12.

    4. Insight:
       Mô hình kinh doanh mang tính chu kỳ mùa vụ rất cao, tập trung dồn vào quý 4
       (mùa lễ hội mua sắm Giáng sinh / Black Friday).
    """
    setup_plot_theme()
    fig, ax = plt.subplots(figsize=(11, 5.5))

    # Chuyển doanh thu sang nghìn bảng (£k) cho dễ đọc
    rev_k = monthly_df["NetRevenue"] / 1000
    months = monthly_df["YearMonth"].astype(str)

    ax.plot(
        months,
        rev_k,
        marker="o",
        markersize=7,
        color="#1f77b4",
        linewidth=2.5,
        label="Doanh thu thuần (Net Revenue)",
    )

    # Đổ bóng nhẹ phía dưới đường line để tăng tính trực quan
    ax.fill_between(months, rev_k, color="#1f77b4", alpha=0.12)

    # Chú thích đỉnh cao nhất (Peak) vào tháng 11/2011
    peak_idx = rev_k.idxmax()
    peak_month = months.iloc[peak_idx]
    peak_val = rev_k.iloc[peak_idx]
    ax.annotate(
        f"Đỉnh doanh thu: £{peak_val:,.0f}k\n(Tháng 11/2011)",
        xy=(peak_idx, peak_val),
        xytext=(peak_idx - 2.2, peak_val + 70),
        arrowprops=dict(facecolor="#d62728", shrink=0.08, width=1.5, headwidth=7),
        fontsize=9.5,
        fontweight="bold",
        color="#d62728",
        bbox=dict(boxstyle="round,pad=0.3", fc="#ffebee", ec="#d62728", lw=1),
    )

    # Chú thích tháng 12/2011 không trọn vẹn
    last_idx = len(months) - 1
    last_val = rev_k.iloc[last_idx]
    ax.annotate(
        f"Chỉ có 9 ngày đầu tháng!\n£{last_val:,.0f}k",
        xy=(last_idx, last_val),
        xytext=(last_idx - 1.8, last_val - 120),
        arrowprops=dict(facecolor="#7f7f7f", shrink=0.08, width=1.2, headwidth=6),
        fontsize=9,
        color="#4f4f4f",
        bbox=dict(boxstyle="round,pad=0.3", fc="#f5f5f5", ec="#9e9e9e", lw=1),
    )

    ax.set_title("Xu hướng Doanh thu thuần theo Tháng (12/2010 – 12/2011)", pad=15)
    ax.set_xlabel("Tháng giao dịch (Year-Month)")
    ax.set_ylabel("Doanh thu thuần (Nghìn bảng Anh - £k)")
    ax.set_ylim(0, rev_k.max() * 1.2)
    plt.xticks(rotation=45)
    ax.legend(loc="upper left")

    if save_path:
        fig.savefig(save_path)
        plt.close(fig)

    return fig


def plot_top_products_revenue(
    product_df: pd.DataFrame,
    save_path: Path | str | None = None,
) -> plt.Figure:
    """
    1. Question:
       Top 10 mặt hàng nào tạo ra doanh thu lớn nhất cho cửa hàng?

    2. Chart Type:
       Horizontal Bar Chart (Biểu đồ thanh ngang) - tối ưu hiển thị tên sản phẩm dài.

    3. Observation:
       - Mặt hàng 'REGENCY CAKESTAND 3 TIER' và 'PAPER CRAFT , LITTLE BIRDIE'
         vượt trội hoàn toàn, đạt xấp xỉ £170k.
       - Tiếp theo là 'WHITE HANGING HEART T-LIGHT HOLDER' và 'PARTY BUNTING'.

    4. Insight:
       Mặt hàng gia dụng, tiệc tùng và quà tặng lưu niệm là trụ cột doanh thu.
    """
    setup_plot_theme()
    fig, ax = plt.subplots(figsize=(11, 6))

    df_sorted = product_df.sort_values(by="TotalRevenue", ascending=True).copy()

    # Rút gọn tên sản phẩm nếu quá dài (>35 ký tự) để hiển thị gọn gàng
    labels = [
        f"{row['StockCode']} - {str(row['Description'])[:32]}..."
        if len(str(row["Description"])) > 35
        else f"{row['StockCode']} - {str(row['Description'])}"
        for _, row in df_sorted.iterrows()
    ]

    bars = ax.barh(
        labels,
        df_sorted["TotalRevenue"] / 1000,
        color="#2ca02c",
        edgecolor="#1b611b",
        alpha=0.85,
        height=0.65,
    )

    # Hiển thị số tiền (£k) ngay phía sau mỗi thanh bar
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 2,
            bar.get_y() + bar.get_height() / 2,
            f"£{width:,.1f}k",
            va="center",
            ha="left",
            fontsize=9,
            fontweight="bold",
            color="#222222",
        )

    ax.set_title("Top 10 Sản phẩm đóng góp Doanh thu cao nhất", pad=15)
    ax.set_xlabel("Tổng doanh thu (Nghìn bảng Anh - £k)")
    ax.set_xlim(0, (df_sorted["TotalRevenue"].max() / 1000) * 1.18)

    if save_path:
        fig.savefig(save_path)
        plt.close(fig)

    return fig


def plot_country_revenue_breakdown(
    country_df: pd.DataFrame,
    save_path: Path | str | None = None,
) -> plt.Figure:
    """
    1. Question:
       Cơ cấu doanh thu theo thị trường địa lý phân bố ra sao?

    2. Chart Type:
       Bar Chart có nhãn tỷ lệ phần trăm (Percentage Share).

    3. Observation:
       - United Kingdom chiếm tỷ trọng áp đảo tuyệt đối: 84.0% tổng doanh thu (£8.19M).
       - Quốc gia thứ 2 là Netherlands chỉ chiếm ~2.9%, Ireland (EIRE) ~2.7%, Đức ~2.3%.

    4. Insight:
       Doanh nghiệp tập trung cao độ vào thị trường nội địa UK. Khi thực hiện
       kiểm định thống kê theo quốc gia ở Phase 6, cần gộp nhóm thị trường nhỏ.
    """
    setup_plot_theme()
    fig, ax = plt.subplots(figsize=(11, 5.5))

    df_top = country_df.head(8).copy()
    colors = ["#1f77b4"] + ["#aec7e8"] * (len(df_top) - 1)

    bars = ax.bar(
        df_top["Country"],
        df_top["TotalRevenue"] / 1000,
        color=colors,
        edgecolor="#333333",
        lw=0.7,
        width=0.6,
    )

    for bar, share in zip(bars, df_top["PercentageShare"]):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 120,
            f"{share:.1f}%\n(£{height:,.0f}k)",
            ha="center",
            va="bottom",
            fontsize=8.5,
            fontweight="bold",
        )

    ax.set_title("Cơ cấu Doanh thu theo Quốc gia (Top 8 thị trường lớn nhất)", pad=15)
    ax.set_xlabel("Quốc gia (Country)")
    ax.set_ylabel("Tổng doanh thu (Nghìn bảng Anh - £k)")
    ax.set_ylim(0, (df_top["TotalRevenue"].max() / 1000) * 1.18)
    plt.xticks(rotation=25)

    if save_path:
        fig.savefig(save_path)
        plt.close(fig)

    return fig


def plot_invoice_value_distribution(
    invoice_df: pd.DataFrame,
    save_path: Path | str | None = None,
) -> plt.Figure:
    """
    1. Question:
       Giá trị từng đơn hàng (Invoice Value) phân phối như thế nào? Có tuân theo phân phối chuẩn không?

    2. Chart Type:
       Histogram kèm đường ước lượng mật độ kernel (KDE) + Boxplot thu nhỏ.

    3. Observation:
       - Đại đa số đơn hàng có giá trị dưới £600 (trung vị là £303.30).
       - Có đuôi dài về bên phải kéo dài đến hơn £100,000 (đơn mua buôn sỉ).

    4. Insight:
       Phân phối giá trị hóa đơn bị lệch phải cực mạnh (Right-Skewed).
       Khi kiểm định thống kê ở Phase 6, cần kiểm tra giả định phân phối chuẩn;
       nếu vi phạm sẽ phải chuyển sang kiểm định phi tham số (Non-parametric test).
    """
    setup_plot_theme()
    normal_invoices = invoice_df[~invoice_df["IsCancelled"]]["InvoiceValue"]

    fig, (ax_box, ax_hist) = plt.subplots(
        2, 1, figsize=(11, 6.5), sharex=True, gridspec_kw={"height_ratios": [0.25, 0.75]}
    )

    # Boxplot ở trên
    sns.boxplot(x=normal_invoices, ax=ax_box, color="#98df8a", fliersize=2.5)
    ax_box.set(xlabel="")
    ax_box.set_title("Phân phối Giá trị Hóa đơn (Invoice Value Distribution)", pad=10)

    # Histogram + KDE ở dưới, giới hạn hiển thị zoom vào vùng £0 - £3,000 (chứa 98% đơn hàng)
    zoom_data = normal_invoices[normal_invoices <= 3000]
    sns.histplot(zoom_data, bins=60, kde=True, ax=ax_hist, color="#2ca02c", alpha=0.6)

    mean_val = normal_invoices.mean()
    median_val = normal_invoices.median()

    ax_hist.axvline(mean_val, color="#d62728", linestyle="--", linewidth=1.8, label=f"Mean: £{mean_val:,.1f}")
    ax_hist.axvline(median_val, color="#1f77b4", linestyle="-", linewidth=2.0, label=f"Median: £{median_val:,.1f}")

    ax_hist.set_xlabel("Giá trị hóa đơn (Bảng Anh - £) [Zoom vùng £0 - £3,000]")
    ax_hist.set_ylabel("Tần số (Số lượng hóa đơn)")
    ax_hist.legend(loc="upper right")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path)
        plt.close(fig)

    return fig


def generate_all_revenue_visualizations() -> None:
    """
    Hàm thực thi vẽ và lưu toàn bộ 4 biểu đồ của Phase 5 vào thư mục outputs/figures/.
    """
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    print("Đang nạp dữ liệu để vẽ biểu đồ...")
    monthly_df = pd.read_csv(TABLES_DIR / "monthly_revenue.csv")
    product_df = pd.read_csv(TABLES_DIR / "top_products_revenue.csv")
    country_df = pd.read_csv(TABLES_DIR / "country_revenue.csv")
    invoice_df = pd.read_csv(PROJECT_ROOT / "data" / "processed" / "invoice_data.csv")

    print("\n1. Đang vẽ: Xu hướng doanh thu theo tháng...")
    plot_monthly_revenue_trend(monthly_df, FIGURES_DIR / "monthly_revenue_trend.png")
    print("-> Đã xuất: outputs/figures/monthly_revenue_trend.png")

    print("\n2. Đang vẽ: Top 10 sản phẩm đóng góp doanh thu...")
    plot_top_products_revenue(product_df, FIGURES_DIR / "top_products_revenue.png")
    print("-> Đã xuất: outputs/figures/top_products_revenue.png")

    print("\n3. Đang vẽ: Cơ cấu doanh thu theo quốc gia...")
    plot_country_revenue_breakdown(country_df, FIGURES_DIR / "country_revenue_breakdown.png")
    print("-> Đã xuất: outputs/figures/country_revenue_breakdown.png")

    print("\n4. Đang vẽ: Phân phối giá trị hóa đơn (Invoice Value)...")
    plot_invoice_value_distribution(invoice_df, FIGURES_DIR / "invoice_value_distribution.png")
    print("-> Đã xuất: outputs/figures/invoice_value_distribution.png")

    print("\n=== HOÀN TẤT XUẤT TOÀN BỘ BIỂU ĐỒ (PHASE 5) ===")


if __name__ == "__main__":
    # Chạy trực tiếp từ dòng lệnh: python -m src.visualization.plots
    generate_all_revenue_visualizations()
