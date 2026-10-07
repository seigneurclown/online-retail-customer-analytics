import { apiClient } from './api';
import type {
  StatisticalTestItem,
  InvoiceValueSummaryItem,
} from '../types/statistics';

export const statisticsApi = {
  getTests: async (): Promise<StatisticalTestItem[]> => {
    const response = await apiClient.get<StatisticalTestItem[]>('/statistics/tests');
    return response.data;
  },

  getInvoiceValueSummary: async (): Promise<InvoiceValueSummaryItem[]> => {
    const response = await apiClient.get<InvoiceValueSummaryItem[]>('/statistics/invoice-value-summary');
    return response.data;
  },
};
