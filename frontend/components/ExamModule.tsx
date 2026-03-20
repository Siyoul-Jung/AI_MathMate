import React from 'react';
import ProblemViewer from './ProblemViewer';
import Scratchpad from './Scratchpad';

interface ExamModuleProps {
  examProblems: any[];
  examAnswers: {[key: number]: any};
  currentExamIndex: number;
  setCurrentExamIndex: (idx: number | ((prev: number) => number)) => void;
  examSubmitted: boolean;
  examScore: number;
  examConfig: { count: number; timeLimit: number };
  timeLeft: number;
  formatTime: (seconds: number) => string;
  showScratchpad: boolean;
  setShowScratchpad: (show: boolean) => void;
  submitExam: (autoSubmit?: boolean) => void;
  handleExamAnswer: (answer: any) => void;
  themeColor: string;
  themeClasses: any;
  omrStyles: any;
  category: string;
  amcMode: string;
  handleDrillBridge?: (prob: any, level: number) => void;
}

const ExamModule: React.FC<ExamModuleProps> = ({
  examProblems,
  examAnswers,
  currentExamIndex,
  setCurrentExamIndex,
  examSubmitted,
  examScore,
  examConfig,
  timeLeft,
  formatTime,
  showScratchpad,
  setShowScratchpad,
  submitExam,
  handleExamAnswer,
  themeColor,
  themeClasses,
  omrStyles,
  category,
  amcMode,
  handleDrillBridge
}) => {
  return (
    <div className="animate-fade-in">
      {/* Top Info and Controls */}
      <div className="bg-white p-4 rounded-2xl shadow-sm border border-slate-200 mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-4">
          <span className={`text-lg font-bold ${themeClasses.text}`}>
            Question {currentExamIndex + 1} <span className="text-slate-400 text-sm">/ {examProblems.length}</span>
          </span>
          {!examSubmitted && examConfig.timeLimit > 0 && (
            <div className={`flex items-center gap-1 font-mono text-lg font-bold ${timeLeft < 60 ? 'text-red-500 animate-pulse' : 'text-slate-600'}`}>
              <span>⏱️</span>
              {formatTime(timeLeft)}
            </div>
          )}
          {examSubmitted && (
            <span className={`px-3 py-1 rounded-full text-sm font-bold ${examScore >= 80 ? 'bg-green-100 text-green-700' : 'bg-slate-100 text-slate-700'}`}>
              Score: {examScore}
            </span>
          )}
        </div>
        
        <div className="flex gap-2">
          <button
            onClick={() => setShowScratchpad(!showScratchpad)}
            className={`px-3 py-2 text-sm font-bold rounded-lg transition-all flex items-center gap-2 ${showScratchpad ? 'bg-slate-800 text-white' : 'bg-white border border-slate-200 text-slate-600 hover:bg-slate-50'}`}
          >
            <span>✏️</span> {showScratchpad ? 'Close Scratchpad' : 'Scratchpad'}
          </button>
          <button
            onClick={() => setCurrentExamIndex((prev: number) => Math.max(0, prev - 1))}
            disabled={currentExamIndex === 0}
            className="px-4 py-2 text-sm font-bold rounded-lg bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-50"
          >
            Prev
          </button>
          {currentExamIndex < examProblems.length - 1 ? (
            <button
              onClick={() => setCurrentExamIndex((prev: number) => Math.min(examProblems.length - 1, prev + 1))}
              className={`px-4 py-2 text-sm font-bold rounded-lg ${themeClasses.button} text-white`}
            >
              Next
            </button>
          ) : !examSubmitted ? (
            <button
              onClick={() => submitExam(false)}
              className="px-6 py-2 text-sm font-bold rounded-lg bg-red-500 hover:bg-red-600 text-white shadow-sm"
            >
              Submit
            </button>
          ) : null}
        </div>
      </div>

      <div className="relative">
        <ProblemViewer
          problem={examProblems[currentExamIndex]}
          selectedAnswer={examAnswers[currentExamIndex] || null}
          isCorrect={examSubmitted ? String(examAnswers[currentExamIndex]) === String(examProblems[currentExamIndex].answer) : null}
          showExplanation={examSubmitted}
          hintIndex={examSubmitted ? 99 : -1}
          onAnswerClick={handleExamAnswer}
          setHintIndex={() => {}}
          setShowExplanation={() => {}}
          themeColor={themeColor}
          onDrillClick={category === 'AIME' ? (lvl) => handleDrillBridge?.(examProblems[currentExamIndex], lvl) : undefined}
          band={examProblems[currentExamIndex].band}
          metadata={amcMode === 'DRILL' ? examProblems[currentExamIndex].metadata : null}
        />
        <Scratchpad isActive={showScratchpad} onClose={() => setShowScratchpad(false)} />
      </div>

      {/* OMR Card (Answer Status) */}
      <div className="mt-6 bg-white p-4 rounded-xl border border-slate-200 flex flex-wrap gap-2 justify-center">
        {examProblems.map((_, idx) => {
          const isAns = examAnswers[idx] !== undefined;
          const isCurr = currentExamIndex === idx;
          let statusClass = "bg-slate-50 border-slate-200 text-slate-400";
          
          if (examSubmitted) {
            const isCorr = String(examAnswers[idx]) === String(examProblems[idx].answer);
            statusClass = isCorr ? "bg-green-100 border-green-300 text-green-700" : "bg-red-100 border-red-300 text-red-700";
          } else if (isAns) {
            statusClass = omrStyles[themeColor as keyof typeof omrStyles];
          }
          
          return (
            <button
              key={idx}
              onClick={() => setCurrentExamIndex(idx)}
              className={`w-10 h-10 rounded-lg border flex items-center justify-center text-sm font-bold transition-all ${statusClass} ${isCurr ? 'ring-2 ring-offset-2 ring-slate-400' : ''}`}
            >
              {idx + 1}
            </button>
          );
        })}
      </div>
    </div>
  );
};

export default ExamModule;
