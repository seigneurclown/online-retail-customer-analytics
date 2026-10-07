import React, { useState } from 'react';
import {
  Package,
  Globe2,
  Receipt,
  Search,
  CheckCircle2,
  XCircle,
} from 'lucide-react';
import { useSales } from '../../hooks/useSales';
import { PageHeader, Pagination, Badge, LoadingState } from '../../components/common';
import { ChartCard } from '../../components/cards';
import { DataTable, type Column } from '../../components/tables';
import { MonthlyBreakdownChart } from '../../components/charts';
import { formatCurrency } from '../../utils/formatCurrency';
import { formatNumber, formatPercent } from '../../utils/formatNumber';
import { formatDate } from '../../utils/formatDate';
import type { ProductSalesItem, CountrySalesItem, InvoiceItem } from '../../types/sales';

type ActiveTab = 'products' | 'countries' | 'invoices';

export const SalesPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<ActiveTab>('products');
  const {
    monthlySales,
    loadingMonthly,
    selectedYear,
    setSelectedYear,
    countriesData,
    loadingCountries,
    countriesPage: _countriesPage,
    setCountriesPage,
    countrySearch,
    setCountrySearch,
    productsData,
    loadingProducts,
    setProductsPage,
    productSearch,
    setProductSearch,
    invoicesData,
    loadingInvoices,
    invoiceParams,
    setInvoiceParams,
    setInvoicePage,
  } = useSales();

  // Columns for Products Table
  const productColumns: Column<ProductSalesItem>[] = [
    {
      key: 'stock_code',
      header: 'Stock Code',
      render: (p) => (
        <span className="font-mono font-semibold text-slate-800 bg-slate-100 px-2 py-0.5 rounded text-xs">
          {p.stock_code}
        </span>
      ),
    },
    {
      key: 'description',
      header: 'Description',
      render: (p) => (
        <span className="font-medium text-slate-900">{p.description || 'N/A'}</span>
      ),
    },
    {
      key: 'total_revenue',
      header: 'Total Revenue',
      align: 'right',
      render: (p) => (
        <span className="font-bold text-slate-900">{formatCurrency(p.total_revenue)}</span>
      ),
    },
    {
      key: 'total_quantity',
      header: 'Units Sold',
      align: 'right',
      render: (p) => <span>{formatNumber(p.total_quantity)}</span>,
    },
    {
      key: 'order_count',
      header: 'Invoices',
      align: 'right',
      render: (p) => <span>{formatNumber(p.order_count)}</span>,
    },
  ];

  // Columns for Country Table
  const countryColumns: Column<CountrySalesItem>[] = [
    {
      key: 'country',
      header: 'Destination Country',
      render: (c) => <span className="font-bold text-slate-900">{c.country}</span>,
    },
    {
      key: 'total_revenue',
      header: 'Net Revenue',
      align: 'right',
      render: (c) => (
        <span className="font-bold text-indigo-700">{formatCurrency(c.total_revenue)}</span>
      ),
    },
    {
      key: 'percentage_share',
      header: 'Market Share',
      align: 'right',
      render: (c) => (
        <Badge variant={c.percentage_share > 5 ? 'info' : 'default'}>
          {formatPercent(c.percentage_share)}
        </Badge>
      ),
    },
    {
      key: 'invoice_count',
      header: 'Total Invoices',
      align: 'right',
      render: (c) => <span>{formatNumber(c.invoice_count)}</span>,
    },
    {
      key: 'customer_count',
      header: 'Unique Buyers',
      align: 'right',
      render: (c) => <span>{formatNumber(c.customer_count)}</span>,
    },
  ];

  // Columns for Invoices Table
  const invoiceColumns: Column<InvoiceItem>[] = [
    {
      key: 'invoice_no',
      header: 'Invoice No',
      render: (inv) => (
        <span className="font-mono font-semibold text-slate-900">{inv.invoice_no}</span>
      ),
    },
    {
      key: 'invoice_date',
      header: 'Date',
      render: (inv) => <span className="text-slate-600">{formatDate(inv.invoice_date)}</span>,
    },
    {
      key: 'customer_id',
      header: 'Customer ID',
      render: (inv) =>
        inv.customer_id ? (
          <span className="font-mono text-indigo-600 font-medium">#{inv.customer_id}</span>
        ) : (
          <span className="text-slate-400 italic">Guest</span>
        ),
    },
    {
      key: 'country',
      header: 'Country',
      render: (inv) => <span className="text-slate-700">{inv.country}</span>,
    },
    {
      key: 'is_cancelled',
      header: 'Status',
      render: (inv) =>
        inv.is_cancelled ? (
          <span className="inline-flex items-center gap-1 text-xs text-rose-700 font-semibold bg-rose-50 px-2 py-0.5 rounded-full border border-rose-200">
            <XCircle className="w-3.5 h-3.5" />
            Cancelled
          </span>
        ) : (
          <span className="inline-flex items-center gap-1 text-xs text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Completed
          </span>
        ),
    },
    {
      key: 'item_count',
      header: 'SKUs',
      align: 'right',
      render: (inv) => <span>{formatNumber(inv.item_count)}</span>,
    },
    {
      key: 'total_quantity',
      header: 'Quantity',
      align: 'right',
      render: (inv) => <span>{formatNumber(inv.total_quantity)}</span>,
    },
    {
      key: 'invoice_value',
      header: 'Total Value',
      align: 'right',
      render: (inv) => (
        <span
          className={`font-bold ${
            inv.invoice_value < 0 ? 'text-rose-600' : 'text-slate-900'
          }`}
        >
          {formatCurrency(inv.invoice_value)}
        </span>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header & Year Filter */}
      <PageHeader
        title="Sales Performance Analysis"
        subtitle="Monthly revenue breakdowns, product catalogues, country performance, and transactional ledger"
        action={
          <div className="inline-flex p-1 bg-slate-200/80 rounded-lg text-xs font-semibold text-slate-700">
            <button
              onClick={() => setSelectedYear(undefined)}
              type="button"
              className={`px-3 py-1.5 rounded-md transition cursor-pointer ${
                selectedYear === undefined
                  ? 'bg-white text-indigo-600 shadow-2xs font-bold'
                  : 'hover:text-slate-900'
              }`}
            >
              All Years
            </button>
            <button
              onClick={() => setSelectedYear(2010)}
              type="button"
              className={`px-3 py-1.5 rounded-md transition cursor-pointer ${
                selectedYear === 2010
                  ? 'bg-white text-indigo-600 shadow-2xs font-bold'
                  : 'hover:text-slate-900'
              }`}
            >
              2010
            </button>
            <button
              onClick={() => setSelectedYear(2011)}
              type="button"
              className={`px-3 py-1.5 rounded-md transition cursor-pointer ${
                selectedYear === 2011
                  ? 'bg-white text-indigo-600 shadow-2xs font-bold'
                  : 'hover:text-slate-900'
              }`}
            >
              2011
            </button>
          </div>
        }
      />

      {/* Section 1: Monthly Breakdown Chart */}
      <ChartCard
        title={`Monthly Financial Performance ${selectedYear ? `(${selectedYear})` : '(Full Period)'}`}
        subtitle="Gross revenue, cancellation deductions, and net retained earnings"
      >
        {loadingMonthly ? (
          <LoadingState type="chart" message="Loading monthly breakdown..." />
        ) : (
          <MonthlyBreakdownChart data={monthlySales} height={300} />
        )}
      </ChartCard>

      {/* Section 2: Tabbed Exploration */}
      <div className="space-y-4">
        {/* Navigation Tabs */}
        <div className="border-b border-slate-200 flex gap-4">
          <button
            onClick={() => setActiveTab('products')}
            type="button"
            className={`pb-3 text-sm font-semibold flex items-center gap-2 border-b-2 transition cursor-pointer ${
              activeTab === 'products'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            <Package className="w-4 h-4" />
            <span>Product Catalogue ({productsData.total.toLocaleString()})</span>
          </button>

          <button
            onClick={() => setActiveTab('countries')}
            type="button"
            className={`pb-3 text-sm font-semibold flex items-center gap-2 border-b-2 transition cursor-pointer ${
              activeTab === 'countries'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            <Globe2 className="w-4 h-4" />
            <span>Markets & Geography ({countriesData.total.toLocaleString()})</span>
          </button>

          <button
            onClick={() => setActiveTab('invoices')}
            type="button"
            className={`pb-3 text-sm font-semibold flex items-center gap-2 border-b-2 transition cursor-pointer ${
              activeTab === 'invoices'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-slate-500 hover:text-slate-700'
            }`}
          >
            <Receipt className="w-4 h-4" />
            <span>Invoice Ledger ({invoicesData.total.toLocaleString()})</span>
          </button>
        </div>

        {/* Tab 1: Products */}
        {activeTab === 'products' && (
          <div className="space-y-3">
            {/* Search Bar */}
            <div className="flex items-center gap-2 max-w-sm">
              <div className="relative flex-1">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={productSearch}
                  onChange={(e) => {
                    setProductSearch(e.target.value);
                    setProductsPage(1);
                  }}
                  placeholder="Search SKU or description..."
                  className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-xs placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition"
                />
              </div>
            </div>

            {/* Table */}
            <DataTable
              columns={productColumns}
              data={productsData.items}
              keyExtractor={(item) => item.stock_code}
              loading={loadingProducts}
              emptyTitle="No products match your search"
              emptyMessage="Try searching with a different SKU code or product description."
            />

            {/* Pagination */}
            <Pagination
              currentPage={productsData.page}
              totalPages={productsData.total_pages}
              totalItems={productsData.total}
              pageSize={productsData.page_size}
              onPageChange={setProductsPage}
            />
          </div>
        )}

        {/* Tab 2: Countries */}
        {activeTab === 'countries' && (
          <div className="space-y-3">
            {/* Search */}
            <div className="flex items-center gap-2 max-w-sm">
              <div className="relative flex-1">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={countrySearch}
                  onChange={(e) => {
                    setCountrySearch(e.target.value);
                    setCountriesPage(1);
                  }}
                  placeholder="Search country..."
                  className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-xs placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition"
                />
              </div>
            </div>

            <DataTable
              columns={countryColumns}
              data={countriesData.items}
              keyExtractor={(item) => item.country}
              loading={loadingCountries}
              emptyTitle="No country revenue data"
              emptyMessage="No country matches your search filter."
            />

            <Pagination
              currentPage={countriesData.page}
              totalPages={countriesData.total_pages}
              totalItems={countriesData.total}
              pageSize={countriesData.page_size}
              onPageChange={setCountriesPage}
            />
          </div>
        )}

        {/* Tab 3: Invoices */}
        {activeTab === 'invoices' && (
          <div className="space-y-3">
            {/* Filters Bar */}
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
              {/* Search */}
              <div className="relative flex-1 max-w-xs">
                <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={invoiceParams.search || ''}
                  onChange={(e) =>
                    setInvoiceParams((prev) => ({ ...prev, search: e.target.value, page: 1 }))
                  }
                  placeholder="Invoice No or Customer ID..."
                  className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-xs placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition"
                />
              </div>

              {/* Status Filter */}
              <select
                value={
                  invoiceParams.is_cancelled === undefined
                    ? 'all'
                    : invoiceParams.is_cancelled
                    ? 'cancelled'
                    : 'completed'
                }
                onChange={(e) => {
                  const val = e.target.value;
                  setInvoiceParams((prev) => ({
                    ...prev,
                    page: 1,
                    is_cancelled: val === 'all' ? undefined : val === 'cancelled',
                  }));
                }}
                className="px-3 py-2 bg-white border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition"
              >
                <option value="all">All Statuses</option>
                <option value="completed">Completed Only</option>
                <option value="cancelled">Cancelled Only</option>
              </select>

              {/* Reset Filter Button */}
              {(invoiceParams.search || invoiceParams.is_cancelled !== undefined) && (
                <button
                  onClick={() =>
                    setInvoiceParams({
                      page: 1,
                      page_size: 15,
                      country: undefined,
                      is_cancelled: undefined,
                      search: '',
                    })
                  }
                  type="button"
                  className="text-xs text-slate-500 hover:text-slate-800 underline transition cursor-pointer"
                >
                  Clear Filters
                </button>
              )}
            </div>

            {/* Invoices Table */}
            <DataTable
              columns={invoiceColumns}
              data={invoicesData.items}
              keyExtractor={(item) => item.invoice_no}
              loading={loadingInvoices}
              emptyTitle="No invoices found"
              emptyMessage="No transaction orders meet the selected filter criteria."
            />

            {/* Pagination */}
            <Pagination
              currentPage={invoicesData.page}
              totalPages={invoicesData.total_pages}
              totalItems={invoicesData.total}
              pageSize={invoicesData.page_size}
              onPageChange={setInvoicePage}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default SalesPage;
