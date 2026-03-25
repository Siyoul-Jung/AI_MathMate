import React, { useState } from 'react';
import { InlineMath, BlockMath } from 'react-katex';
import 'katex/dist/katex.min.css';

interface ProblemViewerProps {
  problem: any;
  selectedAnswer: any;
  isCorrect: boolean | null;
  showExplanation: boolean;
  hintIndex: number;
  onAnswerClick: (ans: any) => void;
  setHintIndex: (idx: number) => void;
  setShowExplanation: (show: boolean) => void;
  themeColor: string;
  onDrillClick?: (level: number) => void;
  band?: string;
  metadata?: any;
}

export default function ProblemViewer({
  problem,
  selectedAnswer,
  isCorrect,
  showExplanation,
  hintIndex,
  onAnswerClick,
  setHintIndex,
  setShowExplanation,
  themeColor,
  onDrillClick,
  band,
  metadata
}: ProblemViewerProps) {
  if (!problem) {
    return (
      <div className="flex flex-col items-center justify-center p-12 border-2 border-dashed border-slate-200 rounded-3xl bg-slate-50 text-slate-400">
        <div className="text-4xl mb-4">🧬</div>
        <p className="font-medium">No problem selected or generated yet.</p>
        <p className="text-xs mt-2">Try clicking "Shuffle Variant" or select a challenge phase.</p>
      </div>
    );
  }
  const themeClasses = {
    indigo: { button: 'bg-indigo-600 hover:bg-indigo-700', text: 'text-indigo-700', bg: 'bg-indigo-50', border: 'border-indigo-200' },
    purple: { button: 'bg-purple-600 hover:bg-purple-700', text: 'text-purple-700', bg: 'bg-purple-50', border: 'border-purple-200' },
    emerald: { button: 'bg-emerald-600 hover:bg-emerald-700', text: 'text-emerald-700', bg: 'bg-emerald-50', border: 'border-emerald-200' },
  }[themeColor] || { button: 'bg-indigo-600', text: 'text-indigo-700', bg: 'bg-indigo-50', border: 'border-indigo-200' };

  // Text Parsing Helper (Bold, Newline)
  const parseText = (text: string) => {
    return text.split(/(\*\*.*?\*\*|\n)/g).map((part, i) => {
      if (part.startsWith('**') && part.endsWith('**')) {
        return <strong key={i}>{part.slice(2, -2)}</strong>;
      }
      if (part === '\n') return <br key={i} />;
      return <span key={i}>{part}</span>;
    });
  };

  // Unified rendering function (Block Math -> HTML -> Inline Math -> Text)
  const resolveImageUrl = (url: string) => {
    if (!url) return '';
    if (url.startsWith('http')) return url;
    // Ensure 'images/' prefix for local backend static serving
    const cleanPath = url.replace(/^images\//, '');
    return `http://localhost:8088/images/${cleanPath}`;
  };

  const renderContent = (content: string) => {
    if (!content) return null;
    
    // 1. Block Math ($$ ... $$ 또는 \[ ... \]) 분리
    const blocks = content.split(/(\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\])/g);
    
    return blocks.map((block, i) => {
      // $$ ... $$ 또는 \[ ... \] 처리
      if ((block.startsWith('$$') && block.endsWith('$$')) || (block.startsWith('\\[') && block.endsWith('\\]'))) {
        const math = block.startsWith('$$') ? block.slice(2, -2) : block.slice(2, -2);
        return (
          <div key={i} className="my-4 overflow-x-auto">
            <BlockMath 
              math={math} 
              renderError={(error) => <div className="text-red-500 font-mono text-xs p-2 bg-red-50 rounded select-all border border-red-100">Math Error: {error.message} <br/> Raw: {math}</div>}
            />
          </div>
        );
      }
      
      // 2. Separate HTML (div including SVG)
      const htmlParts = block.split(/(<div[\s\S]*?<\/div>)/g);
      
      return htmlParts.map((htmlPart, j) => {
        if (htmlPart.startsWith('<div') && htmlPart.endsWith('</div>')) {
          return <div key={`${i}-${j}`} dangerouslySetInnerHTML={{ __html: htmlPart }} />;
        }
        
        // 3. Separate Image Markdown (![alt](url))
        const imageParts = htmlPart.split(/(!\[.*?\]\(.*?\))/g);
        
        return imageParts.map((imgPart, imgIdx) => {
          if (imgPart.startsWith('![') && imgPart.includes('](')) {
            const alt = imgPart.match(/!\[(.*?)\]/)?.[1] || 'image';
            const url = imgPart.match(/\((.*?)\)/)?.[1] || '';
            const fullUrl = resolveImageUrl(url);
            return (
              <div key={`${i}-${j}-${imgIdx}`} className="my-6 flex justify-center">
                <img 
                  src={fullUrl} 
                  alt={alt} 
                  className="max-w-full md:max-w-[85%] max-h-[400px] object-contain rounded-xl shadow-md border border-slate-100 transition-all hover:shadow-lg"
                />
              </div>
            );
          }

          // 4. Separate Inline Math ($ ... $ or \( ... \))
          const inlineParts = imgPart.split(/(\$\$[\s\S]*?\$\$|\$[\s\S]*?\$|\\\([\s\S]*?\\\))/g);

           return inlineParts.map((part, k) => {
             const isBlock = part.startsWith('$$') && part.endsWith('$$');
             const isMath = (part.startsWith('$') && part.endsWith('$')) || (part.startsWith('\\(') && part.endsWith('\\)'));
             
             if (isBlock) {
               const math = part.slice(2, -2);
               return (
                 <div key={`${i}-${j}-${imgIdx}-${k}`} className="overflow-x-auto py-2">
                   <BlockMath 
                     math={math} 
                     renderError={(error) => <div className="text-red-500 font-mono text-xs p-1 bg-red-50 rounded">Block Error: {math}</div>}
                   />
                 </div>
               );
             }
             if (isMath) {
               const math = part.startsWith('$') ? part.slice(1, -1) : part.slice(2, -2);
               return (
                 <InlineMath 
                   key={`${i}-${j}-${imgIdx}-${k}`} 
                   math={math} 
                   renderError={(error) => <span className="text-red-400 font-serif px-1 bg-red-50 text-[10px]" title={error.message}>({math})</span>}
                 />
               );
             }


            // Deduplication: Check if this text is a redundant fallback for the NEXT math part
            let textToRender = part;
            const nextPart = inlineParts[k + 1];
            if (nextPart && ((nextPart.startsWith('$') && nextPart.endsWith('$')) || (nextPart.startsWith('\\(') && nextPart.endsWith('\\)')))) {
              const nextMath = nextPart.startsWith('$') ? nextPart.slice(1, -1) : nextPart.slice(2, -2);
              const trimmedText = textToRender.trim();
              const trimmedMath = nextMath.trim();
              
              if (trimmedText && trimmedMath && (trimmedText === trimmedMath || trimmedText.endsWith(trimmedMath))) {
                // Determine if we should strip the redundancy
                const suffixIndex = textToRender.lastIndexOf(trimmedMath);
                if (suffixIndex !== -1) {
                  const afterSuffix = textToRender.slice(suffixIndex + trimmedMath.length);
                  if (afterSuffix.trim() === "") {
                    textToRender = textToRender.slice(0, suffixIndex);
                  }
                }
              }
            }

            if (!textToRender && k < inlineParts.length - 1) return null;
            return <span key={`${i}-${j}-${imgIdx}-${k}`}>{parseText(textToRender)}</span>;
          });
        });
      });
    });
  };

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Problem Area */}
      <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-sm border border-slate-200">
        {(band || metadata) && (
          <div className="flex items-center justify-between mb-4 flex-wrap gap-2">
            <div />
            {metadata && (
              <div className="flex flex-col items-end">
                <span className="text-[10px] text-slate-400 font-bold italic">
                  🧬 {metadata.domain}
                </span>
                {metadata.dna_tags && (
                   <div className="flex gap-1 mt-1 justify-end flex-wrap max-w-[200px]">
                    {metadata.dna_tags.map((tag: string, i: number) => (
                      <span key={i} className="text-[9px] text-slate-300 font-medium">#{tag}</span>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        )}
        <div className="text-lg sm:text-xl font-medium text-slate-800 leading-relaxed">
          {renderContent(problem.question)}
          {problem.image && !problem.question.includes(problem.image.split('/').pop() || '___') && (
            <div className="mt-6 flex justify-center">
              <img 
                src={resolveImageUrl(problem.image)} 
                alt="Problem Illustration" 
                className="max-w-full md:max-w-[85%] max-h-[400px] object-contain rounded-lg shadow-sm border border-slate-100 transition-all hover:shadow-md"
              />
            </div>
          )}
        </div>
      </div>

      {/* Answer Selection Area */}
      <div className="grid grid-cols-1 gap-3">
        {problem.options && problem.options.length > 0 ? (
          problem.options.map((opt: string, idx: number) => (
            <button
              key={idx}
              onClick={() => onAnswerClick(opt)}
              disabled={selectedAnswer !== null}
              className={`p-4 text-left rounded-xl border-2 transition-all ${
                selectedAnswer === opt
                  ? isCorrect
                    ? 'border-green-500 bg-green-50 text-green-700'
                    : 'border-red-500 bg-red-50 text-red-700'
                  : selectedAnswer !== null && String(opt) === String(problem.answer)
                  ? 'border-green-500 bg-green-50 text-green-700' // Show correct answer
                  : 'border-slate-100 hover:border-slate-300 hover:bg-slate-50'
              }`}
            >
              <span className="font-bold mr-2">{idx + 1}.</span>
              {renderContent(opt)}
            </button>
          ))
        ) : (
          <div className="bg-white p-6 rounded-xl border border-slate-200">
            <p className="text-slate-500 mb-4">This is a short-answer problem. Click the button below to check the answer.</p>
            <button
              onClick={() => onAnswerClick(problem.answer)}
              disabled={selectedAnswer !== null}
              className={`px-6 py-2 rounded-lg font-bold text-white ${themeClasses.button}`}
            >
              Check Answer
            </button>
          </div>
        )}
      </div>

      {/* Explanation Area */}
      {showExplanation && (
        <div className={`p-6 rounded-2xl border ${themeClasses.border} ${themeClasses.bg} animate-slide-up`}>
          <h3 className={`font-bold text-lg mb-3 ${themeClasses.text}`}>💡 Explanation</h3>
          <div className="space-y-2 text-slate-700">
            {Array.isArray(problem.explanation) 
              ? problem.explanation.map((line: string, i: number) => (
                  <div key={i} className="flex gap-2"><span className="text-slate-400">•</span><div>{renderContent(line)}</div></div>
                ))
              : renderContent(problem.explanation)
            }
          </div>
        </div>
      )}

      {/* Drill Bridge (Bridge to Drill) */}
      {onDrillClick && (
        <div className="group relative overflow-hidden bg-white p-1 rounded-2xl border border-slate-200 shadow-sm transition-all hover:shadow-md hover:border-indigo-200">
          <div className="absolute inset-0 bg-gradient-to-r from-indigo-50/50 to-purple-50/50 opacity-0 group-hover:opacity-100 transition-opacity" />
          <div className="relative w-full p-5 rounded-xl transition-all">
            <div className="flex items-center justify-between gap-4 mb-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 flex-shrink-0 bg-indigo-100 text-indigo-600 rounded-full flex items-center justify-center text-xl shadow-sm border border-indigo-50">
                  🧬
                </div>
                <div className="text-left">
                  <h4 className="font-black text-slate-800 text-sm uppercase tracking-tight">Struggling with this concept?</h4>
                  <p className="text-xs text-slate-500 font-medium">Pick a conceptual drill level to master the DNA of this problem.</p>
                </div>
              </div>
            </div>
            
            <div className="grid grid-cols-3 gap-2">
              {[1, 2, 3].filter(lvl => {
                // Determine available levels from metadata prop or problem metadata
                const config = metadata?.drill_config || problem?.metadata?.drill_config;
                if (config) {
                  return !!config[`L${lvl}`];
                }
                return true;
              }).map(lvl => (
                <button
                  key={lvl}
                  onClick={() => onDrillClick?.(lvl)}
                  className="py-2.5 rounded-xl border border-slate-200 bg-slate-50 text-slate-600 text-[10px] font-black uppercase tracking-tighter hover:bg-indigo-600 hover:text-white hover:border-indigo-600 transition-all shadow-sm flex items-center justify-center gap-1.5"
                >
                  <span className="opacity-60">LV{lvl}</span>
                  <span>{lvl === 1 ? 'Concept' : lvl === 2 ? 'Apply' : 'Master'}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}