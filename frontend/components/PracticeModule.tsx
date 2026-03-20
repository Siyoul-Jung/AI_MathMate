import React from 'react';

interface PracticeModuleProps {
  grade: string;
  setGrade: (grade: string) => void;
  standard: string;
  setStandard: (std: string) => void;
  type: string;
  setType: (type: string) => void;
  difficulty: string;
  setDifficulty: (diff: string) => void;
  qType: string;
  setQType: (q: string) => void;
  grades: any[];
  standards: any[];
  types: any[];
  themeClasses: any;
}

const PracticeModule: React.FC<PracticeModuleProps> = ({
  grade,
  setGrade,
  standard,
  setStandard,
  type,
  setType,
  difficulty,
  setDifficulty,
  qType,
  setQType,
  grades,
  standards,
  types,
  themeClasses
}) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {/* 1. Grade/Semester Selection */}
      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-2">Grade/Semester</label>
        <select 
          value={grade} 
          onChange={(e) => setGrade(e.target.value)}
          className={`w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 ${themeClasses.selectFocus} outline-none transition-all text-slate-700 ${themeClasses.selectHover}`}
        >
          {grades.map((g) => (
            <option key={g.id} value={g.id}>{g.name}</option>
          ))}
        </select>
      </div>

      {/* 2. Topic (Main) Selection */}
      <div>
        <label className="block text-sm font-semibold text-slate-700 mb-2">Topic (Main)</label>
        <select value={standard} onChange={(e) => setStandard(e.target.value)} className={`w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 ${themeClasses.selectFocus} outline-none transition-all text-slate-700 ${themeClasses.selectHover}`}>
          {standards.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
      </div>
      
      {/* 3. Subtopic Selection */}
      <div className="md:col-span-2">
        <label className="block text-sm font-bold text-gray-700 mb-2">Subtopic</label>
        <select 
          value={type} 
          onChange={(e) => setType(e.target.value)}
          className={`w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 ${themeClasses.selectFocus} outline-none transition-all text-slate-700 ${themeClasses.selectHover}`}
          disabled={types.length === 0}
        >
          {types.map((t) => (
            <option key={t.id} value={t.id}>{t.name}</option>
          ))}
        </select>
      </div>

      {/* 4. Difficulty */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-2">Difficulty</label>
        <select 
          value={difficulty} 
          onChange={(e) => setDifficulty(e.target.value)}
          className={`w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 ${themeClasses.selectFocus} outline-none transition-all text-slate-700 ${themeClasses.selectHover}`}
        >
          <option value="Easy">Easy</option>
          <option value="Normal">Normal</option>
          <option value="Hard">Hard</option>
        </select>
      </div>

      {/* 5. Question Type */}
      <div>
        <label className="block text-sm font-bold text-gray-700 mb-2">Question Type</label>
        <select 
          value={qType} 
          onChange={(e) => setQType(e.target.value)}
          className={`w-full px-4 py-2.5 bg-slate-50 border border-slate-300 rounded-lg focus:ring-2 ${themeClasses.selectFocus} outline-none transition-all text-slate-700 ${themeClasses.selectHover}`}
        >
          <option value="multi">Multiple Choice</option>
          <option value="short_answer">Short Answer</option>
        </select>
      </div>
    </div>
  );
};

export default PracticeModule;
