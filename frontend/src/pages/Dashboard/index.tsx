import React from 'react';
import {
  PoundSterling,
  ShoppingBag,
  Users,
  CreditCard,
  RotateCw,
  TrendingUp,
  Sparkles,
} from 'lucide-react';
import { useDashboard } from '../../hooks/useDashboard';
import { MetricCard, ChartCard } from '../../components/cards';
import { PageHeader, LoadingState, ErrorState, DataManagementModal } from '../../components/common';
import {
  RevenueTrendChart,
  TopCountriesChart,
  TopProductsChart,
  SegmentDistributionChart,
} from '../../components/charts';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatNumber } from '../../utils/formatNumber';

export const DashboardPage: React.FC = () => {
  const { summary, revenueTrend, topProducts, topCountries, segments, loading, error, refetch } =
    useDashboard();
  const [isSeedModalOpen, setIsSeedModalOpen] = React.useState(false);

  if (error) {
    return (
      <div>
        <PageHeader
          title="Executive Dashboard"
          subtitle="Real-time key performance indicators and revenue analysis"
          action={
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsSeedModalOpen(true)}
                type="button"
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-semibold shadow-xs transition cursor-pointer"
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Nạp dữ liệu vào Database</span>
              </button>
              <button
                onClick={refetch}
                type="button"
                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold shadow-xs transition cursor-pointer"
              >
                <RotateCw className="w-3.5 h-3.5" />
                <span>Thử lại</span>
              </button>
            </div>
          }
        />
        <ErrorState
          title="Failed to Load Dashboard Data"
          message={error}
          onRetry={refetch}
          className="mt-8"
        />
        <DataManagementModal
          isOpen={isSeedModalOpen}
          onClose={() => setIsSeedModalOpen(false)}
          onDataChanged={refetch}
        />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Page Title & Actions */}
      <PageHeader
        title="Executive Dashboard"
        subtitle="Real-time key performance indicators, sales dynamics, and customer segmentation"
        action={
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsSeedModalOpen(true)}
              type="button"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 rounded-lg text-xs font-semibold shadow-2xs transition cursor-pointer"
            >
              <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
              <span>Nạp / Quản lý Dữ liệu</span>
            </button>
            <button
              onClick={refetch}
              type="button"
              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold shadow-2xs transition cursor-pointer"
            >
              <RotateCw className="w-3.5 h-3.5" />
              <span>Làm mới</span>
            </button>
          </div>
        }
      />
      <DataManagementModal
        isOpen={isSeedModalOpen}
        onClose={() => setIsSeedModalOpen(false)}
        onDataChanged={refetch}
      />

      {/* Row 1: KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {loading ? (
          <>
            <LoadingState type="card" />
            <LoadingState type="card" />
            <LoadingState type="card" />
            <LoadingState type="card" />
          </>
        ) : (
          <>
            <MetricCard
              title="Total Revenue"
              value={formatCurrency(summary?.total_revenue)}
              subtitle="Net sales across 2010-2011"
              icon={PoundSterling}
              iconColor="text-indigo-600"
              iconBg="bg-indigo-50"
              trend={{ value: 'Full Period', isPositive: true }}
            />
            <MetricCard
              title="Total Invoices"
              value={formatNumber(summary?.total_orders)}
              subtitle="Successfully fulfilled orders"
              icon={ShoppingBag}
              iconColor="text-emerald-600"
              iconBg="bg-emerald-50"
            />
            <MetricCard
              title="Unique Customers"
              value={formatNumber(summary?.total_customers)}
              subtitle="Identified retail buyers"
              icon={Users}
              iconColor="text-sky-600"
              iconBg="bg-sky-50"
            />
            <MetricCard
              title="Average Order Value"
              value={formatCurrency(summary?.average_order_value)}
              subtitle="Mean basket size per invoice"
              icon={CreditCard}
              iconColor="text-amber-600"
              iconBg="bg-amber-50"
            />
          </>
        )}
      </div>

      {/* Row 2: Revenue Trend & Country Share */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          {loading ? (
            <LoadingState type="chart" message="Loading monthly trend..." />
          ) : (
            <ChartCard
              title="Monthly Revenue Trend (2010 - 2011)"
              subtitle="Net revenue trajectory across 13 months with noticeable Q4 peak"
              action={
                <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full">
                  <TrendingUp className="w-3 h-3" />
                  Peak Nov 2011
                </span>
              }
            >
              <RevenueTrendChart data={revenueTrend} height={300} />
            </ChartCard>
          )}
        </div>

        <div className="lg:col-span-1">
          {loading ? (
            <LoadingState type="chart" message="Loading regional share..." />
          ) : (
            <ChartCard
              title="Revenue by Market"
              subtitle="Top national destinations contributing highest volume"
            >
              <TopCountriesChart data={topCountries} height={300} />
            </ChartCard>
          )}
        </div>
      </div>

      {/* Row 3: Top Products & Customer Segment Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          {loading ? (
            <LoadingState type="chart" message="Loading best-selling items..." />
          ) : (
            <ChartCard
              title="Top Performing Products"
              subtitle="Highest revenue-generating merchandise items by SKU"
            >
              <TopProductsChart data={topProducts} height={290} />
            </ChartCard>
          )}
        </div>

        <div className="lg:col-span-1">
          {loading ? (
            <LoadingState type="chart" message="Loading customer clusters..." />
          ) : (
            <ChartCard
              title="Customer Segments (K-Means)"
              subtitle="Audience share by assigned behavioral tier"
            >
              <SegmentDistributionChart data={segments} height={290} />
            </ChartCard>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
