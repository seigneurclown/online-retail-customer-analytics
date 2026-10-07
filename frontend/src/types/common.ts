/**
 * Common Types & Pagination Contract
 */
export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface ApiErrorResponse {
  detail: string | Array<{ loc: (string | number)[]; msg: string; type: string }>;
}
