# Backend QA Report

## 1. Environment
- **Operating System:** Windows (Docker Desktop Linux WSL2 backend)
- **Python Version:** 3.12 (Host) / Python 3.11-slim (Docker Container)
- **FastAPI Version:** >=0.110.0 (Installed 0.142.2)
- **Uvicorn Version:** >=0.28.0 (Installed 0.54.0)
- **Database Engine:** MongoDB 7.0 Community Edition (NoSQL)
- **MongoDB Drivers:** Motor 3.7.1 (Async Driver) + PyMongo 4.18.2 (Sync Driver) + MongoMock 4.3.0
- **Validation Engine:** Pydantic v2 (2.13.5) + Pydantic-Settings (2.15.0)
- **Docker Compose:** Docker Compose v5.0.2 / Docker Engine 29.2.1

## 2. Dependency Check
- **Packages Audit:**
  - `fastapi`: Đã kiểm tra & hoạt động tốt.
  - `uvicorn[standard]`: Đã kiểm tra & hoạt động tốt.
  - `pydantic` & `pydantic-settings`: Đã kiểm tra, nạp config hợp lệ.
  - `python-dotenv`: Đã bổ sung vào `backend/requirements.txt` để hỗ trợ load file `.env` không lỗi.
  - `pymongo` & `motor`: Đã cài đặt thành công vào Docker image mà không dùng cache.
  - `pandas`: Hoạt động ổn định phục vụ Seeding Script.
  - `pytest` & `httpx`: Hoạt động tốt phục vụ kiểm thử API và mock database.
- **Tình trạng:** Không còn sót bất kỳ thư viện SQL nào (`psycopg2`, `sqlalchemy`, `alembic`, `sqlite3`, `mysql`).

## 3. MongoDB Check
- **Container MongoDB:** `online_retail_mongodb` (Image `mongo:7.0`) chạy ổn định với status `healthy`.
- **Database Name:** `online_retail`
- **Dữ liệu nạp (Seed Database):** Thực thi thành công trong 2.03 giây, tính toán Idempotent (chạy lại không phát sinh duplicate).
- **Collections & Documents:**
  - `customers`: 4,371 documents
  - `invoices`: 23,796 documents
  - `customer_rfm`: 4,317 documents
  - `customer_segments`: 4,317 documents
  - `monthly_revenue`: 13 documents
  - `country_revenue`: 10 documents
  - `product_revenue`: 10 documents
  - `statistical_tests`: 2 documents
  - `kmeans_evaluation`: 6 documents
  - `customer_segments_summary`: 3 documents
  - `invoice_value_summary`: 10 documents
  - `products`: 3,938 documents
- **Indexing:** Toàn bộ Single & Compound Indexes (`customer_id`, `invoice_no`, `stock_code`, `cluster`, `membership_tier`, `year_month`, `country`) được khởi tạo thành công.
- **Health Endpoint:** `GET /health/db` trả về HTTP 200 OK với `{"status": "ok", "database": "online_retail"}`.

## 4. API Test
Đã kiểm thử toàn bộ 17 endpoints chính cùng các biến thể phân trang và bộ lọc:
- `GET /health`: 200 OK
- `GET /health/db`: 200 OK
- `GET /docs` & `GET /redoc`: 200 OK (Swagger UI & Redoc UI)
- `GET /api/v1/dashboard/summary`: 200 OK
- `GET /api/v1/dashboard/revenue-trend`: 200 OK
- `GET /api/v1/dashboard/top-products`: 200 OK
- `GET /api/v1/dashboard/top-countries`: 200 OK
- `GET /api/v1/sales/monthly`: 200 OK
- `GET /api/v1/sales/products` (Pagination + Search): 200 OK
- `GET /api/v1/sales/countries`: 200 OK
- `GET /api/v1/sales/invoices` (Pagination + Status Filter): 200 OK
- `GET /api/v1/customers` (RFM & Cluster Filters): 200 OK
- `GET /api/v1/customers/{customer_id}`: 200 OK
- `GET /api/v1/segmentation/summary`: 200 OK
- `GET /api/v1/segmentation/evaluation`: 200 OK
- `GET /api/v1/segmentation/clusters/{cluster_id}`: 200 OK
- `GET /api/v1/statistics/tests`: 200 OK
- `GET /api/v1/statistics/invoice-value-summary`: 200 OK

## 5. Data Consistency
So sánh đối chiếu trực tiếp dữ liệu API với source file CSV tại `outputs/tables/`:
- **Monthly Revenue:** Tổng doanh thu Net Revenue từ API là `9,748,131.07 £` khớp chính xác 100% với file `monthly_revenue.csv`.
- **Customer Segmentation:** Tổng số khách hàng phân cụm là `4,317` khớp chính xác 100% với `customer_segments_summary.csv`.
- **Top Product #1:** Mã sản phẩm `22423` khớp chính xác 100% với `top_products_revenue.csv`.
- **Top Country #1:** `United Kingdom` khớp chính xác 100% với `country_revenue.csv`.
- **Statistical Tests:** 2 bài kiểm định (ANOVA F-test & Mann-Whitney U test) khớp chính xác 100% với `statistical_tests_summary.csv`.
- **K-Means Evaluation:** 6 hàng chỉ số (k=2 đến k=7) khớp chính xác 100% với `kmeans_evaluation_metrics.csv`.

## 6. Error Handling
- **Query Parameter Validation (HTTP 422):**
  - `page=0` -> Trả về lỗi 422 chuẩn Unprocessable Entity.
  - `page_size=0` hoặc `page_size=101` -> Trả về lỗi 422 chuẩn.
  - `cluster_id=abc` (sai kiểu dữ liệu) -> Trả về lỗi 422 chuẩn.
- **Range Validation (HTTP 400):**
  - `min_monetary=1000&max_monetary=100` -> Trả về HTTP 400 với thông báo rõ ràng "min_monetary cannot be greater than max_monetary".
- **Not Found Handling (HTTP 404):**
  - `customer_id=NOT_FOUND_99999` -> Trả về HTTP 404 "Customer with ID 'NOT_FOUND_99999' not found".
  - `cluster_id=999` -> Trả về HTTP 404 "Cluster with ID 999 not found".
  - Đường dẫn không tồn tại -> Trả về HTTP 404 chuẩn.
- **Database & Server Exceptions (HTTP 503 / 500):**
  - Không leak stack trace / database connection string ra ngoài client.

## 7. Docker Check
- Lệnh chạy kiểm tra:
  ```bash
  docker compose down
  docker compose build --no-cache backend
  docker compose up -d
  ```
- Kết quả `docker compose ps`:
  - `online_retail_mongodb`: **Up (healthy)**
  - `online_retail_backend`: **Up (healthy)**
- **Root Cause lỗi container crash cũ:** Container cũ bị lỗi `ModuleNotFoundError: No module named 'pymongo'` do Docker image được build trước khi `requirements.txt` cập nhật `pymongo`. Sau khi rebuild `--no-cache`, toàn bộ thư viện được cài đặt đầy đủ và container khởi động mượt mà.

## 8. Code Cleanup
- **Đã xóa file thừa:**
  - `backend/app/core/database.py` (file re-export trung gian không còn ai tham chiếu).
  - Thư mục `backend/app/models/` (tàn dư ghi docstring SQLAlchemy cũ).
  - `backend/docker-compose.yml` (bị trùng lặp với file `docker-compose.yml` ở thư mục gốc).
- **Dọn dẹp cache:** Toàn bộ thư mục `__pycache__` và file `.pyc` rác đã được xóa sạch.

## 9. Security Check
- **Kiểm tra Credentials:** Không có mật khẩu, token, API key hay MongoDB URI nhạy cảm nào bị hard-code trong mã nguồn.
- **Bảo mật Git:** Đã bổ sung `.env` và `**/.env` vào file `.gitignore` ở thư mục gốc để ngăn chặn nguy cơ vô tình commit file biến môi trường lên git.
- **CORS:** Đã giới hạn rõ ràng danh sách origins cho Vite (`http://localhost:5173`, `http://127.0.0.1:5173`).

## 10. Remaining Issues
- Không có vấn đề blocking. Hệ thống backend hiện tại hoàn toàn sẵn sàng để tích hợp với React Frontend.

## 11. Final Status
**PASS**
