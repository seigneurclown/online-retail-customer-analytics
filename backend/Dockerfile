# ================================================================
# Dockerfile cho Online Retail Analytics Backend
# Python 3.11-slim | FastAPI | NoSQL MongoDB
# Học phần: DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)
# ================================================================

FROM python:3.11-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app/backend

# Ngăn chặn Python sinh file .pyc và bật stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/backend

# Cài đặt thư viện hệ thống cần thiết (nếu có)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy và cài đặt Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn backend vào container
COPY app ./app
COPY scripts ./scripts
COPY README.md .

# Expose port chạy của FastAPI
EXPOSE 8000

# Healthcheck kiểm tra container hoạt động
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Lệnh khởi chạy server Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
