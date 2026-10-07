import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts';
import type { TopProductItem } from '../../types/dashboard';
import { formatCurrency } from '../../utils/formatCurrency';

interface TopProductsChartProps {
  data: TopProductItem[];
  height?: number;
}

export const TopProductsChart: React.FC<TopProductsChartProps> = ({
  data,
  height = 300,
}) => {
  const displayData = data.slice(0, 6).map((item) => ({
    ...item,
    displayName: item.description
      ? item.description.length > 20
        ? `${item.description.slice(0, 20)}...`
        : item.description
      : item.stock_code,
  }));

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={displayData} margin={{ top: 10, right: 10, left: 10, bottom: 25 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
          <XAxis
            dataKey="displayName"
            stroke="#64748b"
            fontSize={10}
            interval={0}
            angle={-20}
            textAnchor="end"
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
            formatter={(value: unknown, _name: unknown, item: unknown) => {
              const product = (item as { payload?: TopProductItem })?.payload;
              const valNum = typeof value === 'number' ? value : 0;
              return [
                `${formatCurrency(valNum)} (${product?.total_quantity.toLocaleString()} units)`,
                'Revenue',
              ];
            }}
            labelFormatter={(_label, payload) => {
              const p = payload?.[0]?.payload as TopProductItem | undefined;
              return p?.description ? `[${p.stock_code}] ${p.description}` : `Stock: ${p?.stock_code}`;
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
          <Bar dataKey="total_revenue" fill="#6366f1" radius={[4, 4, 0, 0]} barSize={28} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
