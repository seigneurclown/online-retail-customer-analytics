import React from 'react';
import { AlertCircle, RotateCcw } from 'lucide-react';

interface ErrorStateProps {
  title?: string;
  message?: string;
  onRetry?: () => void;
  className?: string;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  title = 'Unable to load data',
  message = 'An unexpected error occurred while fetching information from the server.',
  onRetry,
  className = '',
}) => {
  return (
    <div
      className={`p-6 bg-rose-50/70 border border-rose-200 rounded-xl text-center flex flex-col items-center justify-center ${className}`}
    >
      <div className="w-10 h-10 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center mb-3">
        <AlertCircle className="w-5 h-5" />
      </div>
      <h3 className="text-base font-semibold text-rose-900">{title}</h3>
      <p className="text-xs text-rose-700 mt-1 max-w-md">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          type="button"
          className="mt-4 inline-flex items-center gap-2 px-3.5 py-1.5 bg-white border border-rose-300 hover:bg-rose-50 text-rose-700 rounded-lg text-xs font-semibold shadow-xs transition cursor-pointer"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Retry</span>
        </button>
      )}
    </div>
  );
};
