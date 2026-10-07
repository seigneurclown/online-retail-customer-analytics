import React from 'react';
import {
  FlaskConical,
  CheckCircle2,
  HelpCircle,
  BarChart3,
  RotateCw,
  Sigma,
} from 'lucide-react';
import { useStatistics } from '../../hooks/useStatistics';
import { PageHeader, Badge, LoadingState, ErrorState } from '../../components/common';
import { MetricCard } from '../../components/cards';
import { DataTable, type Column } from '../../components/tables';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatNumber } from '../../utils/formatNumber';
import type { InvoiceValueSummaryItem } from '../../types/statistics';

export const StatisticsPage: React.FC = () => {
  const { tests, invoiceSummary, loading, error, refetch } = useStatistics();

  if (error) {
    return (
      <div className="space-y-6">
        <PageHeader
          title="Statistical Hypothesis Tests"
          subtitle="Empirical statistical inference and data distribution properties"
        />
        <ErrorState
          title="Failed to Load Statistical Results"
          message={error}
          onRetry={refetch}
        />
      </div>
    );
  }

  // Find metrics from summary
  const getMetricValue = (metricName: string): number | null => {
    const item = invoiceSummary.find((m) =>
      m.metric.toLowerCase().includes(metricName.toLowerCase())
    );
    return item ? item.value : null;
  };

  const invoiceColumns: Column<InvoiceValueSummaryItem>[] = [
    {
      key: 'metric',
      header: 'Statistical Metric / Quantile',
      render: (item) => (
        <span className="font-semibold text-slate-800">{item.metric}</span>
      ),
    },
    {
      key: 'value',
      header: 'Value',
      align: 'right',
      render: (item) => {
        const isCurrency = [
          'mean',
          'std',
          'min',
          '25%',
          'median',
          '50%',
          '75%',
          'max',
          'iqr',
        ].some((k) => item.metric.toLowerCase().includes(k));

        if (item.metric.toLowerCase().includes('count')) {
          return <span className="font-mono">{formatNumber(item.value)}</span>;
        }

        if (item.metric.toLowerCase().includes('skewness')) {
          return <span className="font-mono">{item.value.toFixed(2)} (Heavy Right-Skew)</span>;
        }

        return (
          <span className="font-mono font-bold text-slate-900">
            {isCurrency ? formatCurrency(item.value) : item.value.toFixed(2)}
          </span>
        );
      },
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <PageHeader
        title="Statistical Hypothesis Tests & Inference"
        subtitle="Rigorous empirical testing, distribution analysis, and business hypothesis validations"
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

      {/* Section 1: Hypothesis Test Result Cards */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <FlaskConical className="w-4 h-4 text-indigo-600" />
          <h2 className="text-base font-bold text-slate-900">
            Formal Hypothesis Testing Results ({tests.length} Studies)
          </h2>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <LoadingState type="card" />
            <LoadingState type="card" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {tests.map((test) => {
              const isSignificant =
                test.p_value !== null && test.p_value < 0.05;

              return (
                <div
                  key={test.id}
                  className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs flex flex-col justify-between"
                >
                  <div>
                    {/* Top Row: Test ID & Name */}
                    <div className="flex items-center justify-between gap-2 mb-3">
                      <span className="text-[11px] font-mono font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                        TEST #{test.id}
                      </span>
                      <Badge variant={isSignificant ? 'success' : 'default'}>
                        {isSignificant ? 'Statistically Significant (p < 0.05)' : 'Not Significant'}
                      </Badge>
                    </div>

                    <h3 className="text-base font-bold text-slate-900 mb-1">
                      {test.test_name}
                    </h3>

                    {/* Research Question */}
                    <div className="mt-3 p-3 bg-slate-50 rounded-lg border border-slate-100">
                      <div className="flex items-start gap-1.5 text-xs font-semibold text-slate-700 mb-1">
                        <HelpCircle className="w-3.5 h-3.5 text-indigo-600 shrink-0 mt-0.5" />
                        <span>Research Question:</span>
                      </div>
                      <p className="text-xs text-slate-800 italic leading-relaxed">
                        &ldquo;{test.research_question}&rdquo;
                      </p>
                    </div>

                    {/* Justification / Reason */}
                    <div className="mt-3 text-xs text-slate-600">
                      <span className="font-semibold text-slate-700">Methodological Reason: </span>
                      {test.reason}
                    </div>

                    {/* Mathematical Metrics Grid */}
                    <div className="mt-4 grid grid-cols-3 gap-2 p-3 bg-slate-50/80 rounded-lg text-xs">
                      <div>
                        <span className="text-[10px] text-slate-400 uppercase font-semibold">
                          Test Statistic
                        </span>
                        <p className="font-mono font-bold text-slate-900 mt-0.5">
                          {test.test_statistic}
                        </p>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-400 uppercase font-semibold">
                          p-value
                        </span>
                        <p className="font-mono font-bold text-emerald-700 mt-0.5">
                          {test.p_value !== null
                            ? test.p_value < 0.0001
                              ? test.p_value.toExponential(3)
                              : test.p_value.toFixed(4)
                            : 'N/A'}
                        </p>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-400 uppercase font-semibold">
                          Significance Level
                        </span>
                        <p className="font-mono font-bold text-slate-900 mt-0.5">
                          {test.significance_level}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Business Conclusion */}
                  <div className="mt-4 pt-3 border-t border-slate-100 flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <div>
                      <span className="text-xs font-bold text-slate-900">Empirical Verdict: </span>
                      <span className="text-xs text-slate-700 leading-relaxed">
                        {test.conclusion}
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Section 2: Distribution Parameters of Invoice Values */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-indigo-600" />
          <h2 className="text-base font-bold text-slate-900">
            Invoice Value Distribution Properties (Parametric vs Non-Parametric)
          </h2>
        </div>

        {/* 4 Summary KPI Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="Sample Invoices (N)"
            value={formatNumber(getMetricValue('count'))}
            subtitle="Valid completed retail orders"
            icon={Sigma}
            iconColor="text-indigo-600"
            iconBg="bg-indigo-50"
          />
          <MetricCard
            title="Mean Invoice Value"
            value={formatCurrency(getMetricValue('mean'))}
            subtitle="Average basket across whole dataset"
            icon={Sigma}
            iconColor="text-emerald-600"
            iconBg="bg-emerald-50"
          />
          <MetricCard
            title="Median Value (50%)"
            value={formatCurrency(getMetricValue('50%') || getMetricValue('median'))}
            subtitle="50th percentile (Robust metric)"
            icon={Sigma}
            iconColor="text-sky-600"
            iconBg="bg-sky-50"
          />
          <MetricCard
            title="Interquartile Range (IQR)"
            value={formatCurrency(getMetricValue('iqr'))}
            subtitle="Spread between Q3 (75%) and Q1 (25%)"
            icon={Sigma}
            iconColor="text-amber-600"
            iconBg="bg-amber-50"
          />
        </div>

        {/* Full Quantile Table */}
        <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
          <div className="p-4 border-b border-slate-100">
            <h3 className="text-sm font-bold text-slate-900">Complete Quantile & Distribution Breakdown</h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Empirical distribution values explaining why Non-Parametric tests (Mann-Whitney U) are scientifically mandated
            </p>
          </div>
          <DataTable
            columns={invoiceColumns}
            data={invoiceSummary}
            keyExtractor={(item) => item.metric}
            loading={loading}
            emptyTitle="No descriptive statistics available"
          />
        </div>
      </div>
    </div>
  );
};

export default StatisticsPage;
