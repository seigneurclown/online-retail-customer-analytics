import { useState, useEffect, useCallback } from 'react';
import { salesApi } from '../services/salesApi';
import type {
  MonthlySalesItem,
  ProductSalesItem,
  CountrySalesItem,
  InvoiceItem,
  InvoiceFilterParams,
} from '../types/sales';
import type { PaginatedResponse } from '../types/common';

export function useSales() {
  // Monthly sales state
  const [selectedYear, setSelectedYear] = useState<number | undefined>(undefined);
  const [monthlySales, setMonthlySales] = useState<MonthlySalesItem[]>([]);
  const [loadingMonthly, setLoadingMonthly] = useState<boolean>(true);
  const [monthlyError, setMonthlyError] = useState<string | null>(null);

  // Countries state (Paginated)
  const [countriesPage, setCountriesPage] = useState<number>(1);
  const [countrySearch, setCountrySearch] = useState<string>('');
  const [countriesData, setCountriesData] = useState<PaginatedResponse<CountrySalesItem>>({
    items: [],
    page: 1,
    page_size: 15,
    total: 0,
    total_pages: 0,
  });
  const [loadingCountries, setLoadingCountries] = useState<boolean>(true);
  const [countriesError, setCountriesError] = useState<string | null>(null);

  // Products state (Paginated)
  const [productsPage, setProductsPage] = useState<number>(1);
  const [productSearch, setProductSearch] = useState<string>('');
  const [productsData, setProductsData] = useState<PaginatedResponse<ProductSalesItem>>({
    items: [],
    page: 1,
    page_size: 15,
    total: 0,
    total_pages: 0,
  });
  const [loadingProducts, setLoadingProducts] = useState<boolean>(false);

  // Invoices state (Paginated + Filtered)
  const [invoiceParams, setInvoiceParams] = useState<InvoiceFilterParams>({
    page: 1,
    page_size: 15,
    country: undefined,
    is_cancelled: undefined,
    search: '',
  });
  const [invoicesData, setInvoicesData] = useState<PaginatedResponse<InvoiceItem>>({
    items: [],
    page: 1,
    page_size: 15,
    total: 0,
    total_pages: 0,
  });
  const [loadingInvoices, setLoadingInvoices] = useState<boolean>(false);

  // Trigger monthly when year changes
  useEffect(() => {
    let ignore = false;
    async function loadMonthly() {
      try {
        const data = await salesApi.getMonthlySales(selectedYear);
        if (!ignore) {
          setMonthlySales(data);
          setLoadingMonthly(false);
        }
      } catch (err: unknown) {
        if (!ignore) {
          setMonthlyError(err instanceof Error ? err.message : 'Failed to fetch monthly sales');
          setLoadingMonthly(false);
        }
      }
    }

    loadMonthly();

    return () => {
      ignore = true;
    };
  }, [selectedYear]);

  // Fetch countries
  const fetchCountries = useCallback(async (page: number, search?: string) => {
    setLoadingCountries(true);
    setCountriesError(null);
    try {
      const data = await salesApi.getCountries(page, 15, search || undefined);
      setCountriesData(data);
    } catch (err: unknown) {
      setCountriesError(
        err instanceof Error ? err.message : 'Failed to fetch country revenue'
      );
    } finally {
      setLoadingCountries(false);
    }
  }, []);

  // Trigger countries on page/search change
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchCountries(countriesPage, countrySearch);
    }, 250);
    return () => clearTimeout(timer);
  }, [countriesPage, countrySearch, fetchCountries]);

  // Fetch products
  const fetchProducts = useCallback(async (page: number, search?: string) => {
    setLoadingProducts(true);
    try {
      const data = await salesApi.getProducts(page, 15, search || undefined);
      setProductsData(data);
    } catch {
      // Handled via empty state or retry
    } finally {
      setLoadingProducts(false);
    }
  }, []);

  // Fetch invoices
  const fetchInvoices = useCallback(async (params: InvoiceFilterParams) => {
    setLoadingInvoices(true);
    try {
      const data = await salesApi.getInvoices(params);
      setInvoicesData(data);
    } catch {
      // Handled via empty state or retry
    } finally {
      setLoadingInvoices(false);
    }
  }, []);

  // Trigger products on page/search change
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchProducts(productsPage, productSearch);
    }, 250);
    return () => clearTimeout(timer);
  }, [productsPage, productSearch, fetchProducts]);

  // Trigger invoices on params change
  useEffect(() => {
    const timer = setTimeout(() => {
      fetchInvoices(invoiceParams);
    }, 250);
    return () => clearTimeout(timer);
  }, [invoiceParams, fetchInvoices]);

  return {
    // Monthly
    monthlySales,
    loadingMonthly,
    monthlyError,
    selectedYear,
    setSelectedYear,

    // Countries
    countriesData,
    loadingCountries,
    countriesError,
    countriesPage,
    setCountriesPage,
    countrySearch,
    setCountrySearch,

    // Products
    productsData,
    loadingProducts,
    productsPage,
    setProductsPage,
    productSearch,
    setProductSearch,

    // Invoices
    invoicesData,
    loadingInvoices,
    invoiceParams,
    setInvoiceParams,
    setInvoicePage: (page: number) =>
      setInvoiceParams((prev) => ({ ...prev, page })),
  };
}
