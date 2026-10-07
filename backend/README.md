# Online Retail Analytics Platform — Backend Service

> **Học phần:** DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)  
> **Đề tài:** Phân tích dữ liệu doanh thu và Phân cụm hành vi khách hàng trong lĩnh vực bán lẻ  
> **Kiến trúc:** Layered Clean Architecture (API -> Service -> Repository -> MongoDB)  
> **Công nghệ:** Python 3.10+ | FastAPI | Pydantic v2 | Motor (Async) | PyMongo (Sync) | MongoDB | Docker  

---

## 🏗️ Kiến Trúc Hệ Thống (Architecture Flow)

```text
React Frontend (Vite + Tailwind + TypeScript)
                     ↓
FastAPI REST API (/api/v1/ - Pydantic v2 Validation)
                     ↓
               Service Layer
                     ↓
              Repository Layer
                     ↓
       MongoDB Database (NoSQL Engine)
                     ↑
  ETL Data Ingestion (scripts/seed_database.py)
                     ↑
Existing Analytics Results (data/processed/ & outputs/tables/)
```

---

## 📂 Danh Sách API Endpoints (/api/v1/)

### 1. Dashboard
- `GET /api/v1/dashboard/summary`: 4 chỉ số KPI chính (`total_revenue`, `total_orders`, `total_customers`, `average_order_value`).
- `GET /api/v1/dashboard/revenue-trend`: Dữ liệu xu hướng doanh thu theo tháng (Line Chart).
- `GET /api/v1/dashboard/top-products?limit=10`: Top sản phẩm doanh thu cao nhất.
- `GET /api/v1/dashboard/top-countries?limit=10`: Top quốc gia đóng góp doanh thu nhiều nhất.

### 2. Sales & Invoices
- `GET /api/v1/sales/monthly?year=2011`: Doanh thu chi tiết theo tháng (lọc theo năm).
- `GET /api/v1/sales/products`: Phân trang sản phẩm, tìm kiếm từ khóa, sắp xếp doanh thu.
- `GET /api/v1/sales/countries`: Phân trang doanh thu theo quốc gia.
- `GET /api/v1/sales/invoices`: Phân trang hóa đơn kết hợp lọc quốc gia, hủy đơn và khoảng giá trị (`min_value`, `max_value`).

### 3. Customer & RFM
- `GET /api/v1/customers`: Phân trang khách hàng kèm chỉ số RFM, lọc theo cụm K-Means, MembershipTier, khoảng Recency/Frequency/Monetary.
- `GET /api/v1/customers/{customer_id}`: Chi tiết hồ sơ phân khúc một khách hàng.

### 4. Segmentation & ML Evaluation
- `GET /api/v1/segmentation/summary`: Bảng tổng hợp các cụm K-Means kèm đặc trưng hành vi và tỷ trọng doanh thu.
- `GET /api/v1/segmentation/clusters/{cluster_id}`: Chi tiết một cụm K-Means.
- `GET /api/v1/segmentation/evaluation`: Chỉ số Elbow WCSS (Inertia) và Silhouette Score qua các giá trị K.

### 5. Statistics
- `GET /api/v1/statistics/tests`: Kết quả kiểm định giả thuyết thống kê (Mann-Whitney U, Chi-Square).
- `GET /api/v1/statistics/invoice-value-summary`: Thống kê mô tả phân phối giá trị đơn hàng.

---

## 🚀 Hướng Dẫn Khởi Chạy

### Cách 1: Chạy bằng Docker Compose (Khuyên dùng)
```bash
# Khởi động đồng thời MongoDB và FastAPI Backend
docker compose up --build -d

# Nạp dữ liệu vào MongoDB container
docker compose exec backend python scripts/seed_database.py
```
- **Tài liệu Swagger:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **App Health:** [http://localhost:8000/health](http://localhost:8000/health)
- **Database Health:** [http://localhost:8000/health/db](http://localhost:8000/health/db)

### Cách 2: Chạy trực tiếp trên máy host
```bash
cd backend
pip install -r requirements.txt

# Nạp dữ liệu vào MongoDB local
python scripts/seed_database.py

# Khởi động server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🧪 Chạy Kiểm Thử Tự Động (41 Test Cases)
```bash
cd backend
pytest tests/ -v
```

---

## 💻 Hợp Đồng Giao Tiếp React (Frontend Contract)
Các định nghĩa TypeScript interface dành cho Frontend nằm tại:
👉 [`backend/docs/frontend_contracts.ts`](docs/frontend_contracts.ts)
