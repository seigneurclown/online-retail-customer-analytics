import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, ChevronRight, UserCheck, ArrowUpDown, SlidersHorizontal, AlertCircle } from 'lucide-react';
import { useCustomers } from '../../hooks/useCustomers';
import { PageHeader, Pagination, Badge, ErrorState } from '../../components/common';
import { DataTable, type Column } from '../../components/tables';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatNumber } from '../../utils/formatNumber';
import type { CustomerListItem } from '../../types/customer';

export const CustomersPage: React.FC = () => {
  const navigate = useNavigate();
  const {
    data,
    loading,
    error,
    params,
    setParams,
    setSearch,
    setCluster,
    setSorting,
    setPage,
    resetFilters,
  } = useCustomers();

  const [showRfmDrawer, setShowRfmDrawer] = useState<boolean>(false);
  const [rangeError, setRangeError] = useState<string | null>(null);

  // Temporary local state for range inputs
  const [localMinMonetary, setLocalMinMonetary] = useState<string>('');
  const [localMaxMonetary, setLocalMaxMonetary] = useState<string>('');
  const [localMinRecency, setLocalMinRecency] = useState<string>('');
  const [localMaxRecency, setLocalMaxRecency] = useState<string>('');
  const [localMinFrequency, setLocalMinFrequency] = useState<string>('');
  const [localMaxFrequency, setLocalMaxFrequency] = useState<string>('');

  const applyRfmFilters = () => {
    const minM = localMinMonetary ? Number(localMinMonetary) : undefined;
    const maxM = localMaxMonetary ? Number(localMaxMonetary) : undefined;
    const minR = localMinRecency ? Number(localMinRecency) : undefined;
    const maxR = localMaxRecency ? Number(localMaxRecency) : undefined;
    const minF = localMinFrequency ? Number(localMinFrequency) : undefined;
    const maxF = localMaxFrequency ? Number(localMaxFrequency) : undefined;

    // Validate min <= max
    if (minM !== undefined && maxM !== undefined && minM > maxM) {
      setRangeError('Min Monetary cannot be greater than Max Monetary');
      return;
    }
    if (minR !== undefined && maxR !== undefined && minR > maxR) {
      setRangeError('Min Recency cannot be greater than Max Recency');
      return;
    }
    if (minF !== undefined && maxF !== undefined && minF > maxF) {
      setRangeError('Min Frequency cannot be greater than Max Frequency');
      return;
    }

    setRangeError(null);
    setParams((prev) => ({
      ...prev,
      page: 1,
      min_monetary: minM,
      max_monetary: maxM,
      min_recency: minR,
      max_recency: maxR,
      min_frequency: minF,
      max_frequency: maxF,
    }));
  };

  const handleResetAll = () => {
    setLocalMinMonetary('');
    setLocalMaxMonetary('');
    setLocalMinRecency('');
    setLocalMaxRecency('');
    setLocalMinFrequency('');
    setLocalMaxFrequency('');
    setRangeError(null);
    resetFilters();
  };

  const hasActiveRfmFilters =
    params.min_monetary !== undefined ||
    params.max_monetary !== undefined ||
    params.min_recency !== undefined ||
    params.max_recency !== undefined ||
    params.min_frequency !== undefined ||
    params.max_frequency !== undefined;

  // Helper for tier badges
  const renderTierBadge = (cluster: number | null, tier: string | null) => {
    if (cluster === 2) {
      return <Badge variant="gold">Gold Member (Cluster 2)</Badge>;
    }
    if (cluster === 0) {
      return <Badge variant="silver">Silver Member (Cluster 0)</Badge>;
    }
    if (cluster === 1) {
      return <Badge variant="default">Standard / Chuẩn (Cluster 1)</Badge>;
    }
    return <Badge variant="default">{tier || 'Unassigned'}</Badge>;
  };

  const columns: Column<CustomerListItem>[] = [
    {
      key: 'customer_id',
      header: 'Customer ID',
      render: (item) => (
        <span className="font-mono font-bold text-indigo-600 hover:text-indigo-800 transition">
          #{item.customer_id}
        </span>
      ),
    },
    {
      key: 'countries',
      header: 'Markets',
      render: (item) => (
        <span className="text-slate-700">
          {item.countries.length > 0 ? item.countries.join(', ') : 'United Kingdom'}
        </span>
      ),
    },
    {
      key: 'recency',
      header: 'Recency (Days)',
      align: 'right',
      render: (item) => (
        <span className="font-semibold text-slate-700">
          {item.recency !== null ? `${item.recency}d ago` : 'N/A'}
        </span>
      ),
    },
    {
      key: 'frequency',
      header: 'Frequency (Orders)',
      align: 'right',
      render: (item) => (
        <span className="font-medium text-slate-800">
          {item.frequency !== null ? `${formatNumber(item.frequency)} orders` : 'N/A'}
        </span>
      ),
    },
    {
      key: 'monetary',
      header: 'Monetary Value',
      align: 'right',
      render: (item) => (
        <span className="font-bold text-slate-900">
          {item.monetary !== null ? formatCurrency(item.monetary) : 'N/A'}
        </span>
      ),
    },
    {
      key: 'cluster',
      header: 'Segmentation Tier',
      render: (item) => renderTierBadge(item.cluster, item.membership_tier),
    },
    {
      key: 'actions',
      header: '',
      align: 'right',
      render: () => (
        <span className="text-slate-400 group-hover:text-indigo-600 inline-flex items-center text-xs font-medium">
          View Profile <ChevronRight className="w-4 h-4 ml-0.5" />
        </span>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <PageHeader
        title="Customer Directory & RFM Profile"
        subtitle="Individual behavioral profiling across Recency, Frequency, Monetary spend and K-Means clusters"
      />

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-2xs space-y-3">
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3">
          {/* Search Box */}
          <div className="relative flex-1 max-w-sm">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={params.search || ''}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by Customer ID (e.g. 14646)..."
              className="w-full pl-9 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition"
            />
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {/* Cluster Selector */}
            <div className="flex items-center gap-1.5">
              <UserCheck className="w-4 h-4 text-slate-400" />
              <select
                value={params.cluster !== undefined ? String(params.cluster) : 'all'}
                onChange={(e) => {
                  const val = e.target.value;
                  setCluster(val === 'all' ? undefined : Number(val));
                }}
                className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition"
              >
                <option value="all">All Clusters (4,371)</option>
                <option value="2">Cluster 2 - Thẻ Vàng (Gold)</option>
                <option value="0">Cluster 0 - Thẻ Bạc (Silver)</option>
                <option value="1">Cluster 1 - Không Thẻ (Standard)</option>
              </select>
            </div>

            {/* Sort Order Selector */}
            <div className="flex items-center gap-1.5">
              <ArrowUpDown className="w-4 h-4 text-slate-400" />
              <select
                value={`${params.sort_by}_${params.sort_order}`}
                onChange={(e) => {
                  const [sortBy, sortOrder] = e.target.value.split('_') as [string, 'asc' | 'desc'];
                  setSorting(sortBy, sortOrder);
                }}
                className="px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition"
              >
                <option value="monetary_desc">Monetary: High to Low</option>
                <option value="monetary_asc">Monetary: Low to High</option>
                <option value="frequency_desc">Frequency: Most Orders</option>
                <option value="recency_asc">Recency: Most Recent</option>
                <option value="recency_desc">Recency: Least Recent</option>
              </select>
            </div>

            {/* Toggle RFM Ranges Drawer */}
            <button
              onClick={() => setShowRfmDrawer(!showRfmDrawer)}
              type="button"
              className={`inline-flex items-center gap-1.5 px-3 py-2 border rounded-lg text-xs font-semibold transition cursor-pointer ${
                hasActiveRfmFilters || showRfmDrawer
                  ? 'bg-indigo-50 border-indigo-200 text-indigo-700'
                  : 'bg-slate-50 border-slate-200 text-slate-700 hover:bg-slate-100'
              }`}
            >
              <SlidersHorizontal className="w-3.5 h-3.5" />
              <span>RFM Ranges</span>
              {hasActiveRfmFilters && (
                <span className="w-2 h-2 rounded-full bg-indigo-600"></span>
              )}
            </button>

            {/* Clear filter */}
            {(params.search || params.cluster !== undefined || hasActiveRfmFilters) && (
              <button
                onClick={handleResetAll}
                type="button"
                className="text-xs text-slate-500 hover:text-slate-800 underline px-2 transition cursor-pointer"
              >
                Reset All
              </button>
            )}
          </div>
        </div>

        {/* Collapsible Advanced RFM Ranges Drawer */}
        {showRfmDrawer && (
          <div className="pt-3 border-t border-slate-100 bg-slate-50/50 p-3 rounded-lg space-y-3">
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {/* Monetary Range */}
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">
                  Monetary Spend (£)
                </label>
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    value={localMinMonetary}
                    onChange={(e) => setLocalMinMonetary(e.target.value)}
                    placeholder="Min £"
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                  <span className="text-slate-400">-</span>
                  <input
                    type="number"
                    value={localMaxMonetary}
                    onChange={(e) => setLocalMaxMonetary(e.target.value)}
                    placeholder="Max £"
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
              </div>

              {/* Recency Range */}
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">
                  Recency (Days)
                </label>
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    value={localMinRecency}
                    onChange={(e) => setLocalMinRecency(e.target.value)}
                    placeholder="Min days"
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                  <span className="text-slate-400">-</span>
                  <input
                    type="number"
                    value={localMaxRecency}
                    onChange={(e) => setLocalMaxRecency(e.target.value)}
                    placeholder="Max days"
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
              </div>

              {/* Frequency Range */}
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">
                  Frequency (Orders)
                </label>
                <div className="flex items-center gap-2">
                  <input
                    type="number"
                    value={localMinFrequency}
                    onChange={(e) => setLocalMinFrequency(e.target.value)}
                    placeholder="Min orders"
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                  <span className="text-slate-400">-</span>
                  <input
                    type="number"
                    value={localMaxFrequency}
                    onChange={(e) => setLocalMaxFrequency(e.target.value)}
                    placeholder="Max orders"
                    className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  />
                </div>
              </div>
            </div>

            {/* Error Message for min > max */}
            {rangeError && (
              <div className="flex items-center gap-1.5 text-xs text-rose-600 bg-rose-50 p-2 rounded border border-rose-200">
                <AlertCircle className="w-3.5 h-3.5" />
                <span>{rangeError}</span>
              </div>
            )}

            <div className="flex justify-end gap-2 pt-1">
              <button
                onClick={() => {
                  setLocalMinMonetary('');
                  setLocalMaxMonetary('');
                  setLocalMinRecency('');
                  setLocalMaxRecency('');
                  setLocalMinFrequency('');
                  setLocalMaxFrequency('');
                  setRangeError(null);
                  setParams((prev) => ({
                    ...prev,
                    min_monetary: undefined,
                    max_monetary: undefined,
                    min_recency: undefined,
                    max_recency: undefined,
                    min_frequency: undefined,
                    max_frequency: undefined,
                  }));
                }}
                type="button"
                className="px-3 py-1 bg-white border border-slate-200 rounded text-xs text-slate-600 hover:bg-slate-50 cursor-pointer"
              >
                Clear Ranges
              </button>
              <button
                onClick={applyRfmFilters}
                type="button"
                className="px-3 py-1 bg-indigo-600 text-white rounded text-xs font-semibold hover:bg-indigo-700 shadow-xs cursor-pointer"
              >
                Apply Ranges
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Global Error Card if API fails */}
      {error && (
        <ErrorState
          title="Failed to Load Customers"
          message={error}
          onRetry={handleResetAll}
        />
      )}

      {/* Customers Data Table */}
      {!error && (
        <>
          <DataTable
            columns={columns}
            data={data.items}
            keyExtractor={(item) => item.customer_id}
            loading={loading}
            onRowClick={(item) => navigate(`/customers/${item.customer_id}`)}
            emptyTitle="No customers match criteria"
            emptyMessage="Try adjusting your search terms or cluster filter."
          />

          {/* Pagination */}
          <Pagination
            currentPage={data.page}
            totalPages={data.total_pages}
            totalItems={data.total}
            pageSize={data.page_size}
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
};

export default CustomersPage;
