# BÁO CÁO KỸ THUẬT VÀ PHÂN TÍCH QUẢN TRỊ KINH DOANH

> **Học phần:** DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012) – Sem1/2026-2027  
> **Đề tài:** Phân tích dữ liệu doanh thu và Phân cụm hành vi khách hàng trong lĩnh vực bán lẻ  
> **Tập dữ liệu:** Online Retail Dataset – UCI Machine Learning Repository (~541.909 giao dịch)  
> **Nhóm thực hiện:** Nhóm nghiên cứu & phân tích dữ liệu kinh doanh  

---

## 📑 MỤC LỤC

1. [Tóm Tắt Điều Hành (Executive Summary)](#1-tóm-tắt-điều-hành-executive-summary)
2. [Giới Thiệu Đề Tài & Bối Cảnh Kinh Doanh](#2-giới-thiệu-đề-tài--bối-cảnh-kinh-doanh)
3. [Dữ Liệu & Quy Trình Tiền Xử Lý (Data Preprocessing)](#3-dữ-liệu--quy-trình-tiền-xử-lý-data-preprocessing)
4. [Phân Tích Doanh Thu & Hiệu Suất Vận Hành](#4-phân-tích-doanh-thu--hiệu-suất-vận-hành)
5. [Kiểm Định Giả Thuyết Thống Kê](#5-kiểm-định-giả-thuyết-thống-kê)
6. [Mô Hình Hóa Phân Cụm Khách Hàng (RFM & K-Means)](#6-mô-hình-hóa-phân-cụm-khách-hàng-rfm--k-means)
7. [Chân Dung Phân Khúc & Hạng Thẻ Hội Viên](#7-chân-dung-phân-khúc--hạng-thẻ-hội-viên)
8. [Khuyến Nghị Chiến Lược Hành Động](#8-khuyến-nghị-chiến-lược-hành-động)
9. [Hạn Chế Của Đề Tài & Hướng Phát Triển](#9-hạn-chế-của-đề-tài--hướng-phát-triển)
10. [Kết Luận](#10-kết-luận)

---

## 1. TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

Báo cáo này trình bày toàn diện dự án phân tích dữ liệu kinh doanh bán lẻ trực tuyến dựa trên tập dữ liệu chuẩn **Online Retail Dataset (UCI Machine Learning Repository)** bao gồm 541.909 giao dịch phát sinh từ ngày **01/12/2010 đến 09/12/2011**.

Dự án được xây dựng với mục tiêu kép:
1. **Khám phá & Kiểm định:** Làm rõ cấu trúc doanh thu, chu kỳ mùa vụ và kiểm định các giả thuyết kinh doanh then chốt bằng phương pháp thống kê chặt chẽ.
2. **Mô hình hóa & Hành động:** Kết hợp mô hình định lượng **RFM (Recency - Frequency - Monetary)** cùng thuật toán **K-Means**, từ đó đề xuất hệ thống **Hạng thẻ Hội viên (Membership Tiers)** giúp tối ưu hóa chuyển đổi và giữ chân khách hàng.

### 📊 Bảng Chỉ Số Toàn Hệ Thống

| Chỉ số tổng quan | Giá trị ghi nhận | Đơn vị đo | Ý nghĩa thực tiễn |
| :--- | ---: | :---: | :--- |
| **Giao dịch hợp lệ sau làm sạch** | 392.732 | Dòng | Đã lọc trùng, đơn hủy và mã phi thương mại |
| **Số khách hàng định danh duy nhất** | 4.339 | Khách hàng | Cơ sở khách hàng thực tế để xây dựng RFM |
| **Tổng số hóa đơn thành công** | 19.960 | Hóa đơn | Trung bình mỗi khách thực hiện 4,6 đơn hàng |
| **Tổng doanh thu thuần (Net Revenue)** | **£8.291.748,56** | Bảng Anh (£) | Doanh thu sau khi trừ toàn bộ đơn hoàn trả |
| **Giá trị đơn hàng trung vị (Median)** | **£303,30** | Bảng Anh (£) | Phản ánh trung thực quy mô giỏ hàng điển hình |
| **Thị phần thị trường nội địa (UK)** | **84,01%** | Tỷ trọng | Đóng vai trò hạt nhân trong cơ cấu doanh thu |

---

## 2. GIỚI THIỆU ĐỀ TÀI & BỐI CẢNH KINH DOANH

### 2.1. Đặt Vấn Đề
Trong thương mại điện tử hiện đại, doanh nghiệp đối mặt với chi phí thu hút khách hàng mới (CAC) ngày càng đắt đỏ. Phương pháp tiếp thị đại trà (Mass Marketing) bộc lộ sự lãng phí nghiêm trọng. Việc cá nhân hóa theo từng nhóm hành vi nhằm tối đa hóa Giá trị vòng đời khách hàng (Customer Lifetime Value - CLV) là đòi hỏi sống còn.

### 2.2. Mục Tiêu Nghiên Cứu
- **Khám phá vận hành:** Định vị chu kỳ doanh thu, sản phẩm chủ lực và thị trường xuất khẩu trọng điểm.
- **Chứng minh bằng thống kê:** Xác định sự khác biệt về quy mô giỏ hàng giữa ngày thường và cuối tuần; tìm hiểu nguyên nhân tỷ lệ hủy đơn cao ở thị trường nước ngoài.
- **Phân cụm khoa học:** Áp dụng kỹ thuật học máy không giám sát để phân nhóm khách hàng không thiên kiến.
- **Ứng dụng thực tiễn:** Thiết kế chính sách Hạng thẻ Hội viên (Vàng, Bạc, Chuẩn) gắn liền với ngân sách và chương trình hành động cụ thể.

---

## 3. DỮ LIỆU & QUY TRÌNH TIỀN XỬ LÝ (DATA PREPROCESSING)

### 3.1. Cấu Trúc Dữ Liệu Thô

Tập dữ liệu thô gồm **541.909 dòng** và **8 thuộc tính**:

| Cột dữ liệu | Kiểu dữ liệu | Ý nghĩa nghiệp vụ |
| :--- | :---: | :--- |
| `InvoiceNo` | String | Mã hóa đơn 6 chữ số; tiền tố `C` thể hiện giao dịch hủy |
| `StockCode` | String | Mã sản phẩm định danh duy nhất |
| `Description` | String | Tên mô tả mặt hàng quà tặng |
| `Quantity` | Integer | Số lượng mua (âm nếu là hàng trả lại) |
| `InvoiceDate` | Datetime | Thời điểm phát sinh đơn hàng |
| `UnitPrice` | Float | Đơn giá niêm yết tính bằng bảng Anh (£) |
| `CustomerID` | Float | Mã định danh khách hàng (trống nếu là khách vãng lai) |
| `Country` | String | Quốc gia nhận hàng |

### 3.2. Bốn Vấn Đề Chất Lượng Dữ Liệu Phát Hiện Qua EDA

```
[1] 5.268 dòng trùng lặp hoàn toàn
    └── Khắc phục: Xóa bỏ thông qua drop_duplicates().

[2] 135.080 dòng khuyết thiếu CustomerID (24,93%)
    └── Khắc phục: Phân tách thành tập phân tích vĩ mô và tập RFM vi mô.

[3] 9.288 dòng giao dịch hủy (InvoiceNo bắt đầu bằng 'C')
    └── Khắc phục: Gắn cờ IsCancelled để tính riêng doanh thu giảm trừ.

[4] Mã phi sản phẩm & Đơn giá phi lý (UnitPrice <= 0)
    └── Khắc phục: Loại bỏ các mã kế toán nội bộ (POST, D, BANK CHARGES, AMAZONFEE).
```

### 3.3. Công Thức Tính Doanh Thu Thuần

$$\text{Revenue} = \text{Quantity} \times \text{UnitPrice}$$

> **Quy ước kế toán:** Với các đơn hàng hủy (`Quantity < 0`), giá trị `Revenue` nhận giá trị âm, phản ánh chính xác dòng tiền giảm trừ vào tổng doanh thu thuần toàn công ty.

---

## 4. PHÂN TÍCH DOANH THU & HIỆU SUẤT VẬN HÀNH

### 4.1. Xu Hướng Doanh Thu Theo Tháng (Monthly Breakdown)

| Tháng | Doanh thu gộp (£) | Giá trị hoàn trả (£) | Doanh thu thuần (£) | Số đơn hàng | Sản lượng bán |
| :---: | ---: | ---: | ---: | ---: | ---: |
| **2010-12** | 821.452,73 | -74.729,12 | 746.723,61 | 1.885 | 342.009 |
| **2011-01** | 689.811,61 | -131.363,05 | 558.448,56 | 1.346 | 307.255 |
| **2011-02** | 522.545,56 | -25.519,15 | 497.026,41 | 1.319 | 280.069 |
| **2011-03** | 716.215,26 | -34.201,28 | 682.013,98 | 1.772 | 371.424 |
| **2011-04** | 536.968,49 | -44.600,65 | 492.367,84 | 1.486 | 294.309 |
| **2011-05** | 769.296,61 | -47.202,51 | 722.094,10 | 1.995 | 389.133 |
| **2011-06** | 760.547,01 | -70.569,78 | 689.977,23 | 1.862 | 381.175 |
| **2011-07** | 718.076,12 | -37.919,13 | 680.156,99 | 1.745 | 393.666 |
| **2011-08** | 757.841,38 | -54.330,80 | 703.510,58 | 1.639 | 408.675 |
| **2011-09** | 1.056.435,19 | -38.838,51 | 1.017.596,68 | 2.170 | 562.243 |
| **2011-10** | 1.151.263,73 | -81.895,50 | 1.069.368,23 | 2.402 | 598.077 |
| **2011-11** | 1.503.866,78 | -47.720,98 | **1.456.145,80** | **3.210** | **738.782** |
| **2011-12\*** | 637.790,33 | -205.089,27 | 432.701,06 | 965 | 230.043 |

*\*Ghi chú: Dữ liệu tháng 12/2011 chỉ ghi nhận 9 ngày đầu tiên (kết thúc ngày 09/12/2011).*

> **Nhận định:** Doanh thu tăng trưởng vượt bậc từ tháng 09/2011 và đạt đỉnh lịch sử vào tháng 11/2011 (**£1,456 triệu**). Đây là chu kỳ tích trữ hàng hóa mùa lễ hội (Black Friday, Cyber Monday, Christmas).

### 4.2. Top 5 Sản Phẩm Dẫn Đầu Doanh Thu

| Thứ hạng | Mã SP | Tên sản phẩm | Doanh thu (£) | Sản lượng bán | Số lượt đặt |
| :---: | :---: | :--- | ---: | ---: | ---: |
| 1 | `22423` | REGENCY CAKESTAND 3 TIER | **£174.156,54** | 13.851 | 1.988 |
| 2 | `23843` | PAPER CRAFT , LITTLE BIRDIE | **£168.469,60** | 80.995 | 1 |
| 3 | `85123A` | WHITE HANGING HEART T-LIGHT HOLDER | **£104.462,75** | 37.641 | 2.198 |
| 4 | `47566` | PARTY BUNTING | **£99.445,23** | 18.283 | 1.685 |
| 5 | `85099B` | JUMBO BAG RED RETROSPOT | **£94.159,81** | 48.371 | 2.089 |

### 4.3. Thị Trường Địa Lý & Tỷ Trọng Xuất Khẩu

| Quốc gia | Doanh thu (£) | Tỷ trọng DT | Số hóa đơn | Số khách hàng |
| :--- | ---: | ---: | ---: | ---: |
| **United Kingdom** | £8.189.252,30 | **84,01%** | 21.391 | 3.949 |
| **Netherlands** | £284.661,54 | **2,92%** | 100 | 9 |
| **EIRE (Ireland)** | £262.993,38 | **2,70%** | 360 | 3 |
| **Germany** | £221.509,47 | **2,27%** | 603 | 95 |
| **France** | £197.317,11 | **2,02%** | 461 | 87 |
| **Australia** | £137.009,77 | **1,41%** | 69 | 9 |

### 4.4. Phân Phối Giá Trị Đơn Hàng (Invoice Value)

- **Số lượng mẫu:** 19.960 hóa đơn thành công
- **Giá trị trung bình (Mean):** **£533,17**
- **Giá trị trung vị (Median):** **£303,30**
- **Khoảng tứ phân vị (IQR):** **£341,77** ($Q_1 = £151,70$ | $Q_3 = £493,46$)
- **Hệ số bất đối xứng (Skewness):** **51,08** (Lệch phải cực mạnh)

> **Ý nghĩa thực tiễn:** Độ lệch chuẩn rất cao (£1.780,41) và Skewness = 51,08 chứng minh giá trị trung bình bị kéo lệch bởi các đơn hàng mua sỉ quy mô lớn. Do đó, trung vị (£303,30) là thước đo thực tế hơn về hành vi mua sắm thông thường.

---

## 5. KIỂM ĐỊNH GIẢ THUYẾT THỐNG KÊ

### 5.1. Kiểm Định 1: So Sánh Giá Trị Đơn Hàng Weekday vs. Weekend

> - **Giả thuyết $H_0$:** Giá trị đơn hàng giữa các ngày trong tuần (T2-T6) và cuối tuần (Chủ nhật) là đồng nhất.  
> - **Giả thuyết $H_1$:** Giá trị đơn hàng giữa ngày thường và cuối tuần có sự khác biệt mang ý nghĩa thống kê.

- **Phương pháp lựa chọn:** **Mann-Whitney U Test** (Kiểm định phi tham số, do dữ liệu vi phạm giả định phân phối chuẩn với Skewness = 51,08).
- **Kết quả kiểm định:**
  - Thống kê $U$: **21.088.569,0**
  - $p\text{-value}$: **$2,473 \times 10^{-9} \ll 0,05$**
  - Trung vị Weekday: **£311,70** | Trung vị Weekend: **£250,55**
- **Kết luận:** **Bác bỏ $H_0$**. Đơn hàng ngày thường có quy mô giá trị cao hơn đáng kể so với cuối tuần, phản ánh tập khách hàng bán buôn (B2B) hoạt động tập trung vào giờ hành chính.

### 5.2. Kiểm Định 2: Mối Quan Hệ Giữa Quốc Gia Và Tỷ Lệ Hủy Đơn

> - **Giả thuyết $H_0$:** Tỷ lệ hủy đơn hoàn toàn độc lập với quốc gia nhận hàng.  
> - **Giả thuyết $H_1$:** Tỷ lệ hủy đơn có mối phụ thuộc có ý nghĩa thống kê vào quốc gia.

- **Phương pháp lựa chọn:** **Chi-Square Test of Independence** trên bảng chéo 2 chiều (Quốc gia $\times$ Trạng thái đơn hàng).
- **Kết quả kiểm định:**
  - Thống kê $\chi^2$: **38,36** (Bậc tự do $df = 4$)
  - $p\text{-value}$: **$9,465 \times 10^{-8} \ll 0,05$**
  - Tỷ lệ hủy đơn thực tế theo quốc gia:
    - **Đức (Germany): 24,20%** *(Cao vượt trội)*
    - **Pháp (France): 16,04%**
    - **Vương quốc Anh (UK): 13,85%**
    - **Ireland (EIRE): 13,25%**
    - **Hà Lan (Netherlands): 10,71%**
- **Kết luận:** **Bác bỏ $H_0$**. Quốc gia ảnh hưởng rõ rệt đến tỷ lệ hủy đơn. Tỷ lệ hủy gần 1/4 đơn hàng tại Đức là tín hiệu cảnh báo nghiêm trọng về thủ tục hải quan, phí hoàn trả hoặc rào cản cổng thanh toán.

---

## 6. MÔ HÌNH HÓA PHÂN CỤM KHÁCH HÀNG (RFM & K-MEANS)

### 6.1. Xây Dựng Bộ Chỉ Số RFM
- **Recency ($R$):** Số ngày kể từ đơn hàng cuối cùng đến ngày chốt sổ ($10/12/2011$).
- **Frequency ($F$):** Tổng số hóa đơn thành công của khách hàng.
- **Monetary ($M$):** Tổng số tiền (£) khách hàng chi trả thực tế.

### 6.2. Tiền Xử Lý Dữ Liệu RFM
Do cả 3 biến số đều có phân phối lệch phải nghiêm trọng, quy trình xử lý 2 bước được thực thi:
1. **Log-Transform:** $x' = \ln(x + 1)$ nhằm thu nhỏ độ chênh lệch cực trị.
2. **StandardScaler:** Chuẩn hóa $z = \frac{x' - \mu}{\sigma}$ đưa các biến về cùng thang đo $(\mu=0, \sigma=1)$ phục vụ đo khoảng cách Euclidean.

### 6.3. Đánh Giá Lựa Chọn Số Cụm Tối Ưu ($K$)

| Số cụm ($K$) | Inertia (WCSS) | Silhouette Score | Nhận định thuật toán & nghiệp vụ |
| :---: | ---: | :---: | :--- |
| **2** | 6.357,38 | 0,4312 | Phân tách thô sơ, chưa phản ánh được khách hàng trung lưu |
| **3** | **4.805,89** | **0,3400** | **Điểm gập Elbow tối ưu; Silhouette ổn định; Hoàn toàn phù hợp mô hình 3 hạng thẻ** |
| **4** | 3.915,39 | 0,3354 | Bắt đầu phân mảnh nhóm trung thành |
| **5** | 3.356,04 | 0,3013 | Silhouette suy giảm, cụm chồng lấn |
| **6** | 2.873,61 | 0,3102 | Phân mảnh quá mức, khó quản trị |
| **7** | 2.581,56 | 0,3083 | Không khả thi cho triển khai marketing |

> **Quyết định mô hình:** Chọn **$K = 3$** vì vừa tối ưu hóa chỉ số hình học vừa hài hòa với cấu trúc phân cấp hội viên tiêu chuẩn của doanh nghiệp.

---

## 7. CHÂN DUNG PHÂN KHÚC & HẠNG THẺ HỘI VIÊN

```
                                    TỔNG THỂ 4.339 KHÁCH HÀNG
                                                │
         ┌──────────────────────────────────────┼──────────────────────────────────────┐
         ▼                                      ▼                                      ▼
┌─────────────────────────┐            ┌─────────────────────────┐            ┌─────────────────────────┐
│  THẺ VÀNG - KIM CƯƠNG   │            │        THẺ BẠC          │            │       HẠNG CHUẨN        │
│    (Gold / Champions)   │            │   (Silver / Potential)  │            │  (Standard / At-Risk)   │
├─────────────────────────┤            ├─────────────────────────┤            ├─────────────────────────┤
│ • Số lượng: 781 khách   │            │ • Số lượng: 1.701 khách │            │ • Số lượng: 1.835 khách │
│ • Tỷ lệ khách: 18,09%   │            │ • Tỷ lệ khách: 39,40%   │            │ • Tỷ lệ khách: 42,51%   │
│ • Doanh thu: 67,15%     │            │ • Doanh thu: 25,53%     │            │ • Doanh thu: 7,33%      │
│ • Recency TB: 13 ngày   │            │ • Recency TB: 54 ngày   │            │ • Recency TB: 162 ngày  │
│ • Frequency TB: 13,0 đơn│            │ • Frequency TB: 3,5 đơn │            │ • Frequency TB: 1,3 đơn │
│ • Monetary TB: £7.129   │            │ • Monetary TB: £1.244   │            │ • Monetary TB: £331     │
└─────────────────────────┘            └─────────────────────────┘            └─────────────────────────┘
```

### Bảng Chỉ Số Chi Tiết Giữa Các Phân Khúc

| Hạng Thẻ Hội Viên | Mã Cụm | Số Khách | Tỷ Lệ Khách | Recency TB | Recency Med | Freq TB | Freq Med | Monetary TB | Monetary Med | Tổng Doanh Thu (£) | Tỷ Trọng DT |
| :--- | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🥇 **Thẻ Vàng - Kim Cương** | 2 | **781** | **18,09%** | 13,1 ngày | 8 ngày | 13,0 đơn | 9 đơn | £7.129,01 | £3.444,39 | **£5.567.756,47** | **67,15%** |
| 🥈 **Thẻ Bạc (Silver)** | 0 | **1.701** | **39,40%** | 53,6 ngày | 36 ngày | 3,5 đơn | 3 đơn | £1.244,26 | £972,08 | **£2.116.488,32** | **25,53%** |
| 🥉 **Không Thẻ / Hạng Chuẩn** | 1 | **1.835** | **42,51%** | 161,7 ngày | 151 ngày | 1,3 đơn | 1 đơn | £331,06 | £272,07 | **£607.503,77** | **7,33%** |

---

## 8. KHUYẾN NGHỊ CHIẾN LƯỢC HÀNH ĐỘNG

Dựa trên kết quả phân tích định lượng, đề xuất bộ giải pháp 4 trụ cột chiến lược:

### 8.1. Trụ Cột 1: Bảo Vệ Nhóm Khách Hàng Thẻ Vàng - Kim Cương (67% Doanh Thu)
- **Quản lý tài khoản VIP (Key Account Management):** Cử chuyên viên hỗ trợ 1-1 phục vụ 781 khách hàng hàng đầu.
- **Cam kết chuỗi cung ứng:** Ưu tiên giữ hàng tồn kho đối với các sản phẩm chiến lược như *Regency Cakestand* vào cao điểm Q4; miễn phí chuyển phát hỏa tốc.
- **Chính sách chiết khấu khối lượng:** Thiết lập hợp đồng thương mại với chiết khấu bậc thang theo tháng để giữ chân bạn hàng lâu dài.

### 8.2. Trụ Cột 2: Đẩy Mạnh Chuyển Hóa Khách Hàng Thẻ Bạc Lên Vàng
- **Chiến dịch "Bứt phá lên Vàng":** Thiết lập thanh tiến trình chi tiêu (Progress Bar) thông báo số tiền còn thiếu để nhận quyền lợi thẻ Vàng.
- **Tự động hóa kích cầu (Cadence Re-engagement):** Gửi email cá nhân hóa sau 30-45 ngày kèm mã ưu đãi có hạn dùng 7 ngày, mục tiêu rút ngắn Recency từ 54 ngày xuống dưới 30 ngày.
- **Bán chéo thông minh (Cross-selling):** Gợi ý các sản phẩm bổ trợ cùng nhóm phong cách thiết kế với đơn hàng vừa mua.

### 8.3. Trụ Cột 3: Tối Ưu Hóa Chi Phí Tương Tác Với Hạng Chuẩn
- **Dừng tiếp thị đại trà tốn kém:** Không áp dụng SMS Brandname hay telesales cho nhóm này; chuyển toàn bộ sang hệ thống Email Marketing tự động chi phí thấp.
- **Chiến dịch tái kích hoạt dịp lễ:** Gửi ưu đãi 1 lần vào mùa mua sắm Black Friday / Giáng sinh để thăm dò nhu cầu.
- **Sàng lọc dữ liệu định kỳ:** Tự động chuyển các hồ sơ không có bất kỳ tương tác nào sau 360 ngày sang kho lưu trữ để tối ưu chi phí hạ tầng CRM.

### 8.4. Trụ Cột 4: Tái Cấu Trúc Vận Hành Thị Trường Đức (Giảm Tỷ Lệ Hủy Đơn 24,2%)
- **Hợp tác đối tác vận chuyển nội địa Đức:** Tích hợp trực tiếp với DHL Paket để đảm bảo thời gian giao vận dưới 72 giờ và cung cấp mã theo dõi thời gian thực.
- **Cổng thanh toán bản địa hóa:** Bổ sung các phương thức thanh toán quen thuộc của người Đức (Klarna Pay Later, Sofort, GiroPay).
- **Minh bạch thuế & thủ tục hải quan:** Tính toán và hiển thị rõ ràng toàn bộ chi phí thuế VAT nhập khẩu tại giỏ hàng để tránh việc khách hàng từ chối nhận bưu kiện.

---

## 9. HẠN CHẾ CỦA ĐỀ TÀI & HƯỚNG PHÁT TRIỂN

### 9.1. Hạn Chế Hiện Tại
1. **Dữ liệu khách vãng lai:** Gần 25% dòng giao dịch thiếu `CustomerID` nên chưa thể đưa vào mô hình phân cụm RFM.
2. **Khung thời gian quan sát:** Dữ liệu dừng ở ngày 09/12/2011, thiếu mất giai đoạn cao điểm cuối tháng 12 để đánh giá trọn vẹn tăng trưởng cả năm.
3. **Thiếu thông tin giá vốn (COGS):** Chưa có biên lợi nhuận thực tế của từng sản phẩm để tính chính xác lợi nhuận ròng trên từng cụm khách hàng.
4. **Thiếu nhân khẩu học:** Chưa có tuổi tác, giới tính hoặc địa chỉ cụ thể để phân tích theo mô hình STP chi tiết.

### 9.2. Hướng Phát Triển Tương Lai
1. **Dự báo CLV (Customer Lifetime Value):** Ứng dụng mô hình xác suất nâng cao (BG/NBD và Gamma-Gamma) để dự báo giá trị tương lai trong 12 tháng.
2. **Phân tích tập mặt hàng (Market Basket Analysis):** Sử dụng thuật toán Apriori hoặc FP-Growth để phát hiện các mẫu mua hàng đồng thời.
3. **Phân tích giữ chân theo nhóm thuần tập (Cohort Retention Analysis):** Theo dõi tỷ lệ sống sót (Survival Rate) của khách hàng theo từng tháng gia nhập.

---

## 10. KẾT LUẬN

Dự án đã hoàn thành trọn vẹn toàn bộ các mục tiêu đặt ra cho học phần **DATA ANALYSIS FOR BUSINESS ENVIRONMENT**:
- Xây dựng thành công quy trình xử lý dữ liệu chuẩn hóa, có thể tái lập 100% từ dữ liệu thô.
- Giải thích và kiểm định thành công các bài toán kinh doanh bằng công cụ thống kê tin cậy.
- Xây dựng mô hình phân khúc $K=3$ sắc nét, bóc tách được phân khúc **Thẻ Vàng - Kim Cương** (18% khách tạo ra 67% doanh thu) và đề xuất hệ thống giải pháp hành động cụ thể, đem lại giá trị thực tiễn cao cho doanh nghiệp bán lẻ.

---
**Nhóm Sinh Viên Nghiên Cứu Dự Án**  
*Mã học phần: 71DAEE10012 – Học kỳ 1, Năm học 2026-2027*
