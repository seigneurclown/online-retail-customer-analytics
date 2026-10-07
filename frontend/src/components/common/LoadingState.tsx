import React from 'react';

interface LoadingStateProps {
  message?: string;
  rows?: number;
  type?: 'card' | 'table' | 'chart' | 'generic';
}

export const LoadingState: React.FC<LoadingStateProps> = ({
  message = 'Loading analytics data...',
  rows = 4,
  type = 'generic',
}) => {
  if (type === 'card') {
    return (
      <div className="bg-white p-6 rounded-xl border border-slate-200 animate-pulse">
        <div className="h-4 bg-slate-200 rounded w-1/3 mb-4"></div>
        <div className="h-8 bg-slate-200 rounded w-2/3 mb-2"></div>
        <div className="h-3 bg-slate-100 rounded w-1/2"></div>
      </div>
    );
  }

  if (type === 'chart') {
    return (
      <div className="bg-white p-6 rounded-xl border border-slate-200 animate-pulse">
        <div className="h-5 bg-slate-200 rounded w-1/4 mb-2"></div>
        <div className="h-4 bg-slate-100 rounded w-1/3 mb-6"></div>
        <div className="h-64 bg-slate-100 rounded flex items-center justify-center">
          <span className="text-xs text-slate-400 font-medium">{message}</span>
        </div>
      </div>
    );
  }

  if (type === 'table') {
    return (
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden animate-pulse">
        <div className="p-4 border-b border-slate-100 flex justify-between">
          <div className="h-5 bg-slate-200 rounded w-1/4"></div>
          <div className="h-5 bg-slate-100 rounded w-16"></div>
        </div>
        <div className="divide-y divide-slate-100">
          {Array.from({ length: rows }).map((_, i) => (
            <div key={i} className="p-4 flex gap-4">
              <div className="h-4 bg-slate-100 rounded flex-1"></div>
              <div className="h-4 bg-slate-200 rounded flex-1"></div>
              <div className="h-4 bg-slate-100 rounded flex-1"></div>
              <div className="h-4 bg-slate-200 rounded w-20"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center p-12 bg-white rounded-xl border border-slate-200">
      <div className="w-8 h-8 border-3 border-indigo-600 border-t-transparent rounded-full animate-spin"></div>
      <p className="mt-3 text-sm text-slate-500 font-medium">{message}</p>
    </div>
  );
};
