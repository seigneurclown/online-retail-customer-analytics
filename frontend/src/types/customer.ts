/**
 * Customer & RFM TypeScript Contract
 */
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

export interface CustomerFilterParams {
  page?: number;
  page_size?: number;
  cluster?: number;
  membership_tier?: string;
  country?: string;
  min_recency?: number;
  max_recency?: number;
  min_frequency?: number;
  max_frequency?: number;
  min_monetary?: number;
  max_monetary?: number;
  search?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}
