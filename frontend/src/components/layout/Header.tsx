import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { Activity, Menu } from 'lucide-react';

const titleMap: Record<string, { title: string; subtitle: string }> = {
  '/dashboard': {
    title: 'Dashboard Overview',
    subtitle: 'High-level business KPIs, monthly revenue trend, and geographic distribution',
  },
  '/sales': {
    title: 'Sales Performance',
    subtitle: 'Detailed analysis of monthly revenue, top items, and invoice transactions',
  },
  '/customers': {
    title: 'Customer Directory & RFM',
    subtitle: 'Behavioral metrics: Recency, Frequency, Monetary and membership tiers',
  },
  '/segmentation': {
    title: 'Customer Segmentation',
    subtitle: 'Unsupervised K-Means clustering profiles, evaluation metrics, and distribution',
  },
  '/statistics': {
    title: 'Statistical Hypothesis Tests',
    subtitle: 'Rigorous empirical evaluation and hypothesis testing on transaction patterns',
  },
};

interface HeaderProps {
  onToggleSidebar?: () => void;
}

export const Header: React.FC<HeaderProps> = ({ onToggleSidebar }) => {
  const location = useLocation();
  const [backendHealthy, setBackendHealthy] = useState<boolean | null>(null);

  useEffect(() => {
    const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    const healthUrl = apiBase.replace(/\/api\/v1\/?$/, '/health');

    const checkHealth = async () => {
      try {
        const res = await axios.get(healthUrl, { timeout: 3000 });
        setBackendHealthy(res.data?.status === 'ok');
      } catch {
        setBackendHealthy(false);
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  // Customer detail page fallback title
  const isCustomerDetail = location.pathname.startsWith('/customers/');
  const currentMeta = isCustomerDetail
    ? {
        title: 'Customer Profile',
        subtitle: 'Granular RFM metrics and assigned behavioral membership cluster',
      }
    : titleMap[location.pathname] || {
        title: 'Online Retail Analytics',
        subtitle: 'Data Analysis for Business Environment',
      };

  return (
    <header className="h-16 bg-white border-b border-slate-200/80 px-4 sm:px-8 flex items-center justify-between shrink-0 sticky top-0 z-30 shadow-2xs">
      <div className="flex items-center gap-3">
        {onToggleSidebar && (
          <button
            onClick={onToggleSidebar}
            type="button"
            className="lg:hidden p-2 text-slate-600 hover:text-slate-900 rounded-lg hover:bg-slate-100 transition"
            aria-label="Toggle Navigation Menu"
          >
            <Menu className="w-5 h-5" />
          </button>
        )}
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 leading-tight">
            {currentMeta.title}
          </h2>
          <p className="text-xs text-slate-500 hidden sm:block">{currentMeta.subtitle}</p>
        </div>
      </div>

      {/* Backend API Status Indicator */}
      <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-full text-xs">
        <Activity className="w-3.5 h-3.5 text-slate-500" />
        <span className="text-slate-600 font-medium hidden md:inline">Backend API:</span>
        <span className="flex items-center gap-1.5">
          <span
            className={`w-2 h-2 rounded-full ${
              backendHealthy === null
                ? 'bg-amber-400 animate-pulse'
                : backendHealthy
                ? 'bg-emerald-500'
                : 'bg-rose-500'
            }`}
          />
          <span
            className={`font-semibold ${
              backendHealthy === null
                ? 'text-amber-700'
                : backendHealthy
                ? 'text-emerald-700'
                : 'text-rose-700'
            }`}
          >
            {backendHealthy === null ? 'Checking...' : backendHealthy ? 'Online' : 'Offline'}
          </span>
        </span>
      </div>
    </header>
  );
};
