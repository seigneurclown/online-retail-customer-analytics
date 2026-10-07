# Frontend Audit Report: Online Retail Analytics Platform

**Học phần:** DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)  
**Đề tài:** Phân tích dữ liệu doanh thu và Phân cụm hành vi khách hàng trong lĩnh vực bán lẻ  
**Người thực hiện:** Senior Frontend Engineer + QA Lead  
**Giai đoạn:** PHASE 1 — SOURCE AUDIT  
**Ngày thực hiện:** 01/10/2026  

---

## 1. Tech Stack Thực tế
- **Framework & Runtime:** React 19.2.8 + TypeScript 5.9.3 + Node.js 20.x Alpine
- **Build Tool:** Vite 8.3.1 (Hỗ trợ ESM, HMR, Rollup dynamic chunk splitting)
- **Styling:** Tailwind CSS v4.3.3 (`@tailwindcss/vite` tích hợp trong `vite.config.ts`)
- **Routing:** React Router v7.18.4 (`createBrowserRouter` / `Routes` với `React.lazy` code splitting)
- **HTTP Client:** Axios 1.20.0 (Tích hợp interceptors chuẩn hóa lỗi Pydantic 422 và timeout 15s)
- **Biểu đồ (Charts):** Recharts 3.10.1 (ResponsiveContainer, AreaChart, BarChart, ComposedChart, PieChart)
- **Icons:** Lucide React 1.49.0 (Tree-shakeable SVG icons)
- **Linter:** Oxlint 1.81.0 (Kiểm tra 116 rules trong 17ms)
- **Production Server:** Nginx Alpine (Reverse Proxy `/api/v1/` và `/health`, SPA fallback, gzip compression, asset caching)
- **Containerization:** Docker Multi-stage + Docker Compose

---

## 2. Cấu trúc Thư mục Frontend (Current Tree)
```text
frontend/
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── .oxlintrc.json
├── Dockerfile
├── nginx.conf
├── package.json
├── package-lock.json
├── README.md
├── index.html
├── vite.config.ts
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
├── public/
│   ├── favicon.svg
│   └── icons.svg
└── src/
    ├── App.tsx
    ├── main.tsx
    ├── index.css
    ├── assets/ (thư mục rỗng)
    ├── components/
    │   ├── cards/
    │   │   ├── MetricCard.tsx
    │   │   ├── ChartCard.tsx
    │   │   └── index.ts
    │   ├── charts/
    │   │   ├── RevenueTrendChart.tsx
    │   │   ├── TopCountriesChart.tsx
    │   │   ├── TopProductsChart.tsx
    │   │   ├── SegmentDistributionChart.tsx
    │   │   ├── MonthlyBreakdownChart.tsx
    │   │   ├── ClusterComparisonChart.tsx
    │   │   ├── KMeansEvaluationChart.tsx
    │   │   └── index.ts
    │   ├── common/
    │   │   ├── Badge.tsx
    │   │   ├── EmptyState.tsx
    │   │   ├── ErrorState.tsx
    │   │   ├── LoadingState.tsx
    │   │   ├── PageHeader.tsx
    │   │   ├── Pagination.tsx
    │   │   └── index.ts
    │   ├── layout/
    │   │   ├── AppLayout.tsx
    │   │   ├── Header.tsx
    │   │   └── Sidebar.tsx
    │   └── tables/
    │       ├── DataTable.tsx
    │       └── index.ts
    ├── hooks/
    │   ├── useCustomers.ts
    │   ├── useDashboard.ts
    │   ├── useSales.ts
    │   ├── useSegmentation.ts
    │   └── useStatistics.ts
    ├── pages/
    │   ├── Customers/
    │   │   ├── CustomerDetailPage.tsx
    │   │   └── index.tsx
    │   ├── Dashboard/
    │   │   └── index.tsx
    │   ├── NotFound/
    │   │   └── index.tsx
    │   ├── Sales/
    │   │   └── index.tsx
    │   ├── Segmentation/
    │   │   └── index.tsx
    │   └── Statistics/
    │       └── index.tsx
    ├── routes/
    │   └── index.tsx
    ├── services/
    │   ├── api.ts
    │   ├── customersApi.ts
    │   ├── dashboardApi.ts
    │   ├── salesApi.ts
    │   ├── segmentationApi.ts
    │   └── statisticsApi.ts
    ├── types/
    │   ├── common.ts
    │   ├── customer.ts
    │   ├── dashboard.ts
    │   ├── sales.ts
    │   ├── segmentation.ts
    │   └── statistics.ts
    └── utils/
        ├── formatCurrency.ts
        ├── formatDate.ts
        └── formatNumber.ts
```

---

## 3. Danh sách Tuyến đường (Routes Matrix)
1. `/` -> Điều hướng mặc định chuyển tiếp sang `/dashboard`
2. `/dashboard` -> Trang Tổng quan KPI, Doanh thu theo tháng, Top sản phẩm, Top quốc gia, Phân bổ phân khúc
3. `/sales` -> Trang Phân tích bán hàng chuyên sâu (Bộ lọc năm, Cơ cấu Gross/Cancelled/Net, Bảng sản phẩm, Quốc gia, Hóa đơn)
4. `/customers` -> Danh bạ khách hàng, lọc cụm K-Means, bộ lọc RFM Range validation, phân trang
5. `/customers/:customerId` -> Chi tiết hồ sơ RFM khách hàng, chỉ số R-F-M, phân hạng thẻ, thị trường giao dịch
6. `/segmentation` -> Hồ sơ 3 nhóm khách hàng (Gold, Silver, Standard), biểu đồ Elbow & Silhouette, bảng đối chuẩn cụm
7. `/statistics` -> Kết quả kiểm định thống kê Mann-Whitney U, Chi-Square, bảng tham số phân phối giá trị hóa đơn
8. `*` -> Màn hình 404 Not Found điều hướng an toàn

---

## 4. API Services & Backend Mapping
| Service File | Endpoint Backend | Mục đích | Phương thức |
| :--- | :--- | :--- | :---: |
| `api.ts` | `/health` | Kiểm tra nhịp tim backend | GET |
| `dashboardApi.ts` | `/dashboard/summary` | 4 chỉ số cốt lõi KPI | GET |
| `dashboardApi.ts` | `/dashboard/revenue-trend` | Chuỗi doanh thu 13 tháng | GET |
| `dashboardApi.ts` | `/dashboard/top-products` | Top 10 sản phẩm doanh thu cao nhất | GET |
| `dashboardApi.ts` | `/dashboard/top-countries` | Top 10 quốc gia doanh thu lớn nhất | GET |
| `salesApi.ts` | `/sales/monthly` | Cơ cấu doanh thu theo tháng (kèm lọc năm) | GET |
| `salesApi.ts` | `/sales/countries` | Tỷ trọng đóng góp doanh thu theo quốc gia | GET |
| `salesApi.ts` | `/sales/products` | Danh mục 3,938 mặt hàng (phân trang + tìm kiếm) | GET |
| `salesApi.ts` | `/sales/invoices` | Sổ cái 23,796 hóa đơn (phân trang + lọc trạng thái) | GET |
| `customersApi.ts` | `/customers` | 4,371 khách hàng kèm RFM (phân trang + lọc đa chiều) | GET |
| `customersApi.ts` | `/customers/{id}` | Hồ sơ phân tích chi tiết của 1 khách hàng | GET |
| `segmentationApi.ts` | `/segmentation/summary` | Chỉ số trung bình R-F-M của 3 cụm K-Means | GET |
| `segmentationApi.ts` | `/segmentation/clusters/{id}`| Chi tiết cụm K-Means cụ thể | GET |
| `segmentationApi.ts` | `/segmentation/evaluation` | Chỉ số Elbow (Inertia) và Silhouette score | GET |
| `statisticsApi.ts` | `/statistics/tests` | Kết quả kiểm định Mann-Whitney U & Chi-Square | GET |
| `statisticsApi.ts` | `/statistics/invoice-value-summary` | Bảng thống kê mô tả phân phối đơn hàng | GET |

---

## 5. Danh mục Thành phần Giao diện (Components)
- **Cards (2 components):** `MetricCard`, `ChartCard`
- **Charts (7 components):** `RevenueTrendChart`, `TopCountriesChart`, `TopProductsChart`, `SegmentDistributionChart`, `MonthlyBreakdownChart`, `ClusterComparisonChart`, `KMeansEvaluationChart`
- **Common (6 components):** `Badge`, `EmptyState`, `ErrorState`, `LoadingState`, `PageHeader`, `Pagination`
- **Layout (3 components):** `AppLayout`, `Header`, `Sidebar`
- **Tables (1 component):** `DataTable` (Generic typed component với horizontal scroll và custom column renderers)

---

## 6. Kiểm tra Dữ liệu Mock, Debug Code & Bảo mật
- **Mock Data Audit:**
  - Không tìm thấy bất kỳ dữ liệu fake/mock/dummy nào trong `src/`. Toàn bộ dữ liệu hiển thị đều được gọi động từ Backend MongoDB qua Axios.
- **Debug Code Audit:**
  - Không còn `TODO`, `FIXME`, `debugger` hoặc `console.log`.
  - Chỉ duy nhất 1 dòng `console.error` trong `src/services/api.ts` đã được bọc bảo vệ bởi `import.meta.env.DEV` (chỉ log khi chạy môi trường dev).
- **Security Audit:**
  - Không chứa mật khẩu, private key, token, connection string MongoDB (`mongodb://`).
  - Biến môi trường chỉ sử dụng `VITE_API_BASE_URL` định danh URL endpoint API.

---

## 7. Phân loại Toàn bộ Files (Audit Classification)

### [KEEP] — Mã nguồn chính thức cần giữ lại và bảo đảm hoạt động
- `frontend/package.json` — Cấu hình dependencies và build scripts.
- `frontend/package-lock.json` — Lockfile bảo đảm tái tạo dependency chính xác.
- `frontend/vite.config.ts` — Cấu hình Vite bundler + Tailwind v4 + React plugin.
- `frontend/tsconfig.json`, `frontend/tsconfig.app.json`, `frontend/tsconfig.node.json` — Cấu hình TypeScript compiler.
- `frontend/.oxlintrc.json` — Cấu hình bộ kiểm tra cú pháp linter.
- `frontend/index.html` — Điểm gắn kết DOM của Single Page App.
- `frontend/nginx.conf` — Máy chủ Nginx phục vụ production và reverse proxy.
- `frontend/Dockerfile` — Đóng gói Docker multi-stage container.
- `frontend/.dockerignore` — Loại trừ thư mục không cần build vào Docker.
- `frontend/.env`, `frontend/.env.example` — Cấu hình base URL của API.
- `frontend/.gitignore` — Quy định bỏ qua `node_modules`, `dist`.
- `frontend/README.md` — Hướng dẫn cài đặt và sử dụng frontend.
- `frontend/public/favicon.svg` — Biểu tượng ứng dụng trên tab trình duyệt.
- `frontend/src/main.tsx` — Khởi tạo React root.
- `frontend/src/App.tsx` — Nạp router chính.
- `frontend/src/index.css` — CSS toàn cục: font Inter, focus outline, sleek scrollbar.
- `frontend/src/routes/index.tsx` — Cấu hình toàn bộ định tuyến với lazy load.
- `frontend/src/components/cards/*` (2 files + barrel index)
- `frontend/src/components/charts/*` (7 files + barrel index)
- `frontend/src/components/common/*` (6 files + barrel index)
- `frontend/src/components/layout/*` (3 files)
- `frontend/src/components/tables/*` (1 file + barrel index)
- `frontend/src/hooks/*` (5 files)
- `frontend/src/pages/*` (7 files qua 6 thư mục con)
- `frontend/src/services/*` (6 files)
- `frontend/src/types/*` (6 files)
- `frontend/src/utils/*` (3 files)

### [BUG] — Không phát hiện bug blocker (P0) trong Phase 1
- Toàn bộ contract API và router đã ánh xạ chính xác với backend Swagger.

### [UNUSED] — File thừa không được sử dụng
- `frontend/public/icons.svg` — Chứa các symbol SVG (bluesky, discord, documentation, github, social, x) thừa từ template khởi tạo Vite ban đầu, không được tham chiếu ở bất kỳ đâu trong `src/`.
- `frontend/src/assets/` — Thư mục trống rỗng (các ảnh mẫu ban đầu đã được dọn sạch).

### [DUPLICATE] — Thành phần trùng lặp
- `TopProductItem` (`src/types/dashboard.ts`) và `ProductSalesItem` (`src/types/sales.ts`): Có cấu trúc thuộc tính giống nhau 100%. (Tuy nhiên việc giữ riêng theo domain API Dashboard và Sales vẫn hợp lệ theo kiến trúc phân tách domain).
- `TopCountryItem` (`src/types/dashboard.ts`) và `CountrySalesItem` (`src/types/sales.ts`): Có cấu trúc thuộc tính giống nhau 100%.

### [REVIEW] — Cần xem xét / bổ sung ở các phase tiếp theo
1. **Kiểm thử tự động (Unit Tests):** Hiện tại project chưa có thư viện kiểm thử tự động frontend (Vitest / React Testing Library) trong `devDependencies`. Có thể bổ sung bộ test tối thiểu theo yêu cầu Phase 31 khi chuyển sang các phase sau.
2. **Loại bỏ file dư thừa `public/icons.svg`:** Có thể xóa bỏ an toàn ở Phase 8 (Cleanup) để giảm dung lượng bundle tĩnh.

---

## 8. Kết luận Phase 1 Audit
- Mã nguồn hiện tại được tổ chức chặt chẽ, tuân thủ nguyên tắc kiến trúc phân tầng (components, hooks, services, types, utils, pages).
- Không có mã giả lập (mock data) hay rò rỉ thông tin bảo mật.
- Sẵn sàng chuyển giao sang **PHASE 2 — DEPENDENCY CHECK & COMPILATION TEST** khi có chỉ đạo.
