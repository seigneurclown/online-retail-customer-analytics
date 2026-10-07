import React from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  Calendar,
  ShoppingBag,
  PoundSterling,
  Globe2,
  PieChart,
  RotateCcw,
} from 'lucide-react';
import { useCustomerDetail } from '../../hooks/useCustomers';
import { MetricCard } from '../../components/cards';
import { Badge, LoadingState, ErrorState } from '../../components/common';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatNumber } from '../../utils/formatNumber';

export const CustomerDetailPage: React.FC = () => {
  const { customerId } = useParams<{ customerId: string }>();
  const { customer, loading, error, refetch } = useCustomerDetail(customerId);

  if (loading) {
    return (
      <div className="space-y-6">
        <Link
          to="/customers"
          className="inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Customer Directory
        </Link>
        <LoadingState message={`Loading customer #${customerId} profile...`} />
      </div>
    );
  }

  if (error || !customer) {
    return (
      <div className="space-y-6">
        <Link
          to="/customers"
          className="inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-900 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Customer Directory
        </Link>
        <ErrorState
          title="Customer Not Found"
          message={error || `Could not find records for customer ID ${customerId}`}
          onRetry={refetch}
        />
      </div>
    );
  }

  // Tier styling
  const getBadgeVariant = (cluster: number) => {
    if (cluster === 2) return 'gold';
    if (cluster === 0) return 'silver';
    return 'default';
  };

  return (
    <div className="space-y-6">
      {/* Breadcrumb Navigation */}
      <div className="flex items-center justify-between">
        <Link
          to="/customers"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-indigo-600 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Customer Directory
        </Link>
        <button
          onClick={refetch}
          type="button"
          className="inline-flex items-center gap-1.5 text-xs text-slate-500 hover:text-slate-800 transition cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          Refresh Profile
        </button>
      </div>

      {/* Main Profile Header Banner */}
      <div className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 bg-indigo-50 border border-indigo-100 rounded-xl flex items-center justify-center text-indigo-600 font-bold text-xl font-mono">
            #{customer.customer_id.slice(-2)}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-900">
                Customer #{customer.customer_id}
              </h1>
              <Badge variant={getBadgeVariant(customer.cluster)}>
                {customer.membership_tier} (Cluster {customer.cluster})
              </Badge>
            </div>
            <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
              <span className="flex items-center gap-1">
                <Globe2 className="w-3.5 h-3.5 text-slate-400" />
                {customer.countries.length > 0 ? customer.countries.join(', ') : 'United Kingdom'}
              </span>
              <span>&bull;</span>
              <span>Behavioral Tier: {customer.membership_tier}</span>
            </div>
          </div>
        </div>

        <Link
          to="/segmentation"
          className="inline-flex items-center gap-1.5 px-3.5 py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 border border-slate-200 rounded-lg text-xs font-semibold transition"
        >
          <PieChart className="w-4 h-4 text-indigo-600" />
          <span>View Cluster {customer.cluster} Details</span>
        </Link>
      </div>

      {/* RFM Metrics Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <MetricCard
          title="Recency (Days Since Last Order)"
          value={`${customer.recency} days`}
          subtitle={
            customer.recency <= 30
              ? 'Highly active in recent 30 days'
              : customer.recency <= 90
              ? 'Moderately recent buyer'
              : 'Dormant or at-risk of churn'
          }
          icon={Calendar}
          iconColor="text-sky-600"
          iconBg="bg-sky-50"
        />

        <MetricCard
          title="Frequency (Total Invoices)"
          value={`${formatNumber(customer.frequency)} orders`}
          subtitle="Distinct invoice transactions recorded"
          icon={ShoppingBag}
          iconColor="text-emerald-600"
          iconBg="bg-emerald-50"
        />

        <MetricCard
          title="Monetary Value (Lifetime Spend)"
          value={formatCurrency(customer.monetary)}
          subtitle="Net cumulative retail expenditure (£)"
          icon={PoundSterling}
          iconColor="text-indigo-600"
          iconBg="bg-indigo-50"
        />
      </div>

      {/* Analytical Persona Card */}
      <div className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs">
        <h2 className="text-sm font-bold text-slate-900 mb-2">Behavioral Segment Description</h2>
        <div className="text-xs text-slate-600 space-y-2 leading-relaxed">
          {customer.cluster === 2 && (
            <p>
              Khách hàng này thuộc phân cụm <strong>Thẻ Vàng - Kim Cương (Gold Tier)</strong>. Đây là nhóm khách hàng VIP có giá trị giao dịch đặc biệt lớn và tần suất mua hàng cao vượt trội so với mức trung bình của toàn bộ tập khách hàng bán lẻ.
            </p>
          )}
          {customer.cluster === 0 && (
            <p>
              Khách hàng này thuộc phân cụm <strong>Thẻ Bạc (Silver Tier)</strong>. Nhóm khách hàng này có tần suất mua sắm đều đặn, mức chi tiêu ổn định và thời gian quay lại gần đây tương đối ngắn.
            </p>
          )}
          {customer.cluster === 1 && (
            <p>
              Khách hàng này thuộc phân cụm <strong>Không Thẻ / Hạng Chuẩn (Standard Tier)</strong>. Nhóm này có mức chi tiêu khiêm tốn hoặc thời gian phát sinh giao dịch gần nhất cách đây tương đối lâu (Recency cao).
            </p>
          )}
        </div>
      </div>
    </div>
  );
};

export default CustomerDetailPage;
