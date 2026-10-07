import { useState, useEffect, useCallback } from 'react';
import { customersApi } from '../services/customersApi';
import type {
  CustomerListItem,
  CustomerDetailResponse,
  CustomerFilterParams,
} from '../types/customer';
import type { PaginatedResponse } from '../types/common';

export function useCustomers() {
  const [params, setParams] = useState<CustomerFilterParams>({
    page: 1,
    page_size: 15,
    cluster: undefined,
    membership_tier: undefined,
    search: '',
    sort_by: 'monetary',
    sort_order: 'desc',
  });

  const [data, setData] = useState<PaginatedResponse<CustomerListItem>>({
    items: [],
    page: 1,
    page_size: 15,
    total: 0,
    total_pages: 0,
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCustomers = useCallback(async (filterParams: CustomerFilterParams) => {
    setLoading(true);
    setError(null);
    try {
      const res = await customersApi.getCustomers(filterParams);
      setData(res);
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : 'Failed to fetch customer records'
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchCustomers(params);
    }, 250);
    return () => clearTimeout(timer);
  }, [params, fetchCustomers]);

  return {
    data,
    loading,
    error,
    params,
    setParams,
    setPage: (page: number) => setParams((prev) => ({ ...prev, page })),
    setSearch: (search: string) => setParams((prev) => ({ ...prev, search, page: 1 })),
    setCluster: (cluster?: number) =>
      setParams((prev) => ({ ...prev, cluster, page: 1 })),
    setSorting: (sortBy: string, sortOrder: 'asc' | 'desc') =>
      setParams((prev) => ({ ...prev, sort_by: sortBy, sort_order: sortOrder, page: 1 })),
    resetFilters: () =>
      setParams({
        page: 1,
        page_size: 15,
        cluster: undefined,
        membership_tier: undefined,
        search: '',
        sort_by: 'monetary',
        sort_order: 'desc',
      }),
  };
}

export function useCustomerDetail(customerId?: string) {
  const [customer, setCustomer] = useState<CustomerDetailResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDetail = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const res = await customersApi.getCustomerById(id);
      setCustomer(res);
    } catch (err: unknown) {
      setError(
        err instanceof Error ? err.message : `Customer #${id} not found`
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let ignore = false;
    async function load() {
      if (!customerId) return;
      try {
        const res = await customersApi.getCustomerById(customerId);
        if (!ignore) {
          setCustomer(res);
          setLoading(false);
        }
      } catch (err: unknown) {
        if (!ignore) {
          setError(
            err instanceof Error ? err.message : `Customer #${customerId} not found`
          );
          setLoading(false);
        }
      }
    }

    load();
    return () => {
      ignore = true;
    };
  }, [customerId]);

  return {
    customer,
    loading,
    error,
    refetch: () => customerId && fetchDetail(customerId),
  };
}
