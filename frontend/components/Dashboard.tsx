import React, { useState } from 'react';
import { ALL_STANDARDS, GRADES_MAP } from '../data/constants';

interface DashboardProps {
  analysis: any;
  advice: string;
  onWeakPointClick: (stdId: string) => void;
  themeColor: 'indigo' | 'purple' | 'emerald';
  category: string;
}

export default function Dashboard({ analysis, advice, onWeakPointClick, themeColor, category }: DashboardProps) {
  if (!analysis) return null;

  const [showAllProficiency, setShowDashboardProficiency] = useState(false);
  const colors = {
    indigo: {
      border: 'border-indigo-100',
      bg: 'bg-indigo-50',
      text: 'text-indigo-800',
    },
    purple: {
      border: 'border-purple-100',
      bg: 'bg-purple-50',
      text: 'text-purple-800',
    },
    emerald: {
      border: 'border-emerald-100',
      bg: 'bg-emerald-50',
      text: 'text-emerald-800',
    }
  }[themeColor];

  // 1. Extract grade ID list for current category
  const targetGrades = GRADES_MAP[category]?.map(g => g.id) || [];
  
  // 2. Create set of standard IDs belonging to those grades (Filtering criteria)
  const targetStandardsSet = new Set(
    ALL_STANDARDS.filter(s => targetGrades.includes(s.grade)).map(s => s.id)
  );

  // 3. Filter data (only those belonging to current category)
  const filteredWeakPoints = analysis.weak_points.filter((wp: string) => targetStandardsSet.has(wp));
  const proficiencyEntries = Object.entries(analysis.proficiency).filter(([stdId]) => targetStandardsSet.has(stdId));
  
  const displayedProficiency = showAllProficiency ? proficiencyEntries : proficiencyEntries.slice(0, 5);

  // Prepare chart data
  const trendData = analysis.recent_trend || [];
  const maxSolved = Math.max(...trendData.map((d: any) => d.solved), 10); // Reference for max height of bar chart

  return (
    <div className={`bg-white p-6 rounded-lg shadow-md mb-8 border ${colors.border} animate-fade-in`}>
      <h2 className="text-xl font-bold mb-4 text-slate-800">Learning Proficiency Analysis</h2>
      
      {/* AI Advice Section */}
      <div className={`mb-6 ${colors.bg} p-4 rounded-lg border ${colors.border}`}>
        <h3 className={`text-sm font-semibold ${colors.text} mb-2 flex items-center gap-2`}>
          🤖 A Word from AI Tutor
        </h3>
        <p className="text-slate-700 text-sm leading-relaxed whitespace-pre-wrap">{advice || 'Analyzing learning data...'}</p>
      </div>

      <div className="mb-6">
        <h3 className="text-sm font-semibold text-slate-500 mb-2 uppercase tracking-wider">Weak Points (Focus Area)</h3>
        {filteredWeakPoints.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {filteredWeakPoints.map((wp: string) => (
              <button
                key={wp}
                onClick={() => onWeakPointClick(wp)}
                className="px-3 py-1 bg-red-50 text-red-700 rounded-full text-sm font-medium border border-red-200 hover:bg-red-100 transition"
              >
                {ALL_STANDARDS.find(s => s.id === wp)?.name || 'Unknown Standard'} 🚨
              </button>
            ))}
          </div>
        ) : (
          <p className="text-slate-500 text-sm">No weak points found in this course. Great job! 🎉</p>
        )}
      </div>

      {/* Recent Learning Trend Chart */}
      {trendData.length > 0 && (
        <div className="mb-8">
          <h3 className="text-sm font-semibold text-slate-500 mb-4 uppercase tracking-wider">📈 Last 7 Days Learning Trend</h3>
          <div className="bg-white rounded-xl border border-slate-100 p-4">
            <div className="flex items-center justify-between mb-2 text-xs text-slate-400">
              <div className="flex items-center gap-1"><span className="w-2 h-2 bg-slate-200 rounded-sm"></span>Problems Solved</div>
              <div className="flex items-center gap-1"><span className={`w-2 h-2 rounded-full ${colors.bg} border ${colors.border}`}></span>Accuracy (%)</div>
            </div>
            
            <div className="relative h-40 w-full">
              {/* SVG Chart */}
              <svg className="w-full h-full overflow-visible" viewBox={`0 0 ${trendData.length * 50} 100`} preserveAspectRatio="none">
                {/* 1. Bar Chart (Number of Problems Solved) */}
                {trendData.map((d: any, i: number) => {
                  const barHeight = (d.solved / maxSolved) * 80; // Max 80% height
                  return (
                    <g key={`bar-${i}`}>
                      <rect
                        x={i * 50 + 10}
                        y={100 - barHeight}
                        width={30}
                        height={barHeight}
                        className="fill-slate-100 hover:fill-slate-200 transition-colors"
                        rx="4"
                      />
                      {/* Solved Count Label */}
                      <text x={i * 50 + 25} y={100 - barHeight - 5} textAnchor="middle" className="text-[10px] fill-slate-400 font-mono">{d.solved}</text>
                    </g>
                  );
                })}

                {/* 2. Line Chart (Accuracy Rate) */}
                <path
                  d={`M ${trendData.map((d: any, i: number) => `${i * 50 + 25},${100 - d.correct_rate}`).join(' L ')}`}
                  fill="none"
                  stroke={themeColor === 'indigo' ? '#6366f1' : themeColor === 'purple' ? '#a855f7' : '#10b981'}
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
                
                {/* 3. Data Points */}
                {trendData.map((d: any, i: number) => (
                  <circle
                    key={`point-${i}`}
                    cx={i * 50 + 25}
                    cy={100 - d.correct_rate}
                    r="3"
                    className={`${themeColor === 'indigo' ? 'fill-indigo-600' : themeColor === 'purple' ? 'fill-purple-600' : 'fill-emerald-600'} stroke-white stroke-2`}
                  />
                ))}
              </svg>

              {/* X-axis Labels (Date) */}
              <div className="flex justify-between mt-2 px-2">
                {trendData.map((d: any, i: number) => (
                  <span key={i} className="text-[10px] text-slate-400 font-mono w-8 text-center">{d.date}</span>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      <div>
        <h3 className="text-sm font-semibold text-slate-500 mb-2 uppercase tracking-wider">Proficiency by Standard</h3>
        <div className="space-y-2 pr-2">
          {displayedProficiency.map(([stdId, score]: [string, any]) => (
            <div key={stdId} className="flex items-center justify-between text-sm">
              <span className="text-slate-700 truncate w-1/2" title={ALL_STANDARDS.find(s => s.id === stdId)?.name}>{ALL_STANDARDS.find(s => s.id === stdId)?.name || 'Unknown Standard'}</span>
              <div className="w-1/2 flex items-center gap-2">
                <div className="flex-1 h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div 
                    className={`h-full rounded-full ${score >= 80 ? 'bg-green-500' : score >= 60 ? 'bg-yellow-500' : 'bg-red-500'}`} 
                    style={{ width: `${score}%` }}
                  ></div>
                </div>
                <span className="w-8 text-right font-mono text-xs">{score}%</span>
              </div>
            </div>
          ))}
        </div>
        {proficiencyEntries.length > 5 && (
          <button 
            onClick={() => setShowDashboardProficiency(!showAllProficiency)}
            className={`mt-3 text-xs font-medium ${colors.text} hover:underline w-full text-center py-1`}
          >
            {showAllProficiency ? 'Collapse ▲' : `View All (${proficiencyEntries.length}) ▼`}
          </button>
        )}
      </div>
    </div>
  );
}