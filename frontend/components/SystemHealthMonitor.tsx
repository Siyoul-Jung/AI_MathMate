import React, { useState, useEffect } from 'react';
import { api } from '../lib/api';

interface SystemHealthMonitorProps {
  isOpen: boolean;
  onClose: () => void;
}

const SystemHealthMonitor: React.FC<SystemHealthMonitorProps> = ({ isOpen, onClose }) => {
  const [stats, setStats] = useState<any>(null);
  const [failures, setFailures] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchData();
    }
  }, [isOpen]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const statsData = await api.fetchAmcStats();
      const failuresData = await api.fetchAmcFailures(10);
      setStats(statsData);
      setFailures(failuresData || []);
    } catch (error) {
      console.error('Failed to fetch health data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-300">
      <div className="bg-white w-full max-w-2xl rounded-[2.5rem] shadow-2xl overflow-hidden border border-slate-200 flex flex-col max-h-[90vh] animate-in zoom-in-95 duration-500">
        {/* Header */}
        <div className="p-8 bg-slate-900 text-white relative overflow-hidden">
          <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/20 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2"></div>
          <div className="relative z-10 flex justify-between items-center">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span className="text-[10px] font-black uppercase tracking-widest text-emerald-400">System Diagnostics</span>
              </div>
              <h2 className="text-3xl font-black tracking-tight">Backend Health</h2>
            </div>
            <button 
              onClick={onClose}
              className="h-10 w-10 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
            >
              <span className="text-xl">✕</span>
            </button>
          </div>
        </div>

        <div className="flex-grow overflow-y-auto p-8 custom-scrollbar">
          {loading ? (
            <div className="flex flex-col items-center justify-center h-64 gap-4">
              <div className="w-12 h-12 border-4 border-emerald-500 border-t-transparent rounded-full animate-spin"></div>
              <span className="text-sm font-bold text-slate-400">Analyzing System Vitals...</span>
            </div>
          ) : (
            <div className="space-y-8">
              {/* Stats Overview */}
              <div className="grid grid-cols-2 gap-4">
                <div className="p-6 rounded-3xl bg-emerald-50 border border-emerald-100 flex flex-col">
                  <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-1">Verified Variants</span>
                  <span className="text-4xl font-black text-emerald-900">{stats?.VERIFIED || 0}</span>
                </div>
                <div className="p-6 rounded-3xl bg-rose-50 border border-rose-100 flex flex-col">
                  <span className="text-[10px] font-black text-rose-600 uppercase tracking-widest mb-1">Rejected Variants</span>
                  <span className="text-4xl font-black text-rose-900">{stats?.REJECTED || 0}</span>
                </div>
              </div>

              {/* Failures List */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-black text-slate-800 uppercase tracking-widest">Recent Verification Failures</h3>
                  <button onClick={fetchData} className="text-[10px] font-black text-indigo-600 hover:underline">REFRESH</button>
                </div>
                
                {failures.length === 0 ? (
                  <div className="p-8 text-center bg-slate-50 rounded-2xl border border-slate-100">
                    <span className="text-sm font-bold text-slate-400">No recent failures detected. All systems nominal.</span>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {failures.map((f, i) => (
                      <div key={i} className="p-4 rounded-2xl border border-slate-100 bg-white shadow-sm hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start mb-2">
                          <span className="text-xs font-black text-slate-800">{f.engine_id.split('-').pop()}</span>
                          <span className="text-[10px] font-bold text-rose-500 bg-rose-50 px-2 py-0.5 rounded-md uppercase tracking-tighter">
                            {f.error_type}
                          </span>
                        </div>
                        <p className="text-[11px] font-bold text-slate-500 leading-relaxed bg-slate-50 p-2 rounded-lg border border-slate-100 italic">
                          "{f.details}"
                        </p>
                        <div className="mt-2 flex justify-between items-center">
                           <span className="text-[9px] font-black text-slate-300 tracking-widest">{new Date(f.created_at).toLocaleString()}</span>
                           <span className="text-[9px] font-bold text-indigo-400">Seed: {f.seed_key?.slice(0, 8)}...</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="p-6 bg-slate-50 border-t border-slate-100 flex justify-center">
           <p className="text-[10px] font-black text-slate-400 tracking-[0.3em] uppercase">AI MathMate Logic Pipeline v4.0.2</p>
        </div>
      </div>
    </div>
  );
};

export default SystemHealthMonitor;
