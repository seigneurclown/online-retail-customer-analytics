import React from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from 'recharts';
import type { KMeansEvaluationItem } from '../../types/segmentation';

interface KMeansEvaluationChartProps {
  data: KMeansEvaluationItem[];
  height?: number;
}

export const KMeansEvaluationChart: React.FC<KMeansEvaluationChartProps> = ({
  data,
  height = 280,
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4" style={{ width: '100%' }}>
      {/* 1. Inertia (Elbow Method) */}
      <div className="bg-slate-50/70 p-3 rounded-lg border border-slate-200/60">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold text-slate-800">Elbow Method (Inertia)</span>
          <span className="text-[11px] text-slate-500">Lower is better</span>
        </div>
        <div style={{ width: '100%', height }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 10, right: 15, left: 15, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
              <XAxis dataKey="k" stroke="#64748b" fontSize={11} tickLine={false} />
              <YAxis
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                tickFormatter={(val: number) => `${(val / 1000).toFixed(0)}k`}
              />
              <Tooltip
                formatter={(val: unknown) => [
                  typeof val === 'number' ? val.toLocaleString() : String(val),
                  'Inertia (SSE)',
                ]}
                labelFormatter={(k) => `Clusters (k): ${k}`}
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderRadius: '6px',
                  border: 'none',
                  color: '#f8fafc',
                  fontSize: '11px',
                }}
              />
              <Legend verticalAlign="top" height={24} iconType="circle" />
              <Line
                type="monotone"
                dataKey="inertia"
                name="Inertia (SSE)"
                stroke="#4f46e5"
                strokeWidth={2.5}
                dot={{ r: 4, fill: '#4f46e5' }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 2. Silhouette Score */}
      <div className="bg-slate-50/70 p-3 rounded-lg border border-slate-200/60">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs font-bold text-slate-800">Silhouette Score Analysis</span>
          <span className="text-[11px] text-emerald-600 font-semibold">Optimal k = 3 (0.395)</span>
        </div>
        <div style={{ width: '100%', height }}>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data} margin={{ top: 10, right: 15, left: 15, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" vertical={false} />
              <XAxis dataKey="k" stroke="#64748b" fontSize={11} tickLine={false} />
              <YAxis
                stroke="#64748b"
                fontSize={11}
                tickLine={false}
                axisLine={false}
                domain={[0.2, 0.45]}
                tickFormatter={(val: number) => val.toFixed(2)}
              />
              <Tooltip
                formatter={(val: unknown) => [
                  typeof val === 'number' ? val.toFixed(4) : String(val),
                  'Silhouette Score',
                ]}
                labelFormatter={(k) => `Clusters (k): ${k}`}
                contentStyle={{
                  backgroundColor: '#0f172a',
                  borderRadius: '6px',
                  border: 'none',
                  color: '#f8fafc',
                  fontSize: '11px',
                }}
              />
              <Legend verticalAlign="top" height={24} iconType="circle" />
              <Line
                type="monotone"
                dataKey="silhouette_score"
                name="Silhouette Score"
                stroke="#059669"
                strokeWidth={2.5}
                dot={{ r: 4, fill: '#059669' }}
                activeDot={{ r: 6 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};
