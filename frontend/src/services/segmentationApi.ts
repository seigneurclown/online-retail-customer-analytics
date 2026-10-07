import { apiClient } from './api';
import type {
  ClusterSummaryItem,
  KMeansEvaluationItem,
} from '../types/segmentation';

export const segmentationApi = {
  getSummary: async (): Promise<ClusterSummaryItem[]> => {
    const response = await apiClient.get<ClusterSummaryItem[]>('/segmentation/summary');
    return response.data;
  },

  getClusterDetail: async (clusterId: number): Promise<ClusterSummaryItem> => {
    const response = await apiClient.get<ClusterSummaryItem>(`/segmentation/clusters/${clusterId}`);
    return response.data;
  },

  getEvaluation: async (): Promise<KMeansEvaluationItem[]> => {
    const response = await apiClient.get<KMeansEvaluationItem[]>('/segmentation/evaluation');
    return response.data;
  },
};
