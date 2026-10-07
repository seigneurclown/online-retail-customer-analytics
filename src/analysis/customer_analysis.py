"""
src/analysis/customer_analysis.py
Mục đích : Phân tích hồ sơ khách hàng theo cụm K-Means (Cluster Profiling)
           và ánh xạ sang hệ thống Hạng thẻ Hội viên (Membership Loyalty Tiers)
           bám sát yêu cầu bài toán kinh doanh bán lẻ.

Nguyên tắc phương pháp luận cốt lõi:
  1. PHÂN BIỆT RÕ RÀNG:
     - "K-Means tạo Cluster": Thuật toán thuần túy phân nhóm hình học trong không gian
       3 chiều đã chuẩn hóa (Cluster 0, 1, 2).
     - "Nhà phân tích dữ liệu diễn giải": Con người đọc hiểu ý nghĩa các chỉ số R, F, M
       thực tế để đặt tên phân khúc và đề xuất chiến lược tiếp thị.
  2. KHÔNG ĐẶT TÊN TÙY TIỆN:
     - Phải tính toán đầy đủ Mean và Median của cả 3 biến Recency, Frequency, Monetary.
     - Phải tính tỷ lệ phần trăm số lượng khách hàng và tỷ trọng đóng góp doanh thu (% Revenue Share).
  3. HỆ THỐNG HẠNG THẺ HỘI VIÊN (Ánh xạ từ K=3 cụm):
     - Hạng Chuẩn / Không Thẻ (Standard / No Card): Recency cao (đã lâu không mua),
       Frequency thấp (1-2 đơn), Monetary thấp -> Khách hàng vãng lai, nguy cơ rời bỏ.
     - Hạng Bạc (Silver Tier): Recency vừa phải, Frequency trung bình, Monetary khá
       -> Khách hàng đang hoạt động, có tiềm năng chi tiêu thêm.
     - Hạng Vàng - Kim Cương (Gold / Diamond Tier): Recency rất thấp (vừa mua gần đây),
       Frequency cao vượt trội, Monetary đóng góp doanh thu lớn nhất -> Khách hàng VIP nòng cốt.
"""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi font ký tự
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"

from src.modeling.kmeans import fit_kmeans_model


def compute_cluster_profiles(rfm_clustered: pd.DataFrame) -> pd.DataFrame:
    """
    Mục đích:
        Tổng hợp các chỉ số thống kê mô tả (Mean, Median, Sum, Count, Share)
        cho từng cụm toán học K-Means tạo ra.

    Input:
        rfm_clustered (pd.DataFrame): Bảng RFM có thêm cột 'Cluster' (0, 1, 2).

    Output:
        pd.DataFrame: Bảng hồ sơ các cụm với đầy đủ các thước đo định lượng.

    Logic xử lý & Giải thích TẠI SAO:
        - Tính cả Mean lẫn Median: Vì phân phối tiền tệ (Monetary) bị lệch phải,
          Median phản ánh mức độ chi tiêu điển hình của số đông trong cụm,
          còn Mean cho biết giá trị trung bình chịu ảnh hưởng bởi tổng quy mô.
        - Tính % Khách hàng và % Doanh thu: Để kiểm chứng quy luật Pareto 80/20 trong kinh doanh.
    """
    total_customers = len(rfm_clustered)
    total_revenue = rfm_clustered["Monetary"].sum()

    # Nhóm theo cụm và tính toán tổng hợp
    profile = (
        rfm_clustered.groupby("Cluster")
        .agg(
            CustomerCount=("CustomerID", "count"),
            Recency_Mean=("Recency", "mean"),
            Recency_Median=("Recency", "median"),
            Frequency_Mean=("Frequency", "mean"),
            Frequency_Median=("Frequency", "median"),
            Monetary_Mean=("Monetary", "mean"),
            Monetary_Median=("Monetary", "median"),
            TotalMonetary=("Monetary", "sum"),
        )
        .reset_index()
    )

    # Tính tỷ lệ % quy mô và % đóng góp doanh thu
    profile["Customer_Pct"] = (profile["CustomerCount"] / total_customers * 100).round(2)
    profile["Revenue_Share_Pct"] = (profile["TotalMonetary"] / total_revenue * 100).round(2)

    return profile


def map_membership_tiers(
    rfm_clustered: pd.DataFrame,
    cluster_profile: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Mục đích:
        Ánh xạ nhãn cụm toán học (Cluster 0, 1, 2) sang Hạng thẻ Hội viên (Membership Tiers)
        dựa trên mức độ chi tiêu (Monetary) và tần suất (Frequency) thực tế.

    Input:
        rfm_clustered (pd.DataFrame): Bảng dữ liệu khách hàng có nhãn Cluster.
        cluster_profile (pd.DataFrame): Bảng số liệu thống kê hồ sơ cụm.

    Output:
        tuple gồm:
          - rfm_segmented (pd.DataFrame): Bảng dữ liệu khách hàng có thêm cột 'MembershipTier'.
          - tier_summary (pd.DataFrame): Bảng tổng hợp số liệu theo từng Hạng thẻ.

    Quy tắc ánh xạ tự động (Tránh giả định thứ tự nhãn của thuật toán):
        - Sắp xếp các cụm theo Monetary_Mean tăng dần:
          + Cụm chi tiêu thấp nhất, Recency cao nhất -> "Không Thẻ / Hạng Chuẩn (Standard)"
          + Cụm chi tiêu trung bình                 -> "Thẻ Bạc (Silver)"
          + Cụm chi tiêu cao nhất, Recency thấp nhất -> "Thẻ Vàng - Kim Cương (Gold / Diamond)"
    """
    # Sắp xếp theo giá trị chi tiêu trung bình để định danh bậc thẻ khách quan
    sorted_profile = cluster_profile.sort_values(by="Monetary_Mean").reset_index(drop=True)

    tier_names = [
        "Không Thẻ / Hạng Chuẩn",
        "Thẻ Bạc (Silver)",
        "Thẻ Vàng - Kim Cương (Gold)",
    ]

    tier_mapping = {}
    for rank_idx, cluster_id in enumerate(sorted_profile["Cluster"]):
        tier_mapping[cluster_id] = tier_names[rank_idx]

    # Gán nhãn hạng thẻ vào từng khách hàng
    rfm_segmented = rfm_clustered.copy()
    rfm_segmented["MembershipTier"] = rfm_segmented["Cluster"].map(tier_mapping)

    # Cập nhật nhãn hạng thẻ vào bảng hồ sơ tóm tắt
    tier_summary = cluster_profile.copy()
    tier_summary["MembershipTier"] = tier_summary["Cluster"].map(tier_mapping)

    # Đưa cột MembershipTier lên đầu để người đọc dễ theo dõi
    cols = ["MembershipTier", "Cluster", "CustomerCount", "Customer_Pct",
            "Recency_Mean", "Recency_Median",
            "Frequency_Mean", "Frequency_Median",
            "Monetary_Mean", "Monetary_Median",
            "TotalMonetary", "Revenue_Share_Pct"]
    tier_summary = tier_summary[cols].sort_values(by="Monetary_Mean", ascending=False).reset_index(drop=True)

    return rfm_segmented, tier_summary


def plot_customer_segments_profile(
    tier_summary: pd.DataFrame,
    save_path: Path | str | None = None,
) -> plt.Figure:
    """
    Mục đích:
        Vẽ biểu đồ so sánh đa chiều giữa các Hạng thẻ hội viên:
        - Đồ thị 1 (Bên trái): So sánh cơ cấu % Số lượng khách vs % Đóng góp doanh thu.
        - Đồ thị 2 (Bên phải): Giá trị chi tiêu trung bình (£) theo từng hạng thẻ.
    """
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.8))

    tiers = tier_summary["MembershipTier"].tolist()
    colors = ["#ffd700", "#c0c0c0", "#cd7f32"]  # Màu vàng gold, bạc silver, đồng/chuẩn

    # Đồ thị 1: So sánh tỷ lệ khách hàng vs Tỷ lệ doanh thu (Pareto effect)
    x = np.arange(len(tiers))
    width = 0.35

    bars1 = ax1.bar(x - width/2, tier_summary["Customer_Pct"], width, label="% Khách hàng", color="#4a90e2", alpha=0.85)
    bars2 = ax1.bar(x + width/2, tier_summary["Revenue_Share_Pct"], width, label="% Đóng góp doanh thu", color="#50e3c2", alpha=0.85)

    ax1.set_title("Cơ cấu Khách hàng vs Đóng góp Doanh thu (%)", fontsize=12, fontweight="bold", pad=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(tiers, fontsize=9.5, fontweight="semibold")
    ax1.set_ylabel("Tỷ lệ phần trăm (%)", fontweight="semibold")
    ax1.legend(loc="upper right")

    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 1.0, f"{h:.1f}%", ha="center", va="bottom", fontsize=8.5)
    for bar in bars2:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 1.0, f"{h:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    # Đồ thị 2: Chi tiêu trung bình (£ Monetary Mean)
    bars_rev = ax2.bar(tiers, tier_summary["Monetary_Mean"], color=["#d4af37", "#a8a8a8", "#a0522d"], width=0.55, edgecolor="#333333")
    ax2.set_title("Chi tiêu Trung bình mỗi Khách hàng (£)", fontsize=12, fontweight="bold", pad=12)
    ax2.set_ylabel("Giá trị chi tiêu trung bình (£)", fontweight="semibold")
    ax2.set_xticks(range(len(tiers)))
    ax2.set_xticklabels(tiers, fontsize=9.5, fontweight="semibold")

    for bar in bars_rev:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 150, f"£{h:,.0f}", ha="center", va="bottom", fontsize=9.5, fontweight="bold")

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300)
        plt.close(fig)

    return fig


def run_customer_profiling_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Hàm điều phối toàn bộ luồng công việc của PHASE 9:
      rfm_data.csv -> K-Means (K=3) -> Cluster Profiling -> Membership Tiers Mapping -> Lưu bảng & Biểu đồ.
    """
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    rfm_file = PROCESSED_DIR / "rfm_data.csv"
    print("Đang nạp dữ liệu từ data/processed/rfm_data.csv...")
    rfm_df = pd.read_csv(rfm_file)

    # Bước 1: Huấn luyện K-Means với K = 3 đã lựa chọn
    rfm_clustered, _, _ = fit_kmeans_model(rfm_df, n_clusters=3, random_state=42)

    # Bước 2: Tổng hợp hồ sơ định lượng của các cụm
    cluster_profile = compute_cluster_profiles(rfm_clustered)

    # Bước 3: Ánh xạ cụm toán học sang Hạng thẻ hội viên (Business Loyalty Tiers)
    rfm_segmented, tier_summary = map_membership_tiers(rfm_clustered, cluster_profile)

    # Bước 4: Lưu bảng phân khúc khách hàng chi tiết
    segments_output_file = PROCESSED_DIR / "customer_segments.csv"
    rfm_segmented.to_csv(segments_output_file, index=False)
    print(f"\n-> Đã lưu bảng phân khúc khách hàng: {segments_output_file.name} ({len(rfm_segmented):,} dòng)")

    # Bước 5: Lưu bảng tóm tắt chỉ số hồ sơ hạng thẻ
    summary_output_file = TABLES_DIR / "customer_segments_summary.csv"
    tier_summary.to_csv(summary_output_file, index=False)
    print(f"-> Đã lưu bảng thống kê hồ sơ phân khúc: {summary_output_file.name}")

    # Bước 6: Vẽ và lưu biểu đồ trực quan hồ sơ phân khúc
    fig_output_file = FIGURES_DIR / "customer_segments_profile.png"
    plot_customer_segments_profile(tier_summary, save_path=fig_output_file)
    print(f"-> Đã xuất biểu đồ trực quan hồ sơ phân khúc: {fig_output_file.name}")

    print("\n--- BẢNG HỒ SƠ PHÂN KHÚC KHÁCH HÀNG (MEMBERSHIP TIERS SUMMARY) ---")
    print(tier_summary.to_string(index=False))

    print("\n=== HOÀN TẤT PHÂN TÍCH HỒ SƠ KHÁCH HÀNG (PHASE 9) ===")
    return rfm_segmented, tier_summary


if __name__ == "__main__":
    # Chạy trực tiếp từ dòng lệnh: python -m src.analysis.customer_analysis
    run_customer_profiling_pipeline()
