import { apiClient } from './api';

export interface SystemStatus {
  connected: boolean;
  database_name: string;
  has_seed_files: boolean;
  total_records: number;
  collections: Record<string, number>;
  error?: string;
}

export interface SeedResult {
  status: string;
  message: string;
  duration_seconds?: number;
  total_inserted?: number;
  summary?: Record<string, number>;
}

export const systemApi = {
  getStatus: async (): Promise<SystemStatus> => {
    const response = await apiClient.get<SystemStatus>('/system/status');
    return response.data;
  },

  seedDatabase: async (): Promise<SeedResult> => {
    const response = await apiClient.post<SeedResult>('/system/seed', {}, {
      timeout: 90000, // 90 giây cho thao tác nạp dữ liệu đám mây
    });
    return response.data;
  },

  uploadCsv: async (file: File, collectionType: string): Promise<{ status: string; message: string; details: any }> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('collection_type', collectionType);

    const response = await apiClient.post('/system/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 90000,
    });
    return response.data;
  },
};
