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
import type { TopCountryItem } from '../../types/dashboard';
import { formatCurrency } from '../../utils/formatCurrency';

interface TopCountriesChartProps {
  data: TopCountryItem[];
  height?: number;
}

export const TopCountriesChart: React.FC<TopCountriesChartProps> = ({
  data,
  height = 300,
}) => {
  // Take top 6 for clear visual display in dashboard view
  const displayData = data.slice(0, 6);

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          layout="vertical"
          data={displayData}
          margin={{ top: 10, right: 20, left: 35, bottom: 0 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
          <XAxis
            type="number"
            stroke="#94a3b8"
            fontSize={11}
            tickLine={false}
            axisLine={false}
            tickFormatter={(val: number) => `£${(val / 1000).toFixed(0)}k`}
          />
          <YAxis
            type="category"
            dataKey="country"
            stroke="#475569"
            fontSize={11}
            tickLine={false}
            axisLine={{ stroke: '#e2e8f0' }}
            width={75}
          />
          <Tooltip
            formatter={(value: unknown, _name: unknown, item: unknown) => {
              const countryItem = (item as { payload?: TopCountryItem })?.payload;
              const valNum = typeof value === 'number' ? value : 0;
              return [
                `${formatCurrency(valNum)} (${countryItem?.percentage_share ?? 0}% share)`,
                'Revenue',
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
          <Bar dataKey="total_revenue" fill="#0284c7" radius={[0, 4, 4, 0]} barSize={16} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
