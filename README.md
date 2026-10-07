# Phân Tích Dữ Liệu Doanh Thu & Phân Cụm Khách Hàng (Online Retail)

> **Học phần:** DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012) – Sem1/2026-2027  
> **Bộ dữ liệu:** [Online Retail Dataset – UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/352/online+retail) (~541.909 giao dịch)  
> **Ngôn ngữ & Thư viện:** Python 3.10+ | Pandas | Scikit-Learn | SciPy | Matplotlib | Seaborn | Jupyter  

---

## 📑 Mục Lục

1. [Tổng Quan Dự Án](#-tổng-quan-dự-án)
2. [Kết Quả Then Chốt](#-kết-quả-then-chốt)
3. [Phân Khúc Hạng Thẻ Hội Viên](#-phân-khúc-hạng-thẻ-hội-viên)
4. [Cấu Trúc Thư Mục](#-cấu-trúc-thư-mục)
5. [Quy Trình Xử Lý & Mô Hình Hóa](#-quy-trình-xử-lý--mô-hình-hóa)
6. [Hướng Dẫn Cài Đặt & Chạy](#-hướng-dẫn-cài-đặt--chạy)
7. [Khuyến Nghị Chiến Lược](#-khuyến-nghị-chiến-lược)
8. [Tài Liệu Chi Tiết](#-tài-liệu-chi-tiết)

---

## 📌 Tổng Quan Dự Án

Dự án nghiên cứu chuyên sâu về hành vi mua sắm và cơ cấu doanh thu của một doanh nghiệp bán lẻ trực tuyến tại Vương quốc Anh trong giai đoạn 12/2010 – 12/2011.

Áp dụng quy trình Khoa học Dữ liệu chuẩn mực (**CRISP-DM**), dự án giải quyết bài toán kinh doanh thực tế:
- **Tối ưu hóa doanh thu:** Khám phá chu kỳ mùa vụ, cấu trúc sản phẩm và độ tập trung thị trường.
- **Kiểm định giả thuyết:** Chứng minh sự khác biệt chi tiêu (Weekday vs. Weekend) và bất thường tỷ lệ hủy đơn giữa các quốc gia.
- **Cá nhân hóa tiếp thị:** Kết hợp mô hình định lượng **RFM** với thuật toán học máy **K-Means**, ánh xạ thành **Hệ thống Hạng thẻ Hội viên (Membership Tiers)** có tính thực thi cao.

---

## 🌟 Kết Quả Then Chốt

```
      TỔNG DOANH THU THUẦN                   SỐ ĐƠN HÀNG THÀNH CÔNG                 KHÁCH HÀNG ĐỊNH DANH
         £8.291.748,56                               19.960                                4.339
```

| Lĩnh vực phân tích | Kết quả cốt lõi | Ý nghĩa kinh doanh |
| :--- | :--- | :--- |
| **Quy mô dữ liệu** | 392.732 dòng sạch có mã khách hàng định danh | Đảm bảo tính tin cậy tuyệt đối cho mô hình RFM |
| **Hiệu ứng mùa vụ** | Tháng 11/2011 đạt đỉnh **£1,456 triệu** (+43% MoM) | Mùa mua sắm Black Friday & Giáng sinh bùng nổ |
| **Thị trường chính** | Vương quốc Anh chiếm **84,01%** doanh thu | Thị trường nội địa giữ vai trò sống còn |
| **Hành vi theo ngày** | Mann-Whitney U test: $p = 2,47 \times 10^{-9}$ | Đơn hàng Weekday cao hơn Weekend do tệp khách B2B |
| **Rủi ro hủy đơn** | Chi-Square test: $p = 9,47 \times 10^{-8}$ | **Đức có tỷ lệ hủy 24,20%** (cao gấp 1,75 lần UK) |
| **Mô hình phân cụm** | K-Means với $K=3$ (Silhouette Score: **0,34**) | Phân tách ranh giới rõ ràng, dễ ứng dụng vận hành |

---

## 👑 Phân Khúc Hạng Thẻ Hội Viên

Mô hình phân cụm K-Means chia 4.339 khách hàng thành 3 phân khúc tương ứng với 3 Hạng thẻ:

| Hạng Thẻ Hội Viên | Mã Cụm | Số Khách | Tỷ Lệ Khách | Recency TB | Frequency TB | Monetary TB | Tổng Doanh Thu (£) | Tỷ Trọng DT |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🥇 **Thẻ Vàng - Kim Cương** | `Cluster 2` | 781 | 18,09% | 13 ngày | 13,0 đơn | £7.129,01 | £5.567.756,47 | **67,15%** |
| 🥈 **Thẻ Bạc (Silver)** | `Cluster 0` | 1.701 | 39,40% | 54 ngày | 3,5 đơn | £1.244,26 | £2.116.488,32 | **25,53%** |
| 🥉 **Không Thẻ / Chuẩn** | `Cluster 1` | 1.835 | 42,51% | 162 ngày | 1,3 đơn | £331,06 | £607.503,77 | **7,33%** |

```
TỶ TRỌNG DOANH THU THEO HẠNG THẺ:
█████████████████████████████████████████████ 67,15% (Thẻ Vàng - Kim Cương)
█████████████████ 25,53% (Thẻ Bạc)
█████ 7,33% (Không Thẻ / Chuẩn)
```

---

## 📁 Cấu Trúc Thư Mục

```
online-retail-data-analysis/
├── data/
│   ├── raw/                           # Dữ liệu gốc (Online Retail.xlsx)
│   └── processed/                     # Dữ liệu sạch sau tiền xử lý
│       ├── retail_cleaned.csv         # Bảng giao dịch sạch (530k dòng)
│       ├── invoice_data.csv           # Dữ liệu cấp độ hóa đơn (19.960 dòng)
│       ├── rfm_data.csv               # Bảng chỉ số RFM (4.339 dòng)
│       └── customer_segments.csv      # Bảng phân cụm & hạng thẻ khách hàng
│
├── notebooks/                         # 7 Jupyter Notebooks thực nghiệm
│   ├── 01_data_exploration.ipynb      # Khám phá cấu trúc, khuyết thiếu, dị biệt
│   ├── 02_data_cleaning.ipynb         # Pipeline làm sạch, tách đơn hủy
│   ├── 03_revenue_analysis.ipynb      # Doanh thu theo tháng, sản phẩm, quốc gia
│   ├── 04_statistical_analysis.ipynb  # Kiểm định Mann-Whitney U & Chi-Square
│   ├── 05_rfm_analysis.ipynb          # Tính toán phân phối Recency, Frequency, Monetary
│   ├── 06_kmeans_clustering.ipynb     # Log-scale, Elbow, Silhouette, K-Means
│   └── 07_final_integration.ipynb     # Tích hợp toàn diện & Báo cáo quản trị
│
├── src/                               # Thư viện hàm tái sử dụng chuẩn hóa
│   ├── data/                          # Đọc dữ liệu (load_data.py) & làm sạch (cleaning.py)
│   ├── analysis/                      # Doanh thu, kiểm định thống kê, phân tích chân dung
│   ├── modeling/                      # Trích xuất RFM & Thuật toán K-Means
│   ├── visualization/                 # Hàm vẽ biểu đồ chuyên nghiệp (300 DPI)
│   └── utils/                         # Công cụ tiện ích hệ thống
│       └── export/                    # Xuất báo cáo đa trang Excel (.xlsx) & PDF (.pdf)
│           ├── excel_exporter.py      # Xây dựng bảng tính Excel chuẩn Dashboard
│           └── pdf_exporter.py        # Biên dịch báo cáo PDF chuẩn in ấn A4
│
├── outputs/                           # Sản phẩm đầu ra
│   ├── figures/                       # 6 Biểu đồ phân tích chuẩn báo cáo
│   ├── tables/                        # 8 Bảng dữ liệu thống kê tổng hợp (CSV)
│   └── reports/                       # Báo cáo trích xuất định dạng cao cấp
│       ├── Online_Retail_Analysis_Report.xlsx  # Báo cáo Excel đa trang chuẩn Dashboard
│       └── Technical_Report.pdf                # Báo cáo PDF hoàn chỉnh chuẩn học thuật
│
├── report/
│   └── technical_report.md            # Báo cáo kỹ thuật chi tiết toàn diện
│
├── export_reports.py                  # Script 1-chạm xuất file Excel & PDF
├── requirements.txt                   # Danh sách thư viện phụ thuộc
└── README.md                          # Tài liệu tổng quan dự án
```

---

## 🔄 Quy Trình Xử Lý & Mô Hình Hóa

```
DỮ LIỆU THÔ (541k dòng)
         │
         ▼
[1] TIỀN XỬ LÝ & LÀM SẠCH
     - Loại bỏ 5.268 dòng trùng lặp
     - Tách cờ IsCancelled cho đơn hoàn trả
     - Lọc mã phi hàng hóa (POST, D, BANK CHARGES)
         │
         ├─────────────────────────────────────────┐
         ▼                                         ▼
[2] PHÂN TÍCH DOANH THU & THỐNG KÊ        [3] MÔ HÌNH HÓA RFM
     - Xu hướng doanh thu theo tháng           - R: Số ngày kể từ đơn gần nhất
     - Phân phối giá trị đơn hàng              - F: Số đơn hàng thành công
     - Mann-Whitney U Test (Weekday/Weekend)   - M: Tổng chi tiêu (£)
     - Chi-Square Test (Tỷ lệ hủy đơn)             │
                                                   ▼
                                          [4] PHÂN CỤM K-MEANS
                                               - Biến đổi Log-transform
                                               - Chuẩn hóa StandardScaler
                                               - Tối ưu K=3 (Silhouette: 0,34)
                                                   │
                                                   ▼
                                          [5] HẠNG THẺ HỘI VIÊN & CHIẾN LƯỢC
                                               - Thẻ Vàng - Kim Cương (67% DT)
                                               - Thẻ Bạc (25% DT)
                                               - Không Thẻ / Hạng Chuẩn (7% DT)
```

---

## ⚡ Hướng Dẫn Cài Đặt & Chạy

### Bước 1: Chuẩn bị môi trường
Yêu cầu hệ điều hành đã cài đặt **Python 3.10+**.

```bash
# Di chuyển vào thư mục dự án
cd d:/online-retail-data-analysis

# Tạo và kích hoạt môi trường ảo
python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS / Linux

# Cài đặt toàn bộ thư viện
pip install -r requirements.txt
```

### Bước 2: Chạy toàn bộ hệ thống
Bạn có thể lựa chọn 1 trong 2 cách:

#### Cách A: Chạy qua Jupyter Notebook (Khuyến nghị)
Mở file [`notebooks/07_final_integration.ipynb`](file:///d:/online-retail-data-analysis/notebooks/07_final_integration.ipynb) để xem từng bước trực quan kèm bảng biểu và đồ thị.

#### Cách B: Chạy tự động qua Command Line
Chạy chuỗi lệnh sau để cập nhật toàn bộ dữ liệu từ đầu đến cuối:

```bash
python -c "from src.data.cleaning import run_cleaning_pipeline; run_cleaning_pipeline()"
python -c "from src.analysis.revenue_analysis import run_revenue_analysis_pipeline; run_revenue_analysis_pipeline()"
python -c "from src.analysis.statistics import run_statistical_analysis_pipeline; run_statistical_analysis_pipeline()"
python -c "from src.modeling.rfm import run_rfm_pipeline; run_rfm_pipeline()"
python -c "from src.modeling.kmeans import run_kmeans_pipeline; run_kmeans_pipeline()"
python -c "from src.analysis.customer_analysis import run_customer_profiling_pipeline; run_customer_profiling_pipeline()"
```

### Bước 3: Xuất Báo Cáo Định Dạng Excel & PDF (1-Chạm)
Để tự động trích xuất toàn bộ bảng số liệu sang file Excel đa trang và biên dịch Báo cáo Kỹ thuật sang file PDF cao cấp:

```bash
pip install -r requirements.txt
```

*Các file đầu ra sẽ được lưu trữ tự động tại thư mục:* [`outputs/reports/`](file:///d:/online-retail-data-analysis/outputs/reports/)
- 📗 **File Excel:** `outputs/reports/Online_Retail_Analysis_Report.xlsx` (8 sheets phân tích được định dạng chuẩn Dashboard)
- 📕 **File PDF:** `outputs/reports/Technical_Report.pdf` (Báo cáo nghiên cứu học thuật đầy đủ, căn lề A4 in ấn chuẩn mực)

---

## 🎯 Khuyến Nghị Chiến Lược

### 1. Hạng Thẻ Vàng - Kim Cương (781 khách – Bảo vệ 67% doanh thu)
- **Quản lý khách hàng trọng điểm:** Phân bổ nhân sự chăm sóc riêng (1-on-1 account manager).
- **Ưu tiên chuỗi cung ứng:** Ưu tiên giữ tồn kho các mặt hàng chủ lực (*Regency Cakestand 3 Tier*) vào mùa cao điểm Q4.
- **Chính sách ưu đãi:** Hợp đồng chiết khấu bậc thang theo sản lượng và miễn phí vận chuyển hỏa tốc.

### 2. Hạng Thẻ Bạc (1.701 khách – Bứt phá lên Vàng)
- **Tích điểm nâng hạng:** Thông báo chi tiêu còn thiếu để thăng hạng thẻ Vàng kèm đặc quyền hấp dẫn.
- **Rút ngắn chu kỳ mua sắm:** Thiết lập chuỗi email tự động sau 30-45 ngày kèm mã ưu đãi giới hạn trong 7 ngày để giảm Recency từ 54 ngày xuống dưới 30 ngày.
- **Gợi ý bán kèm (Cross-sell):** Đề xuất phụ kiện và sản phẩm liên quan khi đặt hàng.

### 3. Hạng Chuẩn / Không Thẻ (1.835 khách – Tối ưu chi phí)
- **Tiếp thị tiết kiệm:** Dừng các kênh tiếp thị tốn kém (SMS/Direct mail), chỉ dùng email tự động dịp lễ lớn (Black Friday).
- **Sàng lọc định kỳ:** Đưa vào diện đóng băng dữ liệu tiếp thị nếu không tương tác sau 360 ngày để tiết kiệm chi phí CRM.

### 4. Xử lý thị trường Đức (Tỷ lệ hủy đơn 24,2%)
- Tích hợp cổng thanh toán phổ biến tại Đức (GiroPay, Sofort, Klarna).
- Hợp tác với đơn vị chuyển phát nội địa (DHL Paket) nhằm rút ngắn thời gian giao hàng dưới 72 giờ.
- Minh bạch biểu phí thuế nhập khẩu và thủ tục hải quan tại bước thanh toán.

---

## 📚 Tài Liệu Chi Tiết

- 📄 **Báo cáo Kỹ thuật Đầy đủ:** [`report/technical_report.md`](file:///d:/online-retail-data-analysis/report/technical_report.md)
- 📊 **Bộ hình ảnh biểu đồ phân tích:** [`outputs/figures/`](file:///d:/online-retail-data-analysis/outputs/figures/)
- 📑 **Bộ bảng số liệu CSV trích xuất:** [`outputs/tables/`](file:///d:/online-retail-data-analysis/outputs/tables/)

---
**Nhóm Sinh Viên Thực Hiện — Học kỳ 1, Năm học 2026-2027**  
*Mã học phần: 71DAEE10012*
