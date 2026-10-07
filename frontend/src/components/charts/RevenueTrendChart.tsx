import React from 'react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import type { RevenueTrendItem } from '../../types/dashboard';
import { formatCurrency } from '../../utils/formatCurrency';

interface RevenueTrendChartProps {
  data: RevenueTrendItem[];
  height?: number;
}

export const RevenueTrendChart: React.FC<RevenueTrendChartProps> = ({
  data,
  height = 300,
}) => {
  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
          <defs>
            <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#4f46e5" stopOpacity={0.25} />
              <stop offset="95%" stopColor="#4f46e5" stopOpacity={0.0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
          <XAxis
            dataKey="year_month"
            stroke="#94a3b8"
            fontSize={11}
            tickLine={false}
            axisLine={{ stroke: '#e2e8f0' }}
          />
          <YAxis
            stroke="#94a3b8"
            fontSize={11}
            tickLine={false}
            axisLine={false}
            tickFormatter={(val: number) => `£${(val / 1000).toFixed(0)}k`}
          />
          <Tooltip
            formatter={(value: unknown) => [
              formatCurrency(typeof value === 'number' ? value : 0),
              'Net Revenue',
            ]}
            labelFormatter={(label) => `Month: ${label}`}
            contentStyle={{
              backgroundColor: '#0f172a',
              borderRadius: '8px',
              border: 'none',
              color: '#f8fafc',
              fontSize: '12px',
              boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
            }}
          />
          <Area
            type="monotone"
            dataKey="revenue"
            stroke="#4f46e5"
            strokeWidth={2.5}
            fillOpacity={1}
            fill="url(#revenueGradient)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
