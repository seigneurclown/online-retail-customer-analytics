import React, { useState, useEffect } from 'react';
import {
  Database,
  UploadCloud,
  CheckCircle2,
  AlertCircle,
  Loader2,
  RefreshCw,
  FileSpreadsheet,
  X,
  Sparkles,
} from 'lucide-react';
import { systemApi, type SystemStatus, type SeedResult } from '../../services/systemApi';

interface DataManagementModalProps {
  isOpen: boolean;
  onClose: () => void;
  onDataChanged?: () => void;
}

export const DataManagementModal: React.FC<DataManagementModalProps> = ({
  isOpen,
  onClose,
  onDataChanged,
}) => {
  const [activeTab, setActiveTab] = useState<'seed' | 'upload'>('seed');
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loadingStatus, setLoadingStatus] = useState(false);
  const [seeding, setSeeding] = useState(false);
  const [seedResult, setSeedResult] = useState<SeedResult | null>(null);
  const [seedError, setSeedError] = useState<string | null>(null);

  // Upload state
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [collectionType, setCollectionType] = useState('invoices');
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<string | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const fetchStatus = async () => {
    try {
      setLoadingStatus(true);
      const data = await systemApi.getStatus();
      setStatus(data);
    } catch {
      setStatus({
        connected: false,
        database_name: 'unknown',
        has_seed_files: false,
        total_records: 0,
        collections: {},
        error: 'Không thể kết nối Backend',
      });
    } finally {
      setLoadingStatus(false);
    }
  };

  useEffect(() => {
    if (isOpen) {
      fetchStatus();
      setSeedResult(null);
      setSeedError(null);
      setUploadResult(null);
      setUploadError(null);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSeed = async () => {
    try {
      setSeeding(true);
      setSeedError(null);
      setSeedResult(null);
      const res = await systemApi.seedDatabase();
      setSeedResult(res);
      await fetchStatus();
      if (onDataChanged) onDataChanged();
    } catch (err: any) {
      setSeedError(err.message || 'Lỗi khi nạp dữ liệu');
    } finally {
      setSeeding(false);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!uploadFile) return;

    try {
      setUploading(true);
      setUploadError(null);
      setUploadResult(null);
      const res = await systemApi.uploadCsv(uploadFile, collectionType);
      setUploadResult(res.message);
      setUploadFile(null);
      await fetchStatus();
      if (onDataChanged) onDataChanged();
    } catch (err: any) {
      setUploadError(err.message || 'Lỗi khi tải file lên');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in duration-200">
      <div className="bg-white rounded-2xl shadow-2xl border border-slate-200 w-full max-w-2xl max-h-[90vh] flex flex-col overflow-hidden">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
          <div className="flex items-center gap-2.5">
            <div className="p-2 bg-indigo-100 text-indigo-600 rounded-xl">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-slate-900">Quản lý & Nạp dữ liệu</h3>
              <p className="text-xs text-slate-500">Cơ sở dữ liệu MongoDB Atlas (Cloud)</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Database Status Bar */}
        <div className="px-6 py-3 bg-slate-50 border-b border-slate-200/80 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2">
            <span
              className={`w-2.5 h-2.5 rounded-full ${
                status?.connected ? 'bg-emerald-500 ring-2 ring-emerald-200' : 'bg-rose-500 ring-2 ring-rose-200'
              }`}
            />
            <span className="font-medium text-slate-700">
              MongoDB: <strong className="text-slate-900">{status?.database_name || '...'}</strong>
            </span>
            <span className="text-slate-400">|</span>
            <span className="text-slate-600">
              Tổng số bản ghi: <strong className="text-indigo-600 font-semibold">{status?.total_records?.toLocaleString() || 0}</strong>
            </span>
          </div>
          <button
            onClick={fetchStatus}
            disabled={loadingStatus}
            className="flex items-center gap-1 text-slate-500 hover:text-indigo-600 transition"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loadingStatus ? 'animate-spin' : ''}`} />
            <span>Làm mới</span>
          </button>
        </div>

        {/* Tabs */}
        <div className="flex border-b border-slate-200 px-6 bg-white">
          <button
            onClick={() => setActiveTab('seed')}
            className={`py-3 px-4 text-xs font-semibold border-b-2 transition flex items-center gap-1.5 ${
              activeTab === 'seed'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Sparkles className="w-3.5 h-3.5" />
            Nạp dữ liệu mẫu 1-Click
          </button>
          <button
            onClick={() => setActiveTab('upload')}
            className={`py-3 px-4 text-xs font-semibold border-b-2 transition flex items-center gap-1.5 ${
              activeTab === 'upload'
                ? 'border-indigo-600 text-indigo-600'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <UploadCloud className="w-3.5 h-3.5" />
            Tải lên file CSV thủ công
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-4">
          {activeTab === 'seed' && (
            <div className="space-y-4">
              <div className="p-4 bg-indigo-50/70 border border-indigo-100 rounded-xl text-xs text-indigo-900 space-y-2">
                <p className="font-semibold text-indigo-950 flex items-center gap-1.5">
                  <FileSpreadsheet className="w-4 h-4 text-indigo-600" />
                  Gói dữ liệu phân tích bán lẻ chuẩn:
                </p>
                <ul className="list-disc list-inside space-y-1 text-indigo-800 pl-1">
                  <li><strong>4,372 Khách hàng</strong> & Phân cụm RFM (Recency, Frequency, Monetary)</li>
                  <li><strong>23,797 Hóa đơn</strong> giao dịch mua sắm chi tiết</li>
                  <li><strong>Phân cụm K-Means</strong> (VIP, Loyal, Potential, At-Risk...)</li>
                  <li><strong>Báo cáo doanh thu</strong> theo từng tháng & quốc gia</li>
                </ul>
              </div>

              {/* Seed Button */}
              <div className="pt-2 flex flex-col items-center justify-center text-center space-y-3">
                <button
                  onClick={handleSeed}
                  disabled={seeding}
                  className="w-full sm:w-auto px-8 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 text-white font-semibold text-sm rounded-xl shadow-md hover:shadow-lg transition flex items-center justify-center gap-2"
                >
                  {seeding ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Đang nạp dữ liệu lên MongoDB Atlas...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4" />
                      <span>Bắt đầu nạp toàn bộ dữ liệu mẫu</span>
                    </>
                  )}
                </button>
                <p className="text-[11px] text-slate-500">
                  Quá trình sẽ nạp trực tiếp vào Cloud Atlas trong khoảng 10 - 20 giây.
                </p>
              </div>

              {/* Success Result */}
              {seedResult && (
                <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 space-y-2 animate-in fade-in">
                  <div className="flex items-center gap-2 font-bold text-emerald-900">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                    <span>{seedResult.message}</span>
                  </div>
                  <p className="text-[11px] text-emerald-700">
                    Thời gian hoàn thành: <strong>{seedResult.duration_seconds}s</strong>
                  </p>
                  {seedResult.summary && (
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-1">
                      {Object.entries(seedResult.summary).map(([key, val]) => (
                        <div key={key} className="bg-white/80 p-1.5 rounded border border-emerald-100 flex justify-between">
                          <span className="text-slate-600 truncate">{key}:</span>
                          <strong className="text-emerald-700 font-mono">{val}</strong>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}

              {/* Error Alert */}
              {seedError && (
                <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-start gap-2 animate-in fade-in">
                  <AlertCircle className="w-4 h-4 text-rose-600 shrink-0 mt-0.5" />
                  <div>
                    <strong className="font-bold">Nạp dữ liệu không thành công:</strong>
                    <p className="mt-0.5">{seedError}</p>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'upload' && (
            <form onSubmit={handleUpload} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Loại bảng dữ liệu (Collection):
                </label>
                <select
                  value={collectionType}
                  onChange={(e) => setCollectionType(e.target.value)}
                  className="w-full text-xs px-3 py-2 border border-slate-300 rounded-lg focus:outline-hidden focus:ring-2 focus:ring-indigo-500 bg-white"
                >
                  <option value="invoices">Hóa đơn giao dịch (invoices)</option>
                  <option value="segments">Phân cụm khách hàng (customer_segments)</option>
                  <option value="generic">Dữ liệu tùy chỉnh khác</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Chọn file CSV từ máy tính:
                </label>
                <input
                  type="file"
                  accept=".csv"
                  onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
                  className="w-full text-xs text-slate-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-xs file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer border border-slate-200 rounded-lg p-2"
                />
              </div>

              <button
                type="submit"
                disabled={!uploadFile || uploading}
                className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-300 text-white font-semibold text-xs rounded-lg transition flex items-center justify-center gap-1.5"
              >
                {uploading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Đang nạp file lên database...</span>
                  </>
                ) : (
                  <>
                    <UploadCloud className="w-4 h-4" />
                    <span>Tải lên & Nạp vào Database</span>
                  </>
                )}
              </button>

              {uploadResult && (
                <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-xs text-emerald-800 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{uploadResult}</span>
                </div>
              )}

              {uploadError && (
                <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg text-xs text-rose-800 flex items-center gap-2">
                  <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                  <span>{uploadError}</span>
                </div>
              )}
            </form>
          )}
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3.5 bg-slate-50 border-t border-slate-200 flex items-center justify-between">
          <span className="text-[11px] text-slate-400">Online Retail Analytics Platform</span>
          <div className="flex gap-2">
            {seedResult && (
              <button
                type="button"
                onClick={() => window.location.reload()}
                className="px-4 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold rounded-lg transition flex items-center gap-1 shadow-xs"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Xem Dashboard ngay</span>
              </button>
            )}
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-1.5 border border-slate-300 hover:bg-slate-100 text-slate-700 text-xs font-medium rounded-lg transition"
            >
              Đóng
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
