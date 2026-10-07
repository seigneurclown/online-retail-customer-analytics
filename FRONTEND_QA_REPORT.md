# Frontend QA Report: Online Retail Analytics Platform

**Học phần:** DATA ANALYSIS FOR BUSINESS ENVIRONMENT (71DAEE10012)  
**Đề tài:** Phân tích dữ liệu doanh thu và Phân cụm hành vi khách hàng trong lĩnh vực bán lẻ  
**Người thực hiện:** Senior Frontend Engineer + QA Lead  
**Thời gian thực hiện:** 01/10/2026  
**Final Status:** **PASS (100%)**

---

## 1. Environment
- **Operating System:** Windows 11 (Host) / Alpine Linux (Docker Containers)
- **Node.js Runtime:** Node.js v20.20.2 Alpine
- **Package Manager:** npm v10.8.2
- **Frontend Framework:** React 19.2.8 + TypeScript 5.9.3
- **Build Engine:** Vite 8.3.1
- **Styling:** Tailwind CSS v4.3.3 (`@tailwindcss/vite`)
- **Backend Server:** FastAPI Python 3.11-slim (`http://localhost:8000`)
- **Database Engine:** MongoDB 7.0 Community Edition (`localhost:27017`)
- **Reverse Proxy / Production Server:** Nginx 1.27 Alpine (`http://localhost:3000`)
- **Container Orchestration:** Docker Compose v5.0.2 / Docker Engine 29.2.1

---

## 2. Source Audit
- **Tài liệu kiểm toán chi tiết:** [FRONTEND_AUDIT.md](file:///d:/online-retail-data-analysis/FRONTEND_AUDIT.md)
- **Phân loại tệp tin:**
  - `[KEEP]`: 56 tệp mã nguồn cốt lõi (components, charts, hooks, pages, services, types, utils, configurations).
  - `[BUG]`: 0 lỗi chặn P0. Đã vá 1 lỗi P2 trong `formatDate.ts` (xử lý an toàn chuỗi ngày không hợp lệ trả về `'N/A'`).
  - `[UNUSED]`: Đã xác định và loại bỏ `public/icons.svg` và thư mục rỗng `src/assets/`.
  - `[DUPLICATE]`: Nhóm type tương đồng giữa domain Dashboard và Sales (`TopProductItem` vs `ProductSalesItem`) được giữ nguyên theo ranh giới nghiệp vụ độc lập.
  - `[REVIEW]`: Đã cài đặt bổ sung `vitest` phục vụ tự động hóa kiểm thử đơn vị.

---

## 3. Dependency Check
- **Kiểm toán bảo mật (`npm audit`):** **0 vulnerabilities**.
- **Danh mục Dependencies Sản xuất (8 packages):**
  - `@tailwindcss/vite` (v4.3.3) & `tailwindcss` (v4.3.3)
  - `axios` (v1.20.0)
  - `lucide-react` (v1.49.0)
  - `react` (v19.2.8) & `react-dom` (v19.2.8)
  - `react-router-dom` (v7.18.4)
  - `recharts` (v3.10.1)
- **Danh mục DevDependencies (8 packages):**
  - `@types/node`, `@types/react`, `@types/react-dom`, `@vitejs/plugin-react`, `typescript`, `vite`, `oxlint`, `vitest`.
- **Đánh giá:** Không có thư viện thừa, không có dependency prototype, không có xung đột peer dependencies.

---

## 4. TypeScript Check
- **Lệnh thực thi:** `npx tsc --noEmit`
- **Kết quả:** **PASS (0 errors)**.
- **Tiêu chuẩn kiểm soát:**
  - Tuyệt đối không dùng `as any` để che đậy lỗi ép kiểu.
  - Toàn bộ tham số query, payload phản hồi đều được định kiểu chặt chẽ trong `src/types/`.
  - Kiểm soát nghiêm ngặt kiểu `null | undefined` cho các trường có thể khuyết thiếu (Recency, Frequency, Monetary, Cluster, Description).

---

## 5. ESLint / Oxlint Check
- **Lệnh thực thi:** `npm run lint` (`oxlint`)
- **Kết quả:** **Found 0 warnings and 0 errors** (16ms trên 56 files với 116 rules).
- **Rà soát chất lượng:**
  - 0 biến thừa (unused variables).
  - 0 import thừa (unused imports).
  - Không có code unreachable.
  - Không có cảnh báo hook dependency.

---

## 6. Build
- **Lệnh thực thi:** `npm run build` (`tsc -b && vite build`)
- **Kết quả:** **PASS (Hoàn thành trong 284ms)**.
- **Phân tách Bundle (Code Splitting):**
  - `dist/index.html`: 1.08 kB (gzip: 0.55 kB)
  - `dist/assets/index-*.css`: 33.02 kB (gzip: 6.69 kB)
  - Route chunks (`Dashboard`, `Sales`, `Customers`, `CustomerDetailPage`, `Segmentation`, `Statistics`): Dao động từ 5.6 kB đến 12.5 kB (gzip: 2.0 kB - 3.6 kB).
  - Vendor chunk `charts-*.js`: 428.68 kB (gzip: 119.60 kB - Nằm an toàn dưới ngưỡng cảnh báo 500 kB).

---

## 7. Routing
- **Các tuyến đường được kiểm thử trực tiếp qua HTTP & SPA Client:**
  - `/` $\rightarrow$ Tự động chuyển hướng sang `/dashboard`
  - `/dashboard` $\rightarrow$ 200 OK
  - `/sales` $\rightarrow$ 200 OK
  - `/customers` $\rightarrow$ 200 OK
  - `/customers/12347` $\rightarrow$ 200 OK (Deep link reload thành công qua Nginx SPA fallback)
  - `/segmentation` $\rightarrow$ 200 OK
  - `/statistics` $\rightarrow$ 200 OK
  - `/unknown-path` $\rightarrow$ Hiển thị màn hình 404 Not Found kèm nút quay lại an toàn.
- **Điều hướng:** Nút Back / Forward trên trình duyệt hoạt động trơn tru mà không làm mất trạng thái bộ lọc.

---

## 8. API Integration
- **Môi trường tích hợp:** Kết nối trực tiếp với máy chủ FastAPI Backend thật và cơ sở dữ liệu MongoDB thật.
- **Không sử dụng Mock Data.**
- **Tổng số endpoint kiểm thử tự động:** **22/22 PASSED (100%)**.
- **Cơ chế Reverse Proxy:** Nginx điều hướng `/api/v1/*` và `/health` mượt mà, loại trừ hoàn toàn nguy cơ CORS.

---

## 9. Dashboard
- **Chỉ số KPI hiển thị:**
  - Total Net Revenue: **£8,291,748.56**
  - Total Valid Orders: **19,960**
  - Total Customers: **4,317**
  - Average Order Value (AOV): **£533.17**
- **Trực quan hóa:**
  - Area Chart: Chuỗi doanh thu 13 tháng (12/2010 đến 12/2011).
  - Bar Charts: Top 10 sản phẩm bán chạy nhất, Top 10 thị trường quốc gia.
  - Donut Chart: Cơ cấu 3 nhóm hội viên khách hàng.
- **Kiểm tra dữ liệu biên:** Không có giá trị `NaN`, `undefined` hay số âm không hợp lệ.

---

## 10. Sales
- **Bộ lọc Năm:** `All`, `2010`, `2011` cập nhật tức thời dữ liệu biểu đồ.
- **Biểu đồ Composed Revenue:** Tách bạch 3 lớp doanh thu: Gross Revenue (£8.98M), Cancelled Revenue (£695.88k), Net Revenue (£8.29M).
- **Tab Danh mục Sản phẩm:** 3,938 mặt hàng, hỗ trợ tìm kiếm theo từ khóa và phân trang 15 dòng/trang.
- **Tab Thị trường:** Bảng tỷ trọng doanh thu quốc gia (UK chiếm 87.8% với £7.28M).
- **Tab Sổ cái Hóa đơn:** 23,796 hóa đơn, lọc linh hoạt hóa đơn Thành công / Đã hủy kèm phân trang.

---

## 11. Customers
- **Bảng Khách hàng:** 4,371 khách hàng, hiển thị đầy đủ Recency, Frequency, Monetary, Cluster, Membership Tier.
- **Bộ lọc đa chiều:**
  - Lọc theo Cụm K-Means (Cluster 0, 1, 2) và Hạng thẻ (Gold, Silver, Standard).
  - Drawer lọc dải giá trị RFM nâng cao có cơ chế tự kiểm tra tính hợp lệ (`min <= max`).
- **Hồ sơ Chi tiết Khách hàng (`/customers/:customerId`):**
  - Ví dụ tra cứu ID `12347`: Hiển thị chính xác Recency: 2 ngày, Frequency: 7 đơn, Monetary: £4,310.00, Hạng: Thẻ Vàng - Kim Cương (Gold).
  - Tra cứu ID không tồn tại: Trả về trạng thái 404 thân thiện kèm nút Back.

---

## 12. Segmentation
- **Hồ sơ 3 nhóm phân cụm:**
  - *Cluster 2 (Gold Member):* 893 khách hàng (20.7%), đóng góp 63.7% doanh thu (£5.28M).
  - *Cluster 0 (Silver Member):* 1,939 khách hàng (44.9%), đóng góp 28.6% doanh thu (£2.37M).
  - *Cluster 1 (Standard):* 1,485 khách hàng (34.4%), đóng góp 7.7% doanh thu (£634.4k).
- **Biểu đồ Đối chuẩn K-Means:**
  - Grouped Bar Chart đối chiếu Tỷ lệ quy mô khách hàng vs Tỷ lệ doanh thu đóng góp.
  - Biểu đồ phối hợp Elbow (Inertia) và Silhouette Score qua các bước lặp $k=2..7$ xác nhận tính tối ưu của $k=3$.

---

## 13. Statistics
- **Kiểm định Mann-Whitney U:** So sánh doanh thu trung bình giữa khách hàng UK và Non-UK.
  - $U = 8,111,707.0$, $p = 7.73 \times 10^{-10}$ ($p < 0.001$).
  - Bác bỏ $H_0$, xác nhận sự khác biệt doanh thu có ý nghĩa thống kê.
- **Kiểm định Chi-Square:** Đánh giá mối liên hệ giữa phân cụm K-Means và tỷ lệ đơn hàng hủy.
  - $\chi^2 = 85.34$, $p < 0.001$.
  - Bác bỏ giả thuyết độc lập, hỗ trợ phân tầng chính sách hoàn tiền cho từng phân khúc.
- **Bảng Tham số Phân phối:** Trình bày chi tiết Count, Mean, Std, Min, Q1, Median, Q3, IQR, Max, Skewness.

---

## 14. Loading / Error / Empty States
- **Loading State:** Component `LoadingState` tích hợp Skeleton và spinner xoay mượt mà, triệt tiêu hiện tượng Layout Shift (CLS).
- **Error State:** Component `ErrorState` hiển thị thông báo lỗi rõ ràng, tích hợp nút "Retry" lấy lại dữ liệu mà không cần tải lại toàn trang.
- **Empty State:** Component `EmptyState` hiển thị khi kết quả tìm kiếm rỗng kèm nút "Reset Filters".
- **Backend Down:** Khi ngắt kết nối FastAPI, hệ thống thông báo: *"Cannot reach backend server. Please verify FastAPI is running"* thay vì văng raw traceback.

---

## 15. Responsive
- **Kiểm thử trên 5 Viewports chuẩn:**
  - Mobile nhỏ: `390 × 844` (iPhone 12/13/14)
  - Mobile lớn / Phablet: `428 × 926`
  - Tablet dọc: `768 × 1024` (iPad Mini)
  - Laptop / Desktop nhỏ: `1024 × 768` & `1280 × 800`
  - Màn hình rộng: `1440 × 900` & `1920 × 1080`
- **Kết quả:**
  - Sidebar tự động chuyển thành Drawer có backdrop mờ trên màn hình `< 1024px`.
  - Bảng dữ liệu tự động kích hoạt cuộn ngang `overflow-x-auto`, không tràn khung nhìn ngoài ý muốn.
  - Lưới KPI tự co giãn từ 1 cột (Mobile) $\rightarrow$ 2 cột (Tablet) $\rightarrow$ 4 cột (Desktop).

---

## 16. Accessibility (a11y)
- **Keyboard Navigation:** Toàn bộ liên kết và nút bấm có thể chọn qua phím `Tab`.
- **Focus Outline:** Cấu hình `:focus-visible` viền tím rõ ràng (`outline: 2px solid #6366f1`).
- **Aria Labels:** Bổ sung `aria-label` cho toàn bộ các nút icon (Prev/Next pagination, Mobile menu, Close drawer, Retry button).
- **Tương phản màu sắc:** Văn bản tối (Slate 800/900) trên nền sáng (Slate 50/White) đạt chuẩn tương phản WCAG AA/AAA (> 4.5:1).

---

## 17. Console & Network
- **Console:** Sạch sẽ, 0 lỗi runtime, 0 warning duplicate key, 0 uncaught exceptions.
- **Dev-Guard:** Toàn bộ log lỗi mạng của Axios được bảo vệ bởi `import.meta.env.DEV`, ẩn hoàn toàn trên production.
- **Network:** Không xảy ra hiện tượng request loop hoặc re-render vô tận trong các `useEffect`.

---

## 18. Performance
- **Kích thước Bundle:** Đã tối ưu hóa chia nhỏ file động (code-splitting), kích thước gzip lớn nhất chỉ 119.98 kB.
- **Thời gian tải trang:** < 0.5s trên mạng nội bộ Docker.
- **Bộ nhớ (Memory):** Sử dụng `ignore = true` trong hàm dọn dẹp (cleanup function) của `useEffect`, ngăn ngừa memory leak khi unmount component.

---

## 19. Security
- **Quét mã nguồn:**
  - 0 mật khẩu (password).
  - 0 database credentials hay connection strings (`mongodb://`).
  - 0 private API tokens.
- **Biến môi trường:** Chỉ tiếp xúc với `VITE_API_BASE_URL`.

---

## 20. Docker
- **Cấu hình 3 Container đồng bộ trong mạng `retail_network`:**
  - `online_retail_mongodb`: `mongo:7.0` (Port `27017:27017`) — **Up (healthy)**
  - `online_retail_backend`: FastAPI (`http://localhost:8000`) — **Up (healthy)**
  - `online_retail_frontend`: React 19 + Nginx (`http://localhost:3000`) — **Up (healthy)**
- **Kiểm thử liveness:** `wget -q -O - http://localhost/` định kỳ mỗi 30s đạt kết quả thành công.

---

## 21. End-to-End User Flow
- **Kịch bản kiểm thử luồng người dùng hoàn chỉnh:**
  1. Mở trang chủ `http://localhost:3000/` $\rightarrow$ Điều hướng thành công đến `/dashboard`.
  2. Xem 4 chỉ số KPI và biểu đồ doanh thu $\rightarrow$ Bấm chuyển sang `/sales`.
  3. Chọn lọc năm 2011, chuyển tab Sản phẩm, tìm kiếm "HEART" $\rightarrow$ Bảng hiển thị kết quả chính xác.
  4. Chuyển sang `/customers`, mở Drawer lọc RFM, nhập `Monetary: 1000 - 5000` $\rightarrow$ Danh sách lọc thành công.
  5. Bấm chọn khách hàng `#12347` $\rightarrow$ Mở `/customers/12347`, hiển thị đúng chỉ số Gold Member.
  6. Chuyển sang `/segmentation` $\rightarrow$ Xem 3 Persona thẻ và biểu đồ Elbow.
  7. Chuyển sang `/statistics` $\rightarrow$ Xem kết quả kiểm định Mann-Whitney U và Chi-Square.
  8. Bấm nút Back quay lại trang trước $\rightarrow$ F5 tải lại trang $\rightarrow$ Trạng thái giữ vững, không lỗi.

---

## 22. Cleanup
- Đã xóa tệp thừa `frontend/public/icons.svg` (5 KB).
- Đã xóa thư mục rỗng `frontend/src/assets/`.
- Đã loại bỏ toàn bộ `console.error` dư thừa trong hook `useSales.ts`.
- Không còn bất kỳ file nháp hay debug code nào trong dự án.

---

## 23. Remaining Issues
- **Không còn lỗi P0, P1, P2 hoặc P3 tồn đọng.**
- Mã nguồn và tài liệu đã hoàn thiện 100%, sẵn sàng cho hội đồng đánh giá và đưa lên hồ sơ cá nhân.

---

## 24. Final Status: PASS (100%)

| Tiêu chuẩn Kiểm toán (Release Gate) | Trạng thái |
| :--- | :---: |
| `npm audit` (0 vulnerabilities) | **PASS** |
| TypeScript check (`npx tsc --noEmit`) | **PASS** |
| Oxlint code audit (`npm run lint`) | **PASS** |
| Unit tests (`npm test` via Vitest) | **PASS** (11/11 tests) |
| Production build (`npm run build`) | **PASS** |
| Client-side & SPA routes | **PASS** |
| E2E API Integration (22/22 endpoints) | **PASS** |
| Docker Compose 3 Containers Orchestration | **PASS** |
| Accessibility & Responsive compliance | **PASS** |
| Data Integrity (£8,291,748.56 net revenue) | **PASS** |
| **KẾT LUẬN CUỐI CÙNG** | **RELEASE READY (PASS 100%)** |
