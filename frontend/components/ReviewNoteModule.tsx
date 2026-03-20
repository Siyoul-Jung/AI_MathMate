import React from 'react';
import { ALL_STANDARDS } from '../data/constants';

interface ReviewNoteModuleProps {
  wrongAnswers: any[];
  expandedStandards: Set<string>;
  toggleStandard: (stdId: string) => void;
  renderContent: (text: string) => React.ReactNode;
  handleRetryProblem: (wp: any) => void;
  themeClasses: any;
}

const ReviewNoteModule: React.FC<ReviewNoteModuleProps> = ({
  wrongAnswers,
  expandedStandards,
  toggleStandard,
  renderContent,
  handleRetryProblem,
  themeClasses
}) => {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 mb-8 animate-fade-in">
      <h2 className={`text-xl font-bold mb-4 ${themeClasses.text}`}>📝 Review Note ({wrongAnswers.length})</h2>
      {wrongAnswers.length === 0 ? (
        <div className="text-center py-8 text-slate-500">
          <p className="text-lg mb-2">No wrong problems.</p>
          <p className="text-sm">Perfect! 🎉</p>
        </div>
      ) : (
        <div className="space-y-6">
          {Object.entries(
            wrongAnswers.reduce((acc, curr) => {
              const stdId = curr.standard_id || 'unknown';
              if (!acc[stdId]) acc[stdId] = [];
              acc[stdId].push(curr);
              return acc;
            }, {} as {[key: string]: any[]})
          ).map(([stdId, problems]) => (
            <div key={stdId}>
              <button 
                onClick={() => toggleStandard(stdId)}
                className="w-full flex items-center justify-between text-md font-bold text-slate-600 mb-2 p-3 rounded-lg hover:bg-slate-50 transition-colors border border-transparent hover:border-slate-100"
              >
                <div className="flex items-center">
                  <span className={`w-1.5 h-4 mr-2 rounded-full ${themeClasses.bg.replace('-50', '-500')}`}></span>
                  {ALL_STANDARDS.find(s => s.id === stdId)?.name || 'Other Topics'}
                  <span className="ml-2 text-xs text-slate-500 bg-slate-100 px-2 py-0.5 rounded-full">{(problems as any[]).length} Problems</span>
                </div>
                <span className={`transform transition-transform duration-200 text-slate-400 ${expandedStandards.has(stdId) ? 'rotate-180' : ''}`}>▼</span>
              </button>
              
              {expandedStandards.has(stdId) && (
                <div className="space-y-3 pl-2 animate-fade-in">
                  {(problems as any[]).map((wp, idx) => (
                    <div key={idx} className="border border-slate-100 rounded-xl p-4 hover:bg-slate-50 transition-all flex justify-between items-center group bg-white">
                      <div className="flex-1 pr-4">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-xs font-mono text-slate-400 bg-slate-100 px-2 py-0.5 rounded">
                            {new Date(wp.savedAt).toLocaleDateString()}
                          </span>
                          <span className="text-xs font-bold text-red-500 bg-red-50 px-2 py-0.5 rounded">Incorrect</span>
                        </div>
                        <div className="text-slate-800 font-medium line-clamp-2 text-sm">{renderContent(wp.question)}</div>
                      </div>
                      <button 
                         onClick={() => handleRetryProblem(wp)}
                        className={`px-4 py-2 text-sm font-bold rounded-lg ${themeClasses.button} text-white opacity-0 group-hover:opacity-100 transition-opacity shadow-sm`}
                      >
                        Retry
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ReviewNoteModule;
