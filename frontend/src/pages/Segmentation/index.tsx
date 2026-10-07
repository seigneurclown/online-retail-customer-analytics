import React from 'react';
import { Award, Users, CheckCircle, RotateCw } from 'lucide-react';
import { useSegmentation } from '../../hooks/useSegmentation';
import { PageHeader, Badge, LoadingState, ErrorState } from '../../components/common';
import { ChartCard } from '../../components/cards';
import { DataTable, type Column } from '../../components/tables';
import {
  KMeansEvaluationChart,
  ClusterComparisonChart,
} from '../../components/charts';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatNumber, formatPercent } from '../../utils/formatNumber';
import type { ClusterSummaryItem } from '../../types/segmentation';

export const SegmentationPage: React.FC = () => {
  const { clusters, evaluation, loading, error, refetch } = useSegmentation();

  if (error) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Customer Segmentation"
          subtitle="RFM behavioral profiling and K-Means clustering analysis"
        />
        <ErrorState
          title="Failed to Load Segmentation Data"
          message={error}
          onRetry={refetch}
        />
      </div>
    );
  }

  // Helper for tier badges
  const renderTierBadge = (cluster: number, tier: string) => {
    if (cluster === 2) {
      return <Badge variant="gold">Gold Member (Cluster 2)</Badge>;
    }
    if (cluster === 0) {
      return <Badge variant="silver">Silver Member (Cluster 0)</Badge>;
    }
    return <Badge variant="default">{tier || 'Standard (Cluster 1)'}</Badge>;
  };

  const columns: Column<ClusterSummaryItem>[] = [
    {
      key: 'cluster',
      header: 'Cluster ID',
      render: (c) => (
        <span className="font-mono font-bold text-slate-900">Cluster {c.cluster}</span>
      ),
    },
    {
      key: 'membership_tier',
      header: 'Membership Tier',
      render: (c) => renderTierBadge(c.cluster, c.membership_tier),
    },
    {
      key: 'customer_count',
      header: 'Buyers',
      align: 'right',
      render: (c) => (
        <span className="font-bold text-slate-800">
          {formatNumber(c.customer_count)}{' '}
          <span className="text-[11px] text-slate-500 font-normal">
            ({formatPercent(c.customer_pct)})
          </span>
        </span>
      ),
    },
    {
      key: 'revenue_share_pct',
      header: 'Revenue Share',
      align: 'right',
      render: (c) => (
        <Badge variant={c.revenue_share_pct > 40 ? 'gold' : 'info'}>
          {formatPercent(c.revenue_share_pct)}
        </Badge>
      ),
    },
    {
      key: 'recency_mean',
      header: 'Recency (Mean / Med)',
      align: 'right',
      render: (c) => (
        <span>
          {Math.round(c.recency_mean)}d{' '}
          <span className="text-slate-400">/ {Math.round(c.recency_median)}d</span>
        </span>
      ),
    },
    {
      key: 'frequency_mean',
      header: 'Frequency (Mean / Med)',
      align: 'right',
      render: (c) => (
        <span>
          {c.frequency_mean.toFixed(1)}{' '}
          <span className="text-slate-400">/ {c.frequency_median.toFixed(0)}</span>
        </span>
      ),
    },
    {
      key: 'monetary_mean',
      header: 'Monetary (Mean / Med)',
      align: 'right',
      render: (c) => (
        <span>
          {formatCurrency(c.monetary_mean)}{' '}
          <span className="text-slate-400">/ {formatCurrency(c.monetary_median)}</span>
        </span>
      ),
    },
    {
      key: 'total_monetary',
      header: 'Cumulative Spend',
      align: 'right',
      render: (c) => (
        <span className="font-bold text-slate-900">{formatCurrency(c.total_monetary)}</span>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <PageHeader
        title="Customer Segmentation (RFM + K-Means)"
        subtitle="Unsupervised machine learning profiles, cluster evaluation, and business tier assignments"
        action={
          <button
            onClick={refetch}
            disabled={loading}
            type="button"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold shadow-2xs transition cursor-pointer disabled:opacity-50"
          >
            <RotateCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin text-indigo-600' : ''}`} />
            <span>Refresh</span>
          </button>
        }
      />

      {/* Section 1: Cluster Persona Cards */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <LoadingState type="card" />
          <LoadingState type="card" />
          <LoadingState type="card" />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {clusters.map((c) => {
            const isGold = c.cluster === 2;
            const isSilver = c.cluster === 0;
            return (
              <div
                key={c.cluster}
                className={`p-5 rounded-xl border bg-white shadow-xs transition ${
                  isGold
                    ? 'border-amber-300 ring-1 ring-amber-100'
                    : isSilver
                    ? 'border-slate-300'
                    : 'border-slate-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-mono font-bold text-slate-400">
                    CLUSTER {c.cluster}
                  </span>
                  {renderTierBadge(c.cluster, c.membership_tier)}
                </div>

                <div className="mt-3">
                  <div className="text-2xl font-extrabold text-slate-900">
                    {formatCurrency(c.total_monetary)}
                  </div>
                  <p className="text-xs text-slate-500 mt-0.5">
                    {c.revenue_share_pct}% total revenue &bull; {c.customer_pct}% buyers
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-3 gap-2 text-xs">
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">
                      Recency
                    </span>
                    <p className="font-bold text-slate-800 mt-0.5">
                      {Math.round(c.recency_mean)}d
                    </p>
                  </div>
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">
                      Frequency
                    </span>
                    <p className="font-bold text-slate-800 mt-0.5">
                      {c.frequency_mean.toFixed(1)}
                    </p>
                  </div>
                  <div>
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">
                      Avg Spend
                    </span>
                    <p className="font-bold text-slate-800 mt-0.5">
                      {formatCurrency(c.monetary_mean)}
                    </p>
                  </div>
                </div>

                <div className="mt-3 p-2.5 bg-slate-50 rounded-lg text-[11px] text-slate-600 leading-relaxed">
                  {isGold && (
                    <span className="flex items-start gap-1.5">
                      <Award className="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5" />
                      <span>Nhóm khách VIP then chốt mang lại giá trị cao nhất cho doanh nghiệp.</span>
                    </span>
                  )}
                  {isSilver && (
                    <span className="flex items-start gap-1.5">
                      <Users className="w-3.5 h-3.5 text-slate-600 shrink-0 mt-0.5" />
                      <span>Nhóm khách hàng trung thành, phát sinh đơn hàng đều đặn.</span>
                    </span>
                  )}
                  {!isGold && !isSilver && (
                    <span className="flex items-start gap-1.5">
                      <CheckCircle className="w-3.5 h-3.5 text-indigo-600 shrink-0 mt-0.5" />
                      <span>Nhóm khách hàng tiêu chuẩn, chi tiêu khiêm tốn hoặc lâu chưa quay lại.</span>
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Section 2: Visual Comparison & K-Means Evaluation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ChartCard
          title="Segment Population vs Revenue Share"
          subtitle="Pareto disparity: Gold tier drives majority revenue with small customer percentage"
        >
          {loading ? (
            <LoadingState type="chart" message="Loading cluster comparison..." />
          ) : (
            <ClusterComparisonChart data={clusters} height={280} />
          )}
        </ChartCard>

        <ChartCard
          title="K-Means Mathematical Evaluation"
          subtitle="Validation of optimal cluster count (k = 3) via Elbow & Silhouette metrics"
        >
          {loading ? (
            <LoadingState type="chart" message="Loading K-Means evaluation..." />
          ) : (
            <KMeansEvaluationChart data={evaluation} height={220} />
          )}
        </ChartCard>
      </div>

      {/* Section 3: Detailed Metrics Table */}
      <div className="space-y-2">
        <h2 className="text-base font-bold text-slate-900">Cluster Metrics Benchmark</h2>
        <p className="text-xs text-slate-500">
          Empirical statistics: Mean and median RFM values derived directly from clustering model
        </p>
        <DataTable
          columns={columns}
          data={clusters}
          keyExtractor={(c) => c.cluster}
          loading={loading}
          emptyTitle="No segmentation summary available"
        />
      </div>
    </div>
  );
};

export default SegmentationPage;
