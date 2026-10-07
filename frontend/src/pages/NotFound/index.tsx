import { Link } from 'react-router-dom';

export const NotFoundPage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[50vh] text-center p-6 bg-white rounded-xl border border-slate-200 shadow-sm">
      <h1 className="text-6xl font-extrabold text-slate-300">404</h1>
      <p className="text-xl font-semibold text-slate-700 mt-4">Page Not Found</p>
      <p className="text-slate-500 mt-2">The page you are looking for does not exist or has been moved.</p>
      <Link
        to="/dashboard"
        className="mt-6 px-4 py-2 bg-indigo-600 text-white text-sm font-medium rounded-lg hover:bg-indigo-700 transition"
      >
        Return to Dashboard
      </Link>
    </div>
  );
};
export default NotFoundPage;
