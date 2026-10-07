import { useState, useEffect, useCallback } from 'react';
import { segmentationApi } from '../services/segmentationApi';
import type { ClusterSummaryItem, KMeansEvaluationItem } from '../types/segmentation';

export function useSegmentation() {
  const [clusters, setClusters] = useState<ClusterSummaryItem[]>([]);
  const [evaluation, setEvaluation] = useState<KMeansEvaluationItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchSegmentationData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [summaryRes, evalRes] = await Promise.all([
        segmentationApi.getSummary(),
        segmentationApi.getEvaluation(),
      ]);
      setClusters(summaryRes);
      setEvaluation(evalRes);
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to load customer segmentation data'
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let ignore = false;
    async function loadData() {
      try {
        const [summaryRes, evalRes] = await Promise.all([
          segmentationApi.getSummary(),
          segmentationApi.getEvaluation(),
        ]);
        if (!ignore) {
          setClusters(summaryRes);
          setEvaluation(evalRes);
          setLoading(false);
        }
      } catch (err: unknown) {
        if (!ignore) {
          setError(
            err instanceof Error
              ? err.message
              : 'Failed to load customer segmentation data'
          );
          setLoading(false);
        }
      }
    }

    loadData();
    return () => {
      ignore = true;
    };
  }, []);

  return {
    clusters,
    evaluation,
    loading,
    error,
    refetch: fetchSegmentationData,
  };
}
