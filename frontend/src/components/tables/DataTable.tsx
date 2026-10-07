import React from 'react';
import { LoadingState } from '../common/LoadingState';
import { EmptyState } from '../common/EmptyState';

export interface Column<T> {
  key: string;
  header: string;
  render?: (row: T, index: number) => React.ReactNode;
  align?: 'left' | 'center' | 'right';
  className?: string;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (row: T, index: number) => string | number;
  loading?: boolean;
  emptyTitle?: string;
  emptyMessage?: string;
  onRowClick?: (row: T) => void;
  className?: string;
}

export function DataTable<T>({
  columns,
  data,
  keyExtractor,
  loading = false,
  emptyTitle = 'No records found',
  emptyMessage = 'There is no data to display.',
  onRowClick,
  className = '',
}: DataTableProps<T>) {
  if (loading) {
    return <LoadingState type="table" rows={6} />;
  }

  if (data.length === 0) {
    return <EmptyState title={emptyTitle} message={emptyMessage} />;
  }

  const getAlignClass = (align?: 'left' | 'center' | 'right') => {
    switch (align) {
      case 'right':
        return 'text-right justify-end';
      case 'center':
        return 'text-center justify-center';
      default:
        return 'text-left justify-start';
    }
  };

  return (
    <div
      className={`bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden ${className}`}
    >
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse text-xs">
          <thead>
            <tr className="bg-slate-50/80 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
              {columns.map((col) => (
                <th
                  key={col.key}
                  className={`py-3 px-4 ${getAlignClass(col.align)} ${col.className || ''}`}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-slate-700">
            {data.map((row, index) => (
              <tr
                key={keyExtractor(row, index)}
                onClick={() => onRowClick && onRowClick(row)}
                className={`transition-colors ${
                  onRowClick
                    ? 'hover:bg-indigo-50/40 cursor-pointer'
                    : 'hover:bg-slate-50/60'
                }`}
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={`py-3 px-4 ${getAlignClass(col.align)} ${col.className || ''}`}
                  >
                    {col.render
                      ? col.render(row, index)
                      : String((row as Record<string, unknown>)[col.key] ?? '')}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
