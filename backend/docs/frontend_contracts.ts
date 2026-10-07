/**
 * ==============================================================================
 * FRONTEND CONTRACT: TYPESCRIPT INTERFACES FOR REACT FRONTEND
 * Online Retail Analytics Platform
 * ==============================================================================
 * File định nghĩa kiểu dữ liệu chuẩn (Type Definitions) giúp team Frontend (React + TypeScript)
 * có thể copy trực tiếp vào dự án React để gọi API an toàn và có auto-completion 100%.
 */

// --- 1. Cấu trúc Phân trang chung (Pagination Contract) ---
export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

// --- 2. Dashboard APIs Contract ---
export interface DashboardSummaryResponse {
  total_revenue: number;        // Ví dụ: 8291748.56 (£)
  total_orders: number;         // Ví dụ: 19960 đơn
  total_customers: number;      // Ví dụ: 4317 khách
  average_order_value: number;  // Ví dụ: 533.17 (£)
}

export interface RevenueTrendItem {
  year_month: string;           // "YYYY-MM" (VD: "2010-12")
  revenue: number;              // Net revenue (£)
}

export interface RevenueTrendResponse {
  items: RevenueTrendItem[];
}

export interface TopProductItem {
  stock_code: string;
  description: string | null;
  total_revenue: number;
  total_quantity: number;
  order_count: number;
}

export interface TopCountryItem {
  country: string;
  total_revenue: number;
  invoice_count: number;
  customer_count: number;
  percentage_share: number;
}

// --- 3. Sales APIs Contract ---
export interface MonthlySalesItem {
  year_month: string;
  gross_revenue: number;
  cancelled_revenue: number;
  net_revenue: number;
  invoice_count: number;
  total_quantity: number;
}

export interface ProductSalesItem {
  stock_code: string;
  description: string | null;
  total_revenue: number;
  total_quantity: number;
  order_count: number;
}

export interface CountrySalesItem {
  country: string;
  total_revenue: number;
  invoice_count: number;
  customer_count: number;
  percentage_share: number;
}

export interface InvoiceItem {
  invoice_no: string;
  invoice_date: string;
  customer_id: string | null;
  country: string;
  is_cancelled: boolean;
  invoice_value: number;
  total_quantity: number;
  item_count: number;
}

// --- 4. Customer & RFM APIs Contract ---
export interface CustomerListItem {
  customer_id: string;
  countries: string[];
  recency: number | null;
  frequency: number | null;
  monetary: number | null;
  cluster: number | null;
  membership_tier: string | null;
}

export interface CustomerDetailResponse {
  customer_id: string;
  countries: string[];
  recency: number;
  frequency: number;
  monetary: number;
  cluster: number;
  membership_tier: string;
}

// --- 5. Segmentation APIs Contract ---
export interface ClusterSummaryItem {
  cluster: number;
  membership_tier: string;
  customer_count: number;
  customer_pct: number;
  recency_mean: number;
  recency_median: number;
  frequency_mean: number;
  frequency_median: number;
  monetary_mean: number;
  monetary_median: number;
  total_monetary: number;
  revenue_share_pct: number;
}

export interface KMeansEvaluationItem {
  k: number;
  inertia: number;
  silhouette_score: number;
}

// --- 6. Statistics APIs Contract ---
export interface StatisticalTestItem {
  id: number;
  research_question: string;
  test_name: string;
  reason: string;
  test_statistic: string;
  p_value: number | null;
  significance_level: string;
  conclusion: string;
}

export interface InvoiceValueSummaryItem {
  metric: string;
  value: number;
}
