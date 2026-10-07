import React from 'react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip, Legend } from 'recharts';
import type { ClusterSummaryItem } from '../../types/segmentation';
import { formatCurrency } from '../../utils/formatCurrency';

interface SegmentDistributionChartProps {
  data: ClusterSummaryItem[];
  height?: number;
}

const CLUSTER_COLORS = ['#64748b', '#0284c7', '#f59e0b']; // Silver, Blue (Standard), Amber (Gold)

export const SegmentDistributionChart: React.FC<SegmentDistributionChartProps> = ({
  data,
  height = 300,
}) => {
  const chartData = data.map((item, index) => ({
    name: item.membership_tier || `Cluster ${item.cluster}`,
    value: item.customer_count,
    customerPct: item.customer_pct,
    revenueShare: item.revenue_share_pct,
    totalMonetary: item.total_monetary,
    color: CLUSTER_COLORS[index % CLUSTER_COLORS.length],
  }));

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart margin={{ top: 10, right: 10, left: 10, bottom: 10 }}>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={60}
            outerRadius={85}
            paddingAngle={4}
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value: unknown, _name: unknown, item: unknown) => {
              const payload = (item as { payload?: (typeof chartData)[0] })?.payload;
              const valNum = typeof value === 'number' ? value : 0;
              return [
                `${valNum.toLocaleString()} customers (${payload?.customerPct}%) • ${formatCurrency(
                  payload?.totalMonetary
                )} (${payload?.revenueShare}% Rev)`,
                'Audience',
              ];
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
            verticalAlign="bottom"
            height={36}
            iconType="circle"
            formatter={(value) => <span className="text-xs text-slate-700 font-medium">{value}</span>}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};
