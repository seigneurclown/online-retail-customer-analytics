import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import type { ClusterSummaryItem } from '../../types/segmentation';
import { formatCurrency } from '../../utils/formatCurrency';

interface ClusterComparisonChartProps {
  data: ClusterSummaryItem[];
  height?: number;
}

export const ClusterComparisonChart: React.FC<ClusterComparisonChartProps> = ({
  data,
  height = 300,
}) => {
  // Structure data for comparison
  const chartData = data.map((c) => ({
    name: c.membership_tier.split('(')[0].trim() || `Cluster ${c.cluster}`,
    cluster: `Cluster ${c.cluster}`,
    recency_mean: Math.round(c.recency_mean),
    frequency_mean: Math.round(c.frequency_mean),
    monetary_mean: Math.round(c.monetary_mean),
    revenue_share_pct: c.revenue_share_pct,
    customer_pct: c.customer_pct,
  }));

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={chartData} margin={{ top: 15, right: 20, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
          <XAxis dataKey="name" stroke="#475569" fontSize={11} tickLine={false} />
          <YAxis
            stroke="#94a3b8"
            fontSize={11}
            tickLine={false}
            axisLine={false}
            tickFormatter={(val: number) => `${val}%`}
          />
          <Tooltip
            formatter={(value: unknown, name: unknown, item: unknown) => {
              const payload = (item as { payload?: (typeof chartData)[0] })?.payload;
              const valNum = typeof value === 'number' ? value : 0;
              if (name === 'revenue_share_pct') {
                return [`${valNum}% (${formatCurrency(payload?.monetary_mean)} mean)`, 'Revenue Share'];
              }
              return [`${valNum}%`, 'Customer Population'];
            }}
            contentStyle={{
              backgroundColor: '#0f172a',
              borderRadius: '8px',
              border: 'none',
              color: '#f8fafc',
              fontSize: '12px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
          />
          <Legend
            verticalAlign="top"
            height={36}
            iconType="circle"
            formatter={(value) => (
              <span className="text-xs text-slate-700 font-medium">
                {value === 'revenue_share_pct' ? 'Revenue Contribution (%)' : 'Customer Population (%)'}
              </span>
            )}
          />
          <Bar
            dataKey="customer_pct"
            name="customer_pct"
            fill="#64748b"
            radius={[4, 4, 0, 0]}
            barSize={28}
          />
          <Bar
            dataKey="revenue_share_pct"
            name="revenue_share_pct"
            fill="#4f46e5"
            radius={[4, 4, 0, 0]}
            barSize={28}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
