import React, { lazy, Suspense } from 'react';
import { createBrowserRouter, RouterProvider, Navigate } from 'react-router-dom';
import { AppLayout } from '../components/layout/AppLayout';
import { LoadingState } from '../components/common/LoadingState';

const DashboardPage = lazy(() => import('../pages/Dashboard'));
const SalesPage = lazy(() => import('../pages/Sales'));
const CustomersPage = lazy(() => import('../pages/Customers'));
const CustomerDetailPage = lazy(() => import('../pages/Customers/CustomerDetailPage'));
const SegmentationPage = lazy(() => import('../pages/Segmentation'));
const StatisticsPage = lazy(() => import('../pages/Statistics'));
const NotFoundPage = lazy(() => import('../pages/NotFound'));

function SuspenseWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Suspense fallback={<LoadingState message="Loading analytics module..." />}>
      {children}
    </Suspense>
  );
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      {
        path: 'dashboard',
        element: (
          <SuspenseWrapper>
            <DashboardPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'sales',
        element: (
          <SuspenseWrapper>
            <SalesPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'customers',
        element: (
          <SuspenseWrapper>
            <CustomersPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'customers/:customerId',
        element: (
          <SuspenseWrapper>
            <CustomerDetailPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'segmentation',
        element: (
          <SuspenseWrapper>
            <SegmentationPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: 'statistics',
        element: (
          <SuspenseWrapper>
            <StatisticsPage />
          </SuspenseWrapper>
        ),
      },
      {
        path: '*',
        element: (
          <SuspenseWrapper>
            <NotFoundPage />
          </SuspenseWrapper>
        ),
      },
    ],
  },
]);

export const AppRoutes: React.FC = () => {
  return <RouterProvider router={router} />;
};
