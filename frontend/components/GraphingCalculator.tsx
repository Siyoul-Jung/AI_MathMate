import React from 'react';

interface GraphingCalculatorProps {
  isActive: boolean;
  onClose: () => void;
}

export default function GraphingCalculator({ isActive, onClose }: GraphingCalculatorProps) {
  if (!isActive) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-fade-in">
      <div className="bg-white w-full max-w-5xl h-[85vh] rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-slide-up">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-slate-50">
          <div className="flex items-center gap-3">
            <span className="text-2xl">📈</span>
            <div>
              <h3 className="font-bold text-slate-800 text-lg">Graphing Calculator</h3>
              <p className="text-xs text-slate-500">Powered by Desmos</p>
            </div>
          </div>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-slate-200 rounded-full transition-colors text-slate-500 hover:text-slate-700"
            aria-label="Close calculator"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        {/* Content */}
        <div className="flex-1 bg-white relative">
           <iframe 
             src="https://www.desmos.com/calculator?embed" 
             className="w-full h-full border-0" 
             title="Desmos Graphing Calculator"
             allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
           />
        </div>
      </div>
    </div>
  );
}