/**
 * Sales APIs TypeScript Contract
 */
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

export interface InvoiceFilterParams {
  page?: number;
  page_size?: number;
  country?: string;
  is_cancelled?: boolean;
  min_value?: number;
  max_value?: number;
  search?: string;
}
