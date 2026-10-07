import { apiClient } from './api';
import type {
  MonthlySalesItem,
  ProductSalesItem,
  CountrySalesItem,
  InvoiceItem,
  InvoiceFilterParams,
} from '../types/sales';
import type { PaginatedResponse } from '../types/common';

export const salesApi = {
  getMonthlySales: async (year?: number): Promise<MonthlySalesItem[]> => {
    const response = await apiClient.get<MonthlySalesItem[]>('/sales/monthly', {
      params: { year },
    });
    return response.data;
  },

  getProducts: async (
    page: number = 1,
    pageSize: number = 20,
    search?: string
  ): Promise<PaginatedResponse<ProductSalesItem>> => {
    const response = await apiClient.get<PaginatedResponse<ProductSalesItem>>('/sales/products', {
      params: { page, page_size: pageSize, search },
    });
    return response.data;
  },

  getCountries: async (
    page: number = 1,
    pageSize: number = 20,
    search?: string
  ): Promise<PaginatedResponse<CountrySalesItem>> => {
    const response = await apiClient.get<PaginatedResponse<CountrySalesItem>>('/sales/countries', {
      params: { page, page_size: pageSize, search },
    });
    return response.data;
  },

  getInvoices: async (params?: InvoiceFilterParams): Promise<PaginatedResponse<InvoiceItem>> => {
    const response = await apiClient.get<PaginatedResponse<InvoiceItem>>('/sales/invoices', {
      params,
    });
    return response.data;
  },
};
