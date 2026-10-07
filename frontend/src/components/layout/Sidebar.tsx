import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  TrendingUp,
  Users,
  PieChart,
  FlaskConical,
  ShoppingBag,
  X,
} from 'lucide-react';

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

const navigationItems = [
  { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard },
  { name: 'Sales Analysis', path: '/sales', icon: TrendingUp },
  { name: 'Customers & RFM', path: '/customers', icon: Users },
  { name: 'Segmentation', path: '/segmentation', icon: PieChart },
  { name: 'Statistical Tests', path: '/statistics', icon: FlaskConical },
];

export const Sidebar: React.FC<SidebarProps> = ({ isOpen = false, onClose }) => {
  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs z-40 lg:hidden transition-opacity"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-slate-900 text-slate-300 flex flex-col shrink-0 min-h-screen border-r border-slate-800 transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 flex items-center justify-between px-6 border-b border-slate-800 bg-slate-950/40">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-600 rounded-lg text-white shadow-xs">
              <ShoppingBag className="w-5 h-5" />
            </div>
            <div>
              <h1 className="font-bold text-white text-sm tracking-wide">Online Retail</h1>
              <p className="text-xs text-slate-400">Analytics Platform</p>
            </div>
          </div>

          {/* Close button for mobile */}
          {onClose && (
            <button
              onClick={onClose}
              type="button"
              aria-label="Close navigation sidebar"
              className="lg:hidden p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                onClick={onClose}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? 'bg-indigo-600 text-white font-semibold shadow-xs'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`
                }
              >
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.name}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* Footer Info */}
        <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
          <div className="flex items-center gap-2 mb-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            <span className="font-medium text-slate-400">UCI Online Retail</span>
          </div>
          <p className="text-[11px] text-slate-500">FastAPI &bull; MongoDB &bull; React</p>
        </div>
      </aside>
    </>
  );
};
