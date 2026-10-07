/**
 * Dashboard APIs TypeScript Contract
 */
export interface DashboardSummaryResponse {
  total_revenue: number;
  total_orders: number;
  total_customers: number;
  average_order_value: number;
}

export interface RevenueTrendItem {
  year_month: string;
  revenue: number;
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
