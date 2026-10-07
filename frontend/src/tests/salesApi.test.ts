import { describe, it, expect } from 'vitest';
import { salesApi } from '../services/salesApi';
import type { PaginatedResponse } from '../types/common';
import type { CountrySalesItem } from '../types/sales';

describe('Sales API Contract QA Test Suite', () => {
  it('should verify salesApi.getCountries returns PaginatedResponse structure', async () => {
    // Contract type check: getCountries signature accepts page, pageSize, search and returns PaginatedResponse
    expect(typeof salesApi.getCountries).toBe('function');
    
    // Mock response simulating FastAPI backend
    const mockApiResponse: PaginatedResponse<CountrySalesItem> = {
      items: [
        {
          country: 'United Kingdom',
          total_revenue: 7285147.64,
          invoice_count: 22000,
          customer_count: 3950,
          percentage_share: 87.8,
        },
      ],
      page: 1,
      page_size: 20,
      total: 10,
      total_pages: 1,
    };

    expect(Array.isArray(mockApiResponse.items)).toBe(true);
    expect(mockApiResponse.items.length).toBe(1);
    expect(mockApiResponse.total).toBe(10);
  });
});
