import React from 'react';

export type BadgeVariant = 'default' | 'success' | 'danger' | 'warning' | 'info' | 'gold' | 'silver';

interface BadgeProps {
  children: React.ReactNode;
  variant?: BadgeVariant;
  className?: string;
  size?: 'sm' | 'md';
}

const variantStyles: Record<BadgeVariant, string> = {
  default: 'bg-slate-100 text-slate-700 border-slate-200',
  success: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  danger: 'bg-rose-50 text-rose-700 border-rose-200',
  warning: 'bg-amber-50 text-amber-800 border-amber-200',
  info: 'bg-sky-50 text-sky-700 border-sky-200',
  gold: 'bg-amber-100 text-amber-900 border-amber-300 font-semibold',
  silver: 'bg-slate-200 text-slate-800 border-slate-300 font-semibold',
};

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  className = '',
  size = 'sm',
}) => {
  const sizeStyle = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-2.5 py-1 text-sm';
  return (
    <span
      className={`inline-flex items-center rounded-md border font-medium ${sizeStyle} ${variantStyles[variant]} ${className}`}
    >
      {children}
    </span>
  );
};
