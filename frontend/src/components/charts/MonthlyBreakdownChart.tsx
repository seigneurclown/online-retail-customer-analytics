import React from 'react';
import {
  ResponsiveContainer,
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import type { MonthlySalesItem } from '../../types/sales';
import { formatCurrency } from '../../utils/formatCurrency';

interface MonthlyBreakdownChartProps {
  data: MonthlySalesItem[];
  height?: number;
}

export const MonthlyBreakdownChart: React.FC<MonthlyBreakdownChartProps> = ({
  data,
  height = 320,
}) => {
  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={data} margin={{ top: 15, right: 15, left: 15, bottom: 5 }}>
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
            formatter={(value: unknown, name: unknown) => [
              formatCurrency(typeof value === 'number' ? value : 0),
              name === 'gross_revenue'
                ? 'Gross Revenue'
                : name === 'cancelled_revenue'
                ? 'Cancelled Revenue'
                : 'Net Revenue',
            ]}
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
            formatter={(value) => {
              const labelMap: Record<string, string> = {
                gross_revenue: 'Gross Revenue',
                cancelled_revenue: 'Cancelled',
                net_revenue: 'Net Revenue',
              };
              return <span className="text-xs text-slate-700 font-medium">{labelMap[value] || value}</span>;
            }}
          />
          <Bar
            dataKey="gross_revenue"
            fill="#818cf8"
            radius={[4, 4, 0, 0]}
            barSize={18}
          />
          <Bar
            dataKey="cancelled_revenue"
            fill="#f43f5e"
            radius={[4, 4, 0, 0]}
            barSize={18}
          />
          <Line
            type="monotone"
            dataKey="net_revenue"
            stroke="#0284c7"
            strokeWidth={2.5}
            dot={{ r: 3, fill: '#0284c7' }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};
