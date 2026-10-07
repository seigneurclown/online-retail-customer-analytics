import { apiClient } from './api';
import type {
  CustomerListItem,
  CustomerDetailResponse,
  CustomerFilterParams,
} from '../types/customer';
import type { PaginatedResponse } from '../types/common';

export const customersApi = {
  getCustomers: async (
    params?: CustomerFilterParams
  ): Promise<PaginatedResponse<CustomerListItem>> => {
    const response = await apiClient.get<PaginatedResponse<CustomerListItem>>('/customers', {
      params,
    });
    return response.data;
  },

  getCustomerById: async (customerId: string): Promise<CustomerDetailResponse> => {
    const response = await apiClient.get<CustomerDetailResponse>(`/customers/${encodeURIComponent(customerId)}`);
    return response.data;
  },
};
