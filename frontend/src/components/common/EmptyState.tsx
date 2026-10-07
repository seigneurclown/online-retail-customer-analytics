import React from 'react';
import { Inbox, RotateCcw } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  message?: string;
  onReset?: () => void;
  actionText?: string;
  className?: string;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No records found',
  message = 'There is no data matching your current filter criteria.',
  onReset,
  actionText = 'Reset Filters',
  className = '',
}) => {
  return (
    <div
      className={`p-10 bg-white border border-slate-200 rounded-xl text-center flex flex-col items-center justify-center ${className}`}
    >
      <div className="w-12 h-12 bg-slate-100 text-slate-400 rounded-full flex items-center justify-center mb-3">
        <Inbox className="w-6 h-6" />
      </div>
      <h3 className="text-sm font-semibold text-slate-800">{title}</h3>
      <p className="text-xs text-slate-500 mt-1 max-w-sm">{message}</p>
      {onReset && (
        <button
          onClick={onReset}
          type="button"
          className="mt-4 inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-medium transition cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>{actionText}</span>
        </button>
      )}
    </div>
  );
};
