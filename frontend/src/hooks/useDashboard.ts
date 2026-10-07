import { useState, useEffect, useCallback } from 'react';
import { dashboardApi } from '../services/dashboardApi';
import { segmentationApi } from '../services/segmentationApi';
import type {
  DashboardSummaryResponse,
  RevenueTrendItem,
  TopProductItem,
  TopCountryItem,
} from '../types/dashboard';
import type { ClusterSummaryItem } from '../types/segmentation';

export interface DashboardData {
  summary: DashboardSummaryResponse | null;
  revenueTrend: RevenueTrendItem[];
  topProducts: TopProductItem[];
  topCountries: TopCountryItem[];
  segments: ClusterSummaryItem[];
}

export function useDashboard() {
  const [data, setData] = useState<DashboardData>({
    summary: null,
    revenueTrend: [],
    topProducts: [],
    topCountries: [],
    segments: [],
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [summaryRes, trendRes, productsRes, countriesRes, segmentsRes] =
        await Promise.all([
          dashboardApi.getSummary(),
          dashboardApi.getRevenueTrend(),
          dashboardApi.getTopProducts(10),
          dashboardApi.getTopCountries(10),
          segmentationApi.getSummary(),
        ]);

      setData({
        summary: summaryRes,
        revenueTrend: trendRes.items || [],
        topProducts: productsRes || [],
        topCountries: countriesRes || [],
        segments: segmentsRes || [],
      });
    } catch (err: unknown) {
      const message =
        err instanceof Error
          ? err.message
          : 'Failed to fetch dashboard metrics. Please check backend connection.';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let ignore = false;

    async function loadInitial() {
      try {
        const [summaryRes, trendRes, productsRes, countriesRes, segmentsRes] =
          await Promise.all([
            dashboardApi.getSummary(),
            dashboardApi.getRevenueTrend(),
            dashboardApi.getTopProducts(10),
            dashboardApi.getTopCountries(10),
            segmentationApi.getSummary(),
          ]);

        if (!ignore) {
          setData({
            summary: summaryRes,
            revenueTrend: trendRes.items || [],
            topProducts: productsRes || [],
            topCountries: countriesRes || [],
            segments: segmentsRes || [],
          });
          setLoading(false);
        }
      } catch (err: unknown) {
        if (!ignore) {
          const message =
            err instanceof Error
              ? err.message
              : 'Failed to fetch dashboard metrics. Please check backend connection.';
          setError(message);
          setLoading(false);
        }
      }
    }

    loadInitial();

    return () => {
      ignore = true;
    };
  }, []);

  return {
    ...data,
    loading,
    error,
    refetch: fetchDashboardData,
  };
}
