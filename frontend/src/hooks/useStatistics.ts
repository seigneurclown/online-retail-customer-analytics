import { useState, useEffect, useCallback } from 'react';
import { statisticsApi } from '../services/statisticsApi';
import type { StatisticalTestItem, InvoiceValueSummaryItem } from '../types/statistics';

export function useStatistics() {
  const [tests, setTests] = useState<StatisticalTestItem[]>([]);
  const [invoiceSummary, setInvoiceSummary] = useState<InvoiceValueSummaryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStatisticsData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [testsRes, summaryRes] = await Promise.all([
        statisticsApi.getTests(),
        statisticsApi.getInvoiceValueSummary(),
      ]);
      setTests(testsRes);
      setInvoiceSummary(summaryRes);
    } catch (err: unknown) {
      setError(
        err instanceof Error
          ? err.message
          : 'Failed to load statistical hypothesis data'
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let ignore = false;
    async function load() {
      try {
        const [testsRes, summaryRes] = await Promise.all([
          statisticsApi.getTests(),
          statisticsApi.getInvoiceValueSummary(),
        ]);
        if (!ignore) {
          setTests(testsRes);
          setInvoiceSummary(summaryRes);
          setLoading(false);
        }
      } catch (err: unknown) {
        if (!ignore) {
          setError(
            err instanceof Error
              ? err.message
              : 'Failed to load statistical hypothesis data'
          );
          setLoading(false);
        }
      }
    }

    load();
    return () => {
      ignore = true;
    };
  }, []);

  return {
    tests,
    invoiceSummary,
    loading,
    error,
    refetch: fetchStatisticsData,
  };
}
