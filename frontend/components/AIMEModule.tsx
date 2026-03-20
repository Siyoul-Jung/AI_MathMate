import React from 'react';

interface AIMEModuleProps {
  loading: boolean;
  amcMode: 'MOCK' | 'DRILL';
  setAmcMode: (mode: 'MOCK' | 'DRILL') => void;
  amcBand: string;
  setAmcBand: (band: 'CHALLENGER' | 'EXPERT' | 'MASTER') => void;
  amcProblemNum: string;
  setAmcProblemNum: (num: string) => void;
  amcLevels: number[];
  drillLevel: number;
  setDrillLevel: (lvl: number) => void;
  amcMetadata: any;
  themeClasses: any;
}

const AIMEModule: React.FC<AIMEModuleProps> = ({
  loading,
  amcMode,
  setAmcMode,
  amcBand,
  setAmcBand,
  amcProblemNum,
  setAmcProblemNum,
  amcLevels,
  drillLevel,
  setDrillLevel,
  amcMetadata,
  themeClasses
}) => {
  return (
    <div className="space-y-6">
      {/* Learning Mode Selection */}
      <div className="flex bg-slate-100 p-1.5 rounded-2xl max-w-sm mx-auto shadow-inner">
        <button
          onClick={() => !loading && setAmcMode('MOCK')}
          disabled={loading}
          className={`flex-1 py-3 text-sm font-bold rounded-xl transition-all flex items-center justify-center gap-2 ${
            amcMode === 'MOCK' ? 'bg-white shadow-md text-slate-800' : 'text-slate-500 hover:text-slate-700'
          } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          🎯 Mock
        </button>
        <button
          onClick={() => !loading && setAmcMode('DRILL')}
          disabled={loading}
          className={`flex-1 py-3 text-sm font-bold rounded-xl transition-all flex items-center justify-center gap-2 ${
            amcMode === 'DRILL' ? 'bg-white shadow-md text-slate-800' : 'text-slate-500 hover:text-slate-700'
          } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          🛠️ Drill
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Phase 1: Challenger */}
        <div 
          onClick={() => !loading && setAmcBand('CHALLENGER')}
          className={`flex flex-col p-6 rounded-3xl border-2 transition-all relative ${loading ? 'cursor-not-allowed' : 'cursor-pointer active:scale-[0.98]'} ${
            amcBand === 'CHALLENGER' 
              ? 'bg-blue-50/80 border-blue-400 ring-4 ring-blue-100 shadow-xl scale-[1.05] z-10' 
              : 'bg-white border-slate-100 opacity-60 grayscale-[0.3] hover:opacity-100 hover:grayscale-0 hover:border-slate-300'
          } ${loading && amcBand !== 'CHALLENGER' ? 'opacity-30' : ''}`}
        >
          <div className="mb-4">
            <span className={`inline-block px-2 py-1 text-[9px] font-black rounded-md mb-2 ${amcBand === 'CHALLENGER' ? 'bg-blue-600 text-white' : 'bg-slate-200 text-slate-500'}`}>PHASE 1</span>
            <h3 className={`text-xl font-black ${amcBand === 'CHALLENGER' ? 'text-blue-900' : 'text-slate-700'}`}>Challenger</h3>
            <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-wider font-bold">P01 ~ P05</p>
          </div>

          {amcMode === 'DRILL' && (
            <div className="grid grid-cols-5 gap-1.5 mt-auto">
              {Array.from({ length: 5 }, (_, i) => {
                const pid = `P${(i + 1).toString().padStart(2, '0')}`;
                const isImplemented = ['P01'].includes(pid);
                return (
                  <button
                    key={pid}
                    onClick={(e) => { e.stopPropagation(); !loading && isImplemented && setAmcProblemNum(pid); }}
                    disabled={loading || !isImplemented}
                    className={`py-2 rounded-xl text-xs font-bold border-2 transition-all ${
                      amcProblemNum === pid 
                        ? 'bg-blue-600 text-white border-blue-600 shadow-sm' 
                        : !isImplemented ? 'bg-slate-50 text-slate-200 border-transparent' : 'bg-white text-slate-400 border-slate-100 hover:border-blue-200'
                    } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    {i + 1}
                  </button>
                );
              })}
            </div>
          )}
          
          {amcMode === 'MOCK' && amcBand === 'CHALLENGER' && (
            <div className="mt-auto flex justify-center">
              <span className="text-blue-500 animate-bounce">👇</span>
            </div>
          )}
        </div>

        {/* Phase 2: Expert */}
        <div 
          onClick={() => !loading && setAmcBand('EXPERT')}
          className={`flex flex-col p-6 rounded-3xl border-2 transition-all relative ${loading ? 'cursor-not-allowed' : 'cursor-pointer active:scale-[0.98]'} ${
            amcBand === 'EXPERT' 
              ? 'bg-indigo-50/80 border-indigo-400 ring-4 ring-indigo-100 shadow-xl scale-[1.05] z-10' 
              : 'bg-white border-slate-100 opacity-60 grayscale-[0.3] hover:opacity-100 hover:grayscale-0 hover:border-slate-300'
          } ${loading && amcBand !== 'EXPERT' ? 'opacity-30' : ''}`}
        >
          <div className="mb-4">
            <span className={`inline-block px-2 py-1 text-[9px] font-black rounded-md mb-2 ${amcBand === 'EXPERT' ? 'bg-indigo-600 text-white' : 'bg-slate-200 text-slate-500'}`}>PHASE 2</span>
            <h3 className={`text-xl font-black ${amcBand === 'EXPERT' ? 'text-indigo-900' : 'text-slate-700'}`}>Expert</h3>
            <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-wider font-bold">P06 ~ P10</p>
          </div>

          {amcMode === 'DRILL' && (
            <div className="grid grid-cols-5 gap-1.5 mt-auto">
              {Array.from({ length: 5 }, (_, i) => {
                const num = i + 6;
                const pid = `P${num.toString().padStart(2, '0')}`;
                const isImplemented = ['P10'].includes(pid);
                return (
                  <button
                    key={pid}
                    onClick={(e) => { e.stopPropagation(); !loading && isImplemented && setAmcProblemNum(pid); }}
                    disabled={loading || !isImplemented}
                    className={`py-2 rounded-xl text-xs font-bold border-2 transition-all ${
                      amcProblemNum === pid 
                        ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' 
                        : !isImplemented ? 'bg-slate-50 text-slate-200 border-transparent' : 'bg-white text-slate-400 border-slate-100 hover:border-indigo-200'
                    } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    {num}
                  </button>
                );
              })}
            </div>
          )}

          {amcMode === 'MOCK' && amcBand === 'EXPERT' && (
            <div className="mt-auto flex justify-center">
              <span className="text-indigo-500 animate-bounce">👇</span>
            </div>
          )}
        </div>

        {/* Phase 3: Master */}
        <div 
          onClick={() => !loading && setAmcBand('MASTER')}
          className={`flex flex-col p-6 rounded-3xl border-2 transition-all relative ${loading ? 'cursor-not-allowed' : 'cursor-pointer active:scale-[0.98]'} ${
            amcBand === 'MASTER' 
              ? 'bg-rose-50/80 border-rose-400 ring-4 ring-rose-100 shadow-xl scale-[1.05] z-10' 
              : 'bg-white border-slate-100 opacity-60 grayscale-[0.3] hover:opacity-100 hover:grayscale-0 hover:border-slate-300'
          } ${loading && amcBand !== 'MASTER' ? 'opacity-30' : ''}`}
        >
          <div className="mb-4">
            <span className={`inline-block px-2 py-1 text-[9px] font-black rounded-md mb-2 ${amcBand === 'MASTER' ? 'bg-rose-600 text-white' : 'bg-slate-200 text-slate-500'}`}>PHASE 3</span>
            <h3 className={`text-xl font-black ${amcBand === 'MASTER' ? 'text-rose-900' : 'text-slate-700'}`}>Master</h3>
            <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-wider font-bold">P11 ~ P15</p>
          </div>

          {amcMode === 'DRILL' && (
            <div className="grid grid-cols-5 gap-1.5 mt-auto">
              {Array.from({ length: 5 }, (_, i) => {
                const num = i + 11;
                const pid = `P${num.toString().padStart(2, '0')}`;
                const isImplemented = ['P11', 'P12', 'P13', 'P14', 'P15'].includes(pid);
                return (
                  <button
                    key={pid}
                    onClick={(e) => { e.stopPropagation(); !loading && isImplemented && setAmcProblemNum(pid); }}
                    disabled={loading || !isImplemented}
                    className={`py-2 rounded-xl text-xs font-bold border-2 transition-all ${
                      amcProblemNum === pid 
                        ? 'bg-rose-600 text-white border-rose-600 shadow-sm' 
                        : !isImplemented ? 'bg-slate-50 text-slate-200 border-transparent' : 'bg-white text-slate-400 border-slate-100 hover:border-rose-200'
                    } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    {num}
                  </button>
                );
              })}
            </div>
          )}

          {amcMode === 'MOCK' && amcBand === 'MASTER' && (
            <div className="mt-auto flex justify-center">
              <span className="text-rose-500 animate-bounce">👇</span>
            </div>
          )}
        </div>
      </div>

      {/* Bottom Detailed Settings (Visible only in DRILL mode) */}
      {amcMode === 'DRILL' && amcProblemNum && (
        <div className="bg-slate-50 p-6 rounded-3xl border border-slate-200 animate-in fade-in slide-in-from-top-4 duration-500">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <span className={`${themeClasses.bg} ${themeClasses.text} px-3 py-1 rounded-full text-xs font-black`}>{amcProblemNum}</span>
              <span className="text-sm font-bold text-slate-700 uppercase tracking-tighter">Target Drill Level</span>
              {amcMetadata && (
                <div className="flex gap-1 ml-2">
                  <span className="px-2 py-0.5 bg-indigo-100 text-indigo-700 text-[10px] font-bold rounded shadow-sm border border-indigo-200">
                    🧬 {amcMetadata.domain}
                  </span>
                  {amcMetadata.dna_tags?.slice(0, 2).map((tag: string, i: number) => (
                    <span key={i} className="px-2 py-0.5 bg-slate-100 text-slate-500 text-[10px] font-medium rounded border border-slate-200 hidden md:inline">
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
            <div className="flex gap-2 w-full md:w-auto">
              {amcLevels.map((lvl) => (
                <button
                  key={lvl}
                  onClick={() => !loading && setDrillLevel(lvl)}
                  disabled={loading}
                  className={`flex-1 md:flex-none px-6 py-2.5 rounded-xl font-bold text-sm transition-all border-2 ${
                    drillLevel === lvl 
                      ? `${themeClasses.active} border-current shadow-sm` 
                      : 'bg-white text-slate-400 border-slate-100 hover:border-slate-200'
                  } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  LV {lvl}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIMEModule;
