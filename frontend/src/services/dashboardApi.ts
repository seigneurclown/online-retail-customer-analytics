import { apiClient } from './api';
import type {
  DashboardSummaryResponse,
  RevenueTrendResponse,
  TopProductItem,
  TopCountryItem,
} from '../types/dashboard';

export const dashboardApi = {
  getSummary: async (): Promise<DashboardSummaryResponse> => {
    const response = await apiClient.get<DashboardSummaryResponse>('/dashboard/summary');
    return response.data;
  },

  getRevenueTrend: async (): Promise<RevenueTrendResponse> => {
    const response = await apiClient.get<RevenueTrendResponse>('/dashboard/revenue-trend');
    return response.data;
  },

  getTopProducts: async (limit: number = 10): Promise<TopProductItem[]> => {
    const response = await apiClient.get<TopProductItem[]>('/dashboard/top-products', {
      params: { limit },
    });
    return response.data;
  },

  getTopCountries: async (limit: number = 10): Promise<TopCountryItem[]> => {
    const response = await apiClient.get<TopCountryItem[]>('/dashboard/top-countries', {
      params: { limit },
    });
    return response.data;
  },
};
