import React, { useState } from 'react';

interface AIMEModuleProps {
  loading: boolean;
  amcMode: 'MOCK' | 'DRILL';
  setAmcMode: (mode: 'MOCK' | 'DRILL') => void;
  amcBand: string;
  setAmcBand: (band: 'CHALLENGER' | 'EXPERT' | 'MASTER') => void;
  amcProblemNum: string;
  setAmcProblemNum: (num: string) => void;
  amcYear: string;
  setAmcYear: (year: string) => void;
  amcExam: string;
  setAmcExam: (exam: string) => void;
  amcLevels: number[];
  drillLevel: number;
  setDrillLevel: (lvl: number) => void;
  amcMetadata: any;
  amcArchives: any; // { "Algebra": [meta...], "Geometry": [...] }
  themeClasses: any;
  onGenerate?: () => void;
}

const DOMAIN_ICONS: { [key: string]: string } = {
  'Algebra': '∑',
  'Geometry': '△',
  'Number Theory': 'N',
  'Combinatorics': 'C',
  'Special Topics': '✦'
};

const AIMEModule: React.FC<AIMEModuleProps> = ({
  loading,
  amcMode,
  setAmcMode,
  amcBand,
  setAmcBand,
  amcProblemNum,
  setAmcProblemNum,
  amcYear,
  setAmcYear,
  amcExam,
  setAmcExam,
  amcLevels,
  drillLevel,
  setDrillLevel,
  amcMetadata,
  amcArchives,
  themeClasses,
  onGenerate
}) => {
  const [selectedDomain, setSelectedDomain] = useState<string | null>(null);

  const PHASES = [
    { id: 'CHALLENGER', name: 'Challenger', phase: 1, range: 'P01 ~ P05', color: 'blue', problems: ['P01', 'P02', 'P03', 'P04', 'P05'] },
    { id: 'EXPERT', name: 'Expert', phase: 2, range: 'P06 ~ P10', color: 'indigo', problems: ['P06', 'P07', 'P08', 'P09', 'P10'] },
    { id: 'MASTER', name: 'Master', phase: 3, range: 'P11 ~ P15', color: 'rose', problems: ['P11', 'P12', 'P13', 'P14', 'P15'] }
  ];

  const handleMissionClick = (pid: string, year: string, exam: string) => {
    setAmcProblemNum(pid);
    setAmcYear(year);
    setAmcExam(exam);
    setDrillLevel(1);
  };

  const currentArchive = React.useMemo(() => {
    if (!selectedDomain) return [];
    if (selectedDomain === 'Special Topics') {
      const mainKeys = ['Algebra', 'Geometry', 'Number Theory', 'Combinatorics'];
      const otherKeys = Object.keys(amcArchives).filter(k => !mainKeys.includes(k));
      return otherKeys.flatMap(k => amcArchives[k] || []);
    }
    return amcArchives[selectedDomain] || [];
  }, [selectedDomain, amcArchives]);

  return (
    <div className="space-y-6">
      {/* State-of-the-Art Mode Toggle (Final Mock vs Practice Hub) */}
      <div className="flex p-1.5 bg-slate-100/50 backdrop-blur-sm rounded-2xl w-fit mx-auto shadow-inner border border-slate-200/50">
        <button
          onClick={() => !loading && setAmcMode('MOCK')}
          className={`flex items-center gap-2 px-6 py-2.5 text-sm font-black rounded-xl transition-all duration-300 ${
            amcMode === 'MOCK' 
              ? 'bg-white text-indigo-600 shadow-md ring-1 ring-black/5' 
              : 'text-slate-400 hover:text-slate-600'
          }`}
        >
          <span className="text-lg">🎯</span>
          Final Mock
        </button>
        <button
          onClick={() => {
            if (!loading) {
              setAmcMode('DRILL');
              setAmcProblemNum(''); // Clear selection on enter archive
            }
          }}
          className={`flex items-center gap-2 px-6 py-2.5 text-sm font-black rounded-xl transition-all duration-300 ${
            amcMode === 'DRILL' 
              ? 'bg-white text-emerald-600 shadow-md ring-1 ring-black/5' 
              : 'text-slate-400 hover:text-slate-600'
          }`}
        >
          <span className="text-lg">🧬</span>
          Practice Hub
        </button>
      </div>

      {/* --- MOCK MODE: PHASE SELECTION --- */}
      {amcMode === 'MOCK' && (
        <div className="space-y-8 animate-in fade-in zoom-in-95 duration-700">
          {/* Mock Mode Header */}
          <div className="relative p-8 rounded-3xl bg-indigo-950 overflow-hidden shadow-2xl border border-indigo-500/30 group">
             {/* Animated background pulse */}
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-500/10 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/2 group-hover:bg-rose-500/10 transition-colors duration-1000"></div>
            
            <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-indigo-400"></div>
                  <span className="text-[10px] font-black text-indigo-300 uppercase tracking-[0.2em]">Full Phase Practice</span>
                </div>
                <h2 className="text-3xl font-black text-white tracking-tight">Final Mock</h2>
                <p className="max-w-md text-sm font-bold text-indigo-200/60 leading-relaxed">
                  Challenge yourself with representative problems from each phase. 
                  Experience the real-world AIME difficulty in a focused environment.
                </p>
              </div>
              
              <div className="flex items-center gap-4 px-6 py-3 bg-white/5 backdrop-blur-md rounded-2xl border border-white/10">
                <div className="flex flex-col">
                  <span className="text-[10px] font-black text-indigo-400 uppercase tracking-widest leading-none mb-1">Mode</span>
                  <span className="text-xs font-black text-white">REPRESENTATIVE</span>
                </div>
                <div className="w-px h-6 bg-white/10"></div>
                <div className="flex flex-col">
                  <span className="text-[10px] font-black text-indigo-400 uppercase tracking-widest leading-none mb-1">Focus</span>
                  <span className="text-xs font-black text-white">PHASE MASTERY</span>
                </div>
              </div>
            </div>
          </div>

          {/* Phase Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {PHASES.map((phase) => (
              <div 
                key={phase.id}
                onClick={() => !loading && setAmcBand(phase.id as any)}
                className={`group flex flex-col p-8 rounded-[2rem] border-2 transition-all relative overflow-hidden h-[240px] justify-between ${
                  loading ? 'cursor-not-allowed' : 'cursor-pointer active:scale-95'
                } ${
                  amcBand === phase.id 
                    ? 'bg-white border-indigo-600 shadow-2xl shadow-indigo-100 ring-4 ring-indigo-50' 
                    : 'bg-white border-slate-100 opacity-60 hover:opacity-100 hover:border-slate-300 hover:shadow-xl'
                }`}
              >
                {/* Visual Accent */}
                <div className={`absolute -right-4 -top-4 w-24 h-24 rounded-full opacity-5 transition-transform group-hover:scale-150 ${
                  amcBand === phase.id ? 'bg-indigo-600' : 'bg-slate-300'
                }`}></div>

                <div className="relative z-10">
                  <div className="flex justify-between items-center mb-4">
                    <span className={`px-2.5 py-1 text-[10px] font-black rounded-lg ${
                      amcBand === phase.id ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-400'
                    }`}>PHASE {phase.phase}</span>
                    <span className="text-sm">
                      {phase.phase === 1 ? '🥇' : phase.phase === 2 ? '💎' : '👑'}
                    </span>
                  </div>
                  <h3 className={`text-2xl font-black mb-1 ${amcBand === phase.id ? 'text-indigo-950' : 'text-slate-700'}`}>
                    {phase.name}
                  </h3>
                  <p className="text-xs text-slate-400 font-bold tracking-widest uppercase italic">{phase.range}</p>
                </div>

                <div className="mt-8 flex flex-col gap-3 relative z-10">
                   <div className="w-full h-1 bg-slate-100 rounded-full overflow-hidden">
                      <div className={`h-full transition-all duration-1000 ${
                        amcBand === phase.id ? 'w-full bg-indigo-500' : 'w-0 bg-slate-300'
                      }`}></div>
                   </div>
                   <div className="flex justify-between items-center">
                     <span className={`text-[10px] font-black tracking-widest uppercase ${
                       amcBand === phase.id ? 'text-indigo-600' : 'text-slate-300'
                     }`}>
                       {amcBand === phase.id ? 'Challenge Selected' : 'Select Phase'}
                     </span>
                     {amcBand === phase.id && (
                        <div className="flex gap-1">
                          <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse"></div>
                          <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse delay-75"></div>
                          <div className="w-1.5 h-1.5 rounded-full bg-indigo-500 animate-pulse delay-150"></div>
                        </div>
                     )}
                   </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* --- DRILL MODE: BENTO-STYLE PRACTICE HUB --- */}
      {amcMode === 'DRILL' && (
        <div className="space-y-8 animate-in fade-in zoom-in-95 duration-700">
          {/* Practice Hero (Always Visible in Drill Mode) */}
          <div className="relative p-8 rounded-3xl bg-emerald-950 overflow-hidden shadow-2xl border border-emerald-500/30 group">
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-emerald-500/10 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/2 group-hover:bg-indigo-500/10 transition-colors duration-1000"></div>
            
            <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-emerald-400"></div>
                  <span className="text-[10px] font-black text-emerald-300 uppercase tracking-[0.2em]">
                    {selectedDomain ? `${selectedDomain} Practice` : 'Learning Environment'}
                  </span>
                </div>
                <h2 className="text-3xl font-black text-white tracking-tight">
                  {selectedDomain ? `${selectedDomain}` : 'Practice Hub'}
                </h2>
                <p className="max-w-md text-sm font-bold text-emerald-200/60 leading-relaxed">
                  {selectedDomain 
                    ? `Mastering ${selectedDomain} through targeted mission drills. Explore the curated archive below.`
                    : 'Master the foundational concepts of the AIME through targeted mission drills. Select a domain to begin.'
                  }
                </p>
              </div>
              
              <div className="flex items-center gap-6 px-6 py-4 bg-white/5 backdrop-blur-md rounded-2xl border border-white/10">
                <div className="flex flex-col items-center">
                  <span className="text-[10px] font-black text-emerald-400 uppercase tracking-widest mb-1">
                    {selectedDomain ? 'Domain' : 'Missions'}
                  </span>
                  <span className="text-xs font-black text-white">
                    {selectedDomain 
                      ? `${amcArchives[selectedDomain]?.length || 0} Units`
                      : `${Object.values(amcArchives).reduce((sum: number, arr: any) => sum + (arr?.length || 0), 0)} Available`
                    }
                  </span>
                </div>
                <div className="w-px h-8 bg-white/10"></div>
                <div className="flex flex-col items-center">
                  <span className="text-[10px] font-black text-emerald-400 uppercase tracking-widest mb-1">Depth</span>
                  <span className="text-xs font-black text-white">
                    {amcBand === 'CHALLENGER' ? 'LV 1-2' : 'LV 1-3'} Suites
                  </span>
                </div>
              </div>
            </div>
          </div>

          {!selectedDomain ? (
            /* Bento Grid of Domain Archives */
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {Object.keys(DOMAIN_ICONS).map((domain) => {
                let count = amcArchives[domain]?.length || 0;
                
                if (domain === 'Special Topics') {
                  const mainKeys = ['Algebra', 'Geometry', 'Number Theory', 'Combinatorics'];
                  const otherKeys = Object.keys(amcArchives).filter(k => !mainKeys.includes(k));
                  count = otherKeys.reduce((sum, k) => sum + (amcArchives[k]?.length || 0), 0);
                }

                if (count === 0) return null;
                return (
                  <button
                    key={domain}
                    onClick={() => setSelectedDomain(domain)}
                    className="group relative h-48 flex flex-col items-center justify-center p-6 rounded-[2rem] bg-white border border-slate-100 shadow-sm hover:shadow-2xl hover:border-emerald-500 hover:-translate-y-1 transition-all text-center overflow-hidden"
                  >
                    {/* Soft background icon */}
                    <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-8xl opacity-[0.03] pointer-events-none group-hover:scale-125 transition-transform duration-700">
                      {DOMAIN_ICONS[domain]}
                    </div>
                    
                    <div className="relative z-10">
                      <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform duration-500 filter drop-shadow-sm">
                        {DOMAIN_ICONS[domain]}
                      </div>
                      <span className="block text-sm font-black text-slate-800 tracking-tight mb-1">{domain}</span>
                      <div className="inline-block px-2 py-0.5 bg-emerald-50 text-emerald-600 text-[9px] font-black rounded-full border border-emerald-100 opacity-0 group-hover:opacity-100 transition-opacity">
                        {count} MISSIONS
                      </div>
                    </div>
                    
                    <div className="absolute inset-x-0 bottom-0 h-1.5 bg-gradient-to-r from-emerald-500 to-teal-400 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-500"></div>
                  </button>
                );
              })}
            </div>
          ) : (
            /* Selected Domain: Mission List */
            <div className="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden flex flex-col animate-in slide-in-from-bottom-5 duration-500">
              <div className="p-4 bg-slate-50/80 backdrop-blur-md border-b border-slate-100 flex items-center justify-between">
                <button 
                  onClick={() => {
                    setSelectedDomain(null);
                    setAmcProblemNum('');
                  }}
                  className="flex items-center gap-2 text-xs font-black text-slate-400 hover:text-emerald-600 transition-colors"
                >
                  <span className="text-lg">←</span> Back to Practice Hub
                </button>
                <div className="flex items-center gap-2">
                  <span className="text-xl">{DOMAIN_ICONS[selectedDomain]}</span>
                  <span className="text-sm font-black text-slate-800">{selectedDomain} Missions</span>
                </div>
              </div>
              
              <div className="max-h-[350px] overflow-y-auto p-4 custom-scrollbar">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {currentArchive.map((meta: any, idx: number) => {
                    const isSelected = amcProblemNum === meta.p_id;
                    return (
                      <button
                        key={idx}
                        onClick={() => handleMissionClick(meta.p_id, meta.year, meta.exam)}
                        className={`group p-4 rounded-2xl border-2 transition-all flex flex-col text-left relative ${
                          isSelected 
                            ? 'bg-emerald-50 border-emerald-500 shadow-lg shadow-emerald-50' 
                            : 'bg-white border-slate-50 hover:border-slate-200'
                        }`}
                      >
                        <div className="flex justify-between items-start mb-1">
                          <span className={`px-2 py-0.5 rounded-lg text-[10px] font-black ${
                            isSelected ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-400 opacity-0'
                          }`}>
                            ACTIVE
                          </span>
                        </div>
                        <span className={`text-[13px] font-black leading-snug ${isSelected ? 'text-emerald-900' : 'text-slate-700'}`}>
                          {meta.title}
                        </span>
                        <div className="flex flex-wrap gap-1 mt-3">
                          {meta.dna_tags?.slice(0, 3).map((tag: string, i: number) => (
                            <span key={i} className="text-[9px] font-bold text-slate-400">#{tag}</span>
                          ))}
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* --- PREMIUM DRILL CONFIG PANEL (Visible only when mission selected in Archive) --- */}
      {amcMode === 'DRILL' && amcProblemNum && selectedDomain && (
        <div className="bg-gradient-to-br from-slate-50 to-white p-6 rounded-3xl border border-slate-200 shadow-lg animate-in fade-in slide-in-from-top-4 duration-500">
          <div className="flex flex-col gap-6">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
              <div className="flex flex-col gap-2">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-2xl bg-emerald-600 text-white flex items-center justify-center text-xl font-black shadow-lg shadow-emerald-200">
                    {DOMAIN_ICONS[selectedDomain]}
                  </div>
                  <div>
                    <h4 className="text-sm font-black text-slate-800 leading-tight">Focus Concept</h4>
                    <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Strengthening Proficiency</span>
                  </div>
                </div>
                {amcMetadata && (
                   <div className="flex flex-wrap gap-2 mt-2">
                   <div className="px-3 py-1 bg-white text-emerald-600 text-[10px] font-black rounded-xl border border-emerald-100 shadow-sm flex items-center gap-1.5">
                     <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
                     {amcMetadata.title}
                   </div>
                   {amcMetadata.dna_tags?.map((tag: string, i: number) => (
                     <div key={i} className="px-3 py-1 bg-slate-100/50 text-slate-400 text-[10px] font-bold rounded-xl border border-slate-100">
                       #{tag}
                     </div>
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
                    className={`flex-1 md:flex-none h-14 w-20 rounded-2xl font-black text-xs transition-all border-2 relative overflow-hidden ${
                      drillLevel === lvl 
                        ? 'bg-emerald-600 border-emerald-600 text-white shadow-xl shadow-emerald-100' 
                        : 'bg-white text-slate-400 border-slate-100 hover:border-slate-200'
                    } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
                  >
                    {drillLevel === lvl && (
                       <div className="absolute top-0 right-0 w-4 h-4 bg-white opacity-20 transform rotate-45 translate-x-1.5 -translate-y-1.5 font-bold">✓</div>
                    )}
                    <div className="flex flex-col items-center">
                      <span className="opacity-60 font-bold mb-0.5 text-[8px]">
                        {lvl === 1 ? 'CONCEPT' : lvl === 2 ? 'APPLY' : 'MASTER'}
                      </span>
                      <span className="text-lg leading-none">{lvl}</span>
                    </div>
                  </button>
                ))}
              </div>
            </div>

            {/* Dynamic Level Description */}
            <div className="mt-4 p-4 bg-emerald-50/30 rounded-2xl border border-emerald-100/50 animate-in fade-in slide-in-from-left-2 duration-700">
              <div className="flex gap-3">
                <div className="text-lg">💡</div>
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] font-black text-emerald-700 uppercase tracking-widest">Training Goal</span>
                  <p className="text-xs font-bold text-slate-600 leading-relaxed italic">
                    {amcMetadata?.drill_config?.[`L${drillLevel}`] || "Strengthening core proficiency and problem-solving depth in this concept."}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIMEModule;
