"""
src/modeling/kmeans.py
Mục đích : Thực hiện thuật toán Phân cụm học không giám sát K-Means (Unsupervised Learning)
           trên dữ liệu RFM, bám sát syllabus CHAPTER 5.
Nguyên tắc phương pháp luận:
  1. INPUT: Chỉ sử dụng 3 đặc trưng RFM đã qua tiền xử lý.
     TUYỆT ĐỐI KHÔNG đưa CustomerID vào vì ID chỉ là mã định danh, không có ý nghĩa hình học.
  2. TIỀN XỬ LÝ (TẠI SAO BẮT BUỘC):
     - Log-transform: Nén độ lệch phải cực đoan của Frequency (skewness 12.05) và Monetary (skewness 21.59).
     - StandardScaler: Đưa cả 3 chiều về mean = 0, std = 1 để khoảng cách Euclid không bị chi phối
       bởi chiều có giá trị lớn (Monetary hàng trăm nghìn £).
  3. LỰA CHỌN SỐ CỤM K:
     - Thử nghiệm trên dải K = 2..7.
     - Đánh giá khách quan bằng 2 chỉ số:
         + Inertia (Within-Cluster Sum of Squares - WCSS) -> Elbow Curve.
         + Silhouette Score (Độ phân tách và độ gắn kết của cụm).
     - KHÔNG khẳng định trước K nào là tốt nhất, trình bày kết quả số liệu để lựa chọn.
"""

import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Đảm bảo in tiếng Việt trên console Windows không bị lỗi mã hóa ký tự
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
TABLES_DIR = PROJECT_ROOT / "outputs" / "tables"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"


def preprocess_rfm_for_clustering(
    rfm_df: pd.DataFrame,
) -> tuple[np.ndarray, pd.DataFrame, StandardScaler]:
    """
    Mục đích:
        Chuẩn hóa dữ liệu RFM trước khi đưa vào thuật toán gom cụm K-Means.

    Input:
        rfm_df (pd.DataFrame): Bảng rfm_data.csv gồm 4 cột (CustomerID, Recency, Frequency, Monetary).

    Output:
        tuple gồm:
          - X_scaled (np.ndarray): Mảng 2 chiều chứa 3 đặc trưng đã Log-transform và chuẩn hóa StandardScaler.
          - rfm_log (pd.DataFrame): Bảng RFM sau khi đã áp dụng Log-transform (để tiện tra cứu).
          - scaler (StandardScaler): Đối tượng scaler đã fit với dữ liệu.

    Logic xử lý & Giải thích TẠI SAO:
        1. Bỏ cột CustomerID: Không được dùng ID để gom cụm.
        2. Biến đổi Log-transform: ln(x)
           - TẠI SAO: Ở Phase 7, Skewness của F là 12.05 và M là 21.59.
             Hàm ln(x) kéo đuôi phân phối về dạng gần đối xứng chuẩn (Skewness sau log < 0.8),
             giúp K-Means không bị các khách hàng ngoại lai (outliers) kéo lệch tâm cụm.
        3. Chuẩn hóa StandardScaler: (x - mean) / std
           - TẠI SAO: Recency dao động từ 1-374, Frequency từ 1-209, Monetary từ vài £ đến £280,000.
             K-Means đo lường bằng khoảng cách Euclid. Nếu không scale, chiều Monetary sẽ chiếm 99%
             tỷ trọng khoảng cách, biến R và F thành vô nghĩa.
    """
    print("--- Tiền xử lý dữ liệu RFM trước khi gom cụm ---")

    # Chỉ lấy 3 cột đặc trưng hành vi
    features = ["Recency", "Frequency", "Monetary"]
    X_raw = rfm_df[features].copy()

    # Bước 1: Log-transform
    rfm_log = np.log(X_raw)
    print("1. Độ lệch (Skewness) trước vs sau khi biến đổi Log-transform:")
    for col in features:
        print(f"   - {col:10s}: Trước log = {X_raw[col].skew():6.2f} -> Sau log = {rfm_log[col].skew():6.2f}")

    # Bước 2: Chuẩn hóa StandardScaler
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(rfm_log)
    print("2. Đã chuẩn hóa dữ liệu bằng StandardScaler (Mean=0, Std=1).")

    return X_scaled, rfm_log, scaler


def evaluate_kmeans_clusters(
    X_scaled: np.ndarray,
    k_range: range = range(2, 8),
    random_state: int = 42,
) -> pd.DataFrame:
    """
    Mục đích:
        Chạy thử nghiệm thuật toán K-Means trên dải số cụm K từ 2 đến 7,
        tính toán Inertia và Silhouette Score để đánh giá khách quan.

    Input:
        X_scaled (np.ndarray): Mảng dữ liệu đã chuẩn hóa.
        k_range (range): Dải số cụm cần thử nghiệm (mặc định K = 2..7).
        random_state (int): Hạt giống ngẫu nhiên để đảm bảo tính tái lập (Reproducibility).

    Output:
        pd.DataFrame: Bảng số liệu đánh giá gồm: K, Inertia, Silhouette_Score.
    """
    print(f"\n--- Đang chạy thử nghiệm K-Means trên dải K = {min(k_range)} đến {max(k_range)} ---")
    results = []

    for k in k_range:
        kmeans = KMeans(n_clusters=k, random_state=random_state, n_init=10)
        cluster_labels = kmeans.fit_predict(X_scaled)

        inertia = kmeans.inertia_
        silhouette = silhouette_score(X_scaled, cluster_labels)

        results.append({
            "K": k,
            "Inertia (WCSS)": round(inertia, 2),
            "Silhouette Score": round(silhouette, 4),
        })
        print(f"-> K = {k}: Inertia = {inertia:8.2f} | Silhouette Score = {silhouette:.4f}")

    return pd.DataFrame(results)


def plot_elbow_and_silhouette(
    eval_df: pd.DataFrame,
    save_path: Path | str | None = None,
) -> plt.Figure:
    """
    Mục đích:
        Vẽ đồ thị so sánh kép:
        - Đồ thị 1: Elbow Curve (Đường quán tính Inertia / WCSS).
        - Đồ thị 2: Biểu đồ Silhouette Score theo từng giá trị K.
    """
    sns.set_theme(style="whitegrid")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))

    k_values = eval_df["K"]

    # Đồ thị 1: Elbow Curve
    ax1.plot(
        k_values,
        eval_df["Inertia (WCSS)"],
        marker="o",
        markersize=7,
        color="#1f77b4",
        linewidth=2.2,
    )
    ax1.set_title("Phương pháp Điểm uốn (Elbow Method)", fontsize=12, fontweight="bold", pad=12)
    ax1.set_xlabel("Số lượng cụm (K)", fontweight="semibold")
    ax1.set_ylabel("Inertia (Tổng bình phương khoảng cách nội cụm - WCSS)", fontweight="semibold")
    ax1.set_xticks(k_values)

    # Đánh dấu các điểm uốn tiềm năng tại K=3 và K=4
    ax1.axvline(3, color="#d62728", linestyle="--", alpha=0.7, label="Điểm uốn K=3")
    ax1.axvline(4, color="#2ca02c", linestyle=":", alpha=0.7, label="Điểm uốn K=4")
    ax1.legend(loc="upper right")

    # Đồ thị 2: Silhouette Score
    bars = ax2.bar(
        k_values,
        eval_df["Silhouette Score"],
        color="#2ca02c",
        edgecolor="#1b611b",
        alpha=0.75,
        width=0.55,
    )
    ax2.set_title("Hệ số Silhouette Score theo từng K", fontsize=12, fontweight="bold", pad=12)
    ax2.set_xlabel("Số lượng cụm (K)", fontweight="semibold")
    ax2.set_ylabel("Silhouette Score (Càng gần 1 càng tốt)", fontweight="semibold")
    ax2.set_xticks(k_values)
    ax2.set_ylim(0, max(eval_df["Silhouette Score"]) * 1.25)

    for bar in bars:
        height = bar.get_height()
        ax2.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.012,
            f"{height:.4f}",
            ha="center",
            va="bottom",
            fontsize=9.5,
            fontweight="bold",
        )

    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300)
        plt.close(fig)

    return fig


def fit_kmeans_model(
    rfm_df: pd.DataFrame,
    n_clusters: int = 3,
    random_state: int = 42,
) -> tuple[pd.DataFrame, KMeans, np.ndarray]:
    """
    Mục đích:
        Chạy mô hình K-Means với số cụm K đã được nhóm lựa chọn (K = 3),
        gán nhãn cụm toán học (Cluster) cho từng khách hàng.

    Input:
        rfm_df (pd.DataFrame): Bảng rfm_data.csv gồm 4 cột (CustomerID, Recency, Frequency, Monetary).
        n_clusters (int): Số lượng cụm đã chọn (mặc định K = 3 theo quyết định ở Phase 8).
        random_state (int): Seed cố định để kết quả tái lập 100%.

    Output:
        tuple gồm:
          - rfm_clustered (pd.DataFrame): Bảng RFM có thêm cột 'Cluster'.
          - kmeans (KMeans): Đối tượng mô hình K-Means đã fit.
          - X_scaled (np.ndarray): Mảng đặc trưng đã chuẩn hóa.
    """
    print(f"\n--- Tiến hành gán nhãn phân cụm K-Means với K = {n_clusters} ---")
    X_scaled, _, _ = preprocess_rfm_for_clustering(rfm_df)

    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)

    rfm_clustered = rfm_df.copy()
    rfm_clustered["Cluster"] = cluster_labels
    print(f"-> Đã gán nhãn {n_clusters} cụm thành công cho {len(rfm_clustered):,} khách hàng.")

    return rfm_clustered, kmeans, X_scaled


def run_kmeans_evaluation_pipeline() -> pd.DataFrame:
    """
    Hàm điều phối toàn bộ quá trình thử nghiệm và đánh giá K-Means.
    """
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    rfm_file = PROCESSED_DIR / "rfm_data.csv"
    print("Đang nạp dữ liệu RFM từ data/processed/rfm_data.csv...")
    rfm_df = pd.read_csv(rfm_file)

    # Bước 1: Tiền xử lý dữ liệu
    X_scaled, _, _ = preprocess_rfm_for_clustering(rfm_df)

    # Bước 2: Thử nghiệm dải K = 2..7
    eval_df = evaluate_kmeans_clusters(X_scaled, k_range=range(2, 8))

    # Bước 3: Lưu bảng đánh giá
    output_table = TABLES_DIR / "kmeans_evaluation_metrics.csv"
    eval_df.to_csv(output_table, index=False)
    print(f"\n-> Đã lưu bảng đánh giá chỉ số: {output_table.name}")

    # Bước 4: Vẽ và lưu biểu đồ Elbow & Silhouette
    output_fig = FIGURES_DIR / "kmeans_elbow_silhouette.png"
    plot_elbow_and_silhouette(eval_df, save_path=output_fig)
    print(f"-> Đã lưu biểu đồ trực quan: {output_fig.name}")

    print("\n=== HOÀN TẤT THỬ NGHIỆM VÀ ĐÁNH GIÁ K-MEANS (PHASE 8) ===")
    return eval_df


if __name__ == "__main__":
    # Chạy trực tiếp từ dòng lệnh: python -m src.modeling.kmeans
    run_kmeans_evaluation_pipeline()

