import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export function formatApiErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      const detail = error.response.data?.detail;
      if (typeof detail === 'string') return detail;
      if (Array.isArray(detail)) {
        return detail
          .map((d: { msg?: string; loc?: (string | number)[] }) =>
            d.msg || `${d.loc?.join('.')}: Invalid input`
          )
          .join('; ');
      }
      return `Server returned HTTP ${error.response.status}`;
    }
    if (error.request) {
      return 'Cannot reach backend server (http://localhost:8000). Please verify FastAPI is running.';
    }
    return error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return 'An unexpected network error occurred.';
}

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = formatApiErrorMessage(error);
    if (import.meta.env.DEV) {
      console.error(`[API Error] ${error.config?.url}:`, message);
    }
    return Promise.reject(new Error(message));
  }
);

