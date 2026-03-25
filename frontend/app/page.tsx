'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { CATEGORIES, GRADES_MAP, ALL_STANDARDS } from '../data/constants';
import Dashboard from '../components/Dashboard';
import ProblemViewer from '../components/ProblemViewer';
import Scratchpad from '../components/Scratchpad';
import GraphingCalculator from '../components/GraphingCalculator';
import AIMEModule from '../components/AIMEModule';
import PracticeModule from '../components/PracticeModule';
import ExamModule from '../components/ExamModule';
import ReviewNoteModule from '../components/ReviewNoteModule';
import { api } from '../lib/api';
import { renderContent } from '../lib/utils';
import 'katex/dist/katex.min.css';

export default function Home() {
  // --- UI View State ---
  const [isHome, setIsHome] = useState(true);

  // --- Selection State Management ---
  const [category, setCategory] = useState('AIME'); // Default: AIME
  const [grade, setGrade] = useState('AIME_1');      // Default: AIME 1
  const [standard, setStandard] = useState('');
  const [type, setType] = useState('');
  
  // --- Data State ---
  const [types, setTypes] = useState<{id: string, name: string}[]>([]);
  const [difficulty, setDifficulty] = useState('Normal');
  const [qType, setQType] = useState('multi'); 
  const [problem, setProblem] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  
  // Grading State Management
  const [selectedAnswer, setSelectedAnswer] = useState<any>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);

  // --- Drill-only State ---
  const [drillProblem, setDrillProblem] = useState<any>(null);
  const [drillSelectedAnswer, setDrillSelectedAnswer] = useState<any>(null);
  const [drillIsCorrect, setDrillIsCorrect] = useState<boolean | null>(null);
  const [drillShowExplanation, setDrillShowExplanation] = useState(false);

  // Refs for scrolling
  const drillRef = useRef<HTMLDivElement>(null);

  // --- Scroll Handling on Drill Creation ---
  useEffect(() => {
    if (drillProblem && drillRef.current) {
      drillRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }, [drillProblem]);

  // Analysis Data State
  const [studentId, setStudentId] = useState('student_001'); 
  const [analysis, setAnalysis] = useState<any>(null);
  const [advice, setAdvice] = useState<string>('');
  const [hintIndex, setHintIndex] = useState(-1); 
  const [showDashboard, setShowDashboard] = useState(false);
  
  // Review Note (Wrong Note) State
  const [wrongAnswers, setWrongAnswers] = useState<any[]>([]);
  const [showWrongNote, setShowWrongNote] = useState(false);
  const [expandedStandards, setExpandedStandards] = useState<Set<string>>(new Set());
  const [activeTab, setActiveTab] = useState<'settings' | 'problem'>('settings');
  const [activeMode, setActiveMode] = useState<'study' | 'exam'>('study');
  const [showScratchpad, setShowScratchpad] = useState(false);
  const [showGraph, setShowGraph] = useState(false);

  // Mock Exam State
  const [examConfig, setExamConfig] = useState({ count: 5, timeLimit: 0 });
  const [examProblems, setExamProblems] = useState<any[]>([]);
  const [examAnswers, setExamAnswers] = useState<{[key: number]: any}>({});
  const [currentExamIndex, setCurrentExamIndex] = useState(0);
  const [examSubmitted, setExamSubmitted] = useState(false);
  const [examScore, setExamScore] = useState(0);
  const [timeLeft, setTimeLeft] = useState(0);


  // --- AMC / AIME Exclusive State ---
  const [amcProblemNum, setAmcProblemNum] = useState<string>('');
  const [amcMode, setAmcMode] = useState<'MOCK' | 'DRILL'>('MOCK');
  const [drillLevel, setDrillLevel] = useState<number>(1);
  const [amcLevels, setAmcLevels] = useState<number[]>([1, 2, 3]); 
  const [amcBand, setAmcBand] = useState<string>('CHALLENGER');
  const [amcMetadata, setAmcMetadata] = useState<any>(null);
  const [amcArchives, setAmcArchives] = useState<any>({});
  const [amcYear, setAmcYear] = useState<string>('2025');
  const [amcExam, setAmcExam] = useState<string>('AIME1');

  // Filter standards corresponding to the currently selected grade
  const currentStandards = ALL_STANDARDS.filter(s => s.grade === grade);

  // --- Theme Settings ---
  const categoryToColor: {[key: string]: 'indigo' | 'purple' | 'emerald'} = {
    'AMC_10': 'indigo',
    'AMC_12': 'purple',
    'AIME': 'emerald'
  };
  const themeColor = categoryToColor[category] || 'emerald';
  
  const themes = {
    indigo: {
      text: 'text-indigo-700',
      bg: 'bg-indigo-50',
      border: 'border-indigo-100',
      button: 'bg-indigo-600 hover:bg-indigo-700',
      ring: 'ring-indigo-200',
      active: 'bg-indigo-100 text-indigo-700 ring-2 ring-indigo-200',
      selectFocus: 'focus:ring-indigo-500 focus:border-indigo-500',
      selectHover: 'hover:border-indigo-300',
    },
    purple: {
      text: 'text-purple-700',
      bg: 'bg-purple-50',
      border: 'border-purple-100',
      button: 'bg-purple-600 hover:bg-purple-700',
      ring: 'ring-purple-200',
      active: 'bg-purple-100 text-purple-700 ring-2 ring-purple-200',
      selectFocus: 'focus:ring-purple-500 focus:border-purple-500',
      selectHover: 'hover:border-purple-300',
    },
    emerald: {
      text: 'text-emerald-700',
      bg: 'bg-emerald-50',
      border: 'border-emerald-100',
      button: 'bg-emerald-600 hover:bg-emerald-700',
      ring: 'ring-emerald-200',
      active: 'bg-emerald-100 text-emerald-700 ring-2 ring-emerald-200',
      selectFocus: 'focus:ring-emerald-500 focus:border-emerald-500',
      selectHover: 'hover:border-emerald-300',
    }
  };
  const themeClasses = themes[themeColor];

  const omrStyles = {
    indigo: 'bg-indigo-100 border-indigo-300 text-indigo-700',
    purple: 'bg-purple-100 border-purple-300 text-purple-700',
    emerald: 'bg-emerald-100 border-emerald-300 text-emerald-700',
  };

  // --- Event Handlers & Effects ---

  // 1. When category changes -> auto-select first grade
  const handleCategoryChange = (newCategory: string) => {
    setCategory(newCategory);
    const availableGrades = GRADES_MAP[newCategory] || [];
    if (availableGrades.length > 0) {
      setGrade(availableGrades[0].id); 
    } else {
      setGrade('');
    }
  };

  // 2. When grade changes -> auto-select first standard
  useEffect(() => {
    if (currentStandards.length > 0) {
      setStandard(currentStandards[0].id);
    } else {
      setStandard('');
    }
  }, [grade]);

  // 3. When standard changes -> fetch problem type list
  useEffect(() => {
    async function fetchTypes() {
      if (!standard) { setTypes([]); setType(''); return; }
      try {
        const data = await api.fetchTypes(standard, grade);
        setTypes(data.types || []);
        if (data.types && data.types.length > 0) {
          setType(data.types[0].id);
        } else {
          setType('');
        }
      } catch (error) {
        console.error('Failed to fetch types:', error);
        setTypes([]);
        setType('');
      }
    }
    fetchTypes();
  }, [standard, grade]);

  // Fetch analysis data
  const fetchAnalysis = async () => {
    try {
      const data = await api.fetchAnalysis(studentId);
      setAnalysis(data);
    } catch (error) {
      console.error('Failed to fetch analysis:', error);
    }
  };

  // Fetch learning advice
  const fetchAdvice = async () => {
    try {
      const data = await api.fetchAdvice(studentId, category);
      setAdvice(data.advice);
    } catch (error) {
      console.error('Failed to fetch advice:', error);
    }
  };

  // Fetch AIME Archives
  useEffect(() => {
    if (category === 'AIME') {
      api.fetchAmcArchives().then(data => {
        setAmcArchives(data.archives || {});
      });
    }
  }, [category]);


  // Fetch AIME drill level metadata
  useEffect(() => {
    if (category === 'AIME' && grade === 'AIME_1' && amcProblemNum) {
      api.fetchAmcLevels(amcProblemNum, amcYear, amcExam)
        .then(data => {
          const levels = data.levels || [1, 2, 3];
          setAmcLevels(levels);
          setAmcBand(data.band || 'CHALLENGER');
          setAmcMetadata(data.metadata || null);
          if (!levels.includes(drillLevel)) {
            setDrillLevel(levels[0]);
          }
        })
        .catch(err => {
          console.error('Failed to fetch AIME levels:', err);
          setAmcLevels([1, 2, 3]);
        });
    }
  }, [amcProblemNum, amcYear, amcExam, category, grade]);

  // Clear AIME metadata when mission is unselected
  useEffect(() => {
    if (category === 'AIME' && grade === 'AIME_1' && !amcProblemNum) {
      setAmcMetadata(null);
    }
  }, [amcProblemNum, category, grade]);

  // Problem generation request
  const generateProblem = async (pIdOverride?: string, modeOverride?: string, levelOverride?: number) => {
    if (category === 'AIME' && grade === 'AIME_1') {
      let targetPid = pIdOverride || amcProblemNum;
      const targetMode = modeOverride || amcMode;
      const targetLevel = levelOverride || drillLevel;

      if (targetMode === 'MOCK' || (!targetPid && amcBand)) {
        let problems: string[] = [];
        if (amcBand === 'CHALLENGER') problems = ['P01', 'P02', 'P03', 'P04', 'P05'];
        else if (amcBand === 'EXPERT') problems = ['P06', 'P07', 'P08', 'P09', 'P10'];
        else if (amcBand === 'MASTER') problems = ['P11', 'P12', 'P13', 'P14', 'P15'];
        
        const implemented = ['P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07', 'P08', 'P09', 'P10', 'P11', 'P12', 'P13', 'P14', 'P15'];
        const available = problems.filter(p => implemented.includes(p));
        
        if (available.length > 1) {
          // Exclude current mission to avoid "stagnant" content perception
          const others = available.filter(p => p !== amcProblemNum);
          targetPid = others[Math.floor(Math.random() * others.length)];
        } else if (available.length === 1) {
          targetPid = available[0];
        }
        
        if (targetPid) {
          setAmcProblemNum(targetPid);
        }
      }

      if (!targetPid) {
        alert('Please select an AIME problem or learning phase.');
        return;
      }
      
      setLoading(true);
      try {
        const data = await api.generateAmcProblem(targetPid, targetMode, targetLevel, amcYear, amcExam);
        
        if (data.status === 'REGENERATING' || data.error === 'MISSION_BEING_CLEANSED') {
          // Special handling for background cleansing/generation
          alert(`🧬 High-fidelity regeneration in progress for ${targetPid}. Please try another mission for a moment or wait 30-60s for the deep cleansing to finish.`);
          setLoading(false);
          return;
        }

        if (data.error) {
          console.error('API Error:', data.error);
          alert(`Problem Generation Failed: ${data.error}`);
          setLoading(false);
          return;
        }

        if (targetMode === 'DRILL') {
          setDrillProblem({ ...data, p_id: targetPid });
          setDrillSelectedAnswer(null);
          setDrillIsCorrect(null);
          setDrillShowExplanation(false);
          setShowExplanation(false); 
          if (data.metadata) setAmcMetadata(data.metadata);
        } else {
          setProblem({ ...data, standard_id: standard, p_id: targetPid });
          setAmcMetadata(data.metadata || null);
          setDrillProblem(null);
          setSelectedAnswer(null);
          setIsCorrect(null);
          setShowExplanation(false);
          setHintIndex(-1);
        }
        
        setActiveTab('problem');
        setShowScratchpad(false);
        setShowGraph(false);
      } catch (error) {
        console.error('Failed to generate AIME problem:', error);
        alert('Failed to generate AIME problem.');
      } finally {
        setLoading(false);
      }
      return;
    }

    if (!type) return;
    setLoading(true);
    try {
      const data = await api.generateProblem(standard, type, difficulty, qType, grade);
      setProblem({ ...data, standard_id: standard });
      setDrillProblem(null); 
      setSelectedAnswer(null);
      setIsCorrect(null);
      setShowExplanation(false);
      setHintIndex(-1); 
      setActiveTab('problem');
      setShowScratchpad(false); 
      setShowGraph(false);
      setExamProblems([]); 
    } catch (error) {
      console.error('Failed to generate problem:', error);
      alert('Failed to generate problem. Please check if the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

  // Drill bridge handler
  const handleDrillBridge = (prob: any, level: number) => {
    if (!prob) return;
    setActiveMode('study');
    setCategory('AIME');
    // We stay in MOCK mode to keep the bridge context, but we will show the drillProblem UI
    setActiveTab('problem');
    const pid = prob.p_id || 'P01';
    setAmcProblemNum(pid);
    setDrillLevel(level);
    generateProblem(pid, 'DRILL', level);
  };

  // Mock Exam generation request
  const startExam = async () => {
    if (!grade || currentStandards.length === 0) {
      alert("Please select a grade first.");
      return;
    }
    
    setLoading(true);
    try {
      const questionsToGenerate = [];
      for (let i = 0; i < examConfig.count; i++) {
        const randomStd = currentStandards[Math.floor(Math.random() * currentStandards.length)];
        questionsToGenerate.push(randomStd);
      }
      
      const uniqueStdIds = [...new Set(questionsToGenerate.map(s => s.id))];
      const typesMap: {[key: string]: any[]} = {};
      
      await Promise.all(uniqueStdIds.map(async (stdId) => {
        try {
          const data = await api.fetchTypes(stdId, grade);
          typesMap[stdId] = data.types || [];
        } catch (e) {
          console.error(e);
          typesMap[stdId] = [];
        }
      }));

      const problemPromises = questionsToGenerate.map(std => {
        const stdTypes = typesMap[std.id];
        if (!stdTypes || stdTypes.length === 0) return null;
        const randomType = stdTypes[Math.floor(Math.random() * stdTypes.length)];
        return api.generateProblem(std.id, randomType.id, difficulty, qType, grade)
            .then(data => ({ ...data, standard_id: std.id }));
      }).filter(p => p !== null);

      const results = await Promise.all(problemPromises as Promise<any>[]);
      
      if (results.length === 0) {
        alert("Failed to generate problem.");
        setLoading(false);
        return;
      }

      setExamProblems(results);
      setExamAnswers({});
      setCurrentExamIndex(0);
      setExamSubmitted(false);
      setExamScore(0);
      setTimeLeft(examConfig.timeLimit * 60);
      setShowScratchpad(false);
    } catch (error) {
      console.error('Failed to generate exam:', error);
      alert('An error occurred while generating the mock exam.');
    } finally {
      setLoading(false);
    }
  };

  // Save learning history log
  const logStep = async (status: string) => {
    if (!problem) return;
    try {
      await api.logStep({
          student_id: studentId,
          standard_id: standard,
          step_type: 'CALC', 
          success_status: status
      });
      fetchAnalysis();
    } catch (error) {
      console.error('Failed to log step:', error);
    }
  };

  // Answer check handler
  const handleAnswerClick = (answer: any, isDrill: boolean = false) => {
    const targetProblem = isDrill ? drillProblem : problem;
    const currentSelected = isDrill ? drillSelectedAnswer : selectedAnswer;
    
    if (!targetProblem || currentSelected !== null) return;
    const correct = String(answer) === String(targetProblem.answer);
    
    if (isDrill) {
      setDrillSelectedAnswer(answer);
      setDrillIsCorrect(correct);
      setDrillShowExplanation(true);
    } else {
      setSelectedAnswer(answer);
      setIsCorrect(correct);
      setShowExplanation(true); 
      logStep(correct ? 'SELF' : 'FAIL');

      if (!correct) {
        if (!targetProblem.savedAt) {
          setWrongAnswers(prev => [...prev, { ...targetProblem, savedAt: new Date() }]);
        }
      } else if (targetProblem.savedAt) {
        setWrongAnswers(prev => prev.filter(p => {
          const t1 = p.savedAt instanceof Date ? p.savedAt.getTime() : new Date(p.savedAt).getTime();
          const t2 = targetProblem.savedAt instanceof Date ? targetProblem.savedAt.getTime() : new Date(targetProblem.savedAt).getTime();
          return t1 !== t2;
        }));
      }
    }
  };

  // Mock Exam answer selection handler
  const handleExamAnswer = (answer: any) => {
    if (examSubmitted) return;
    setExamAnswers(prev => ({
      ...prev,
      [currentExamIndex]: answer
    }));
  };

  // Mock Exam submission and grading
  const submitExam = useCallback((autoSubmit = false) => {
    if (!autoSubmit && typeof window !== 'undefined' && !window.confirm('Do you want to submit your answers and get graded?')) return;
    
    let correctCount = 0;
    examProblems.forEach((prob, idx) => {
      if (String(examAnswers[idx]) === String(prob.answer)) {
        correctCount++;
      }
    });
    setExamScore(Math.round((correctCount / examProblems.length) * 100));
    setExamSubmitted(true);
    if (autoSubmit) {
      if (typeof window !== 'undefined') window.alert("Time is up! Your answers have been automatically submitted.");
    }
  }, [examProblems, examAnswers]);

  // Timer Logic
  useEffect(() => {
    if (activeMode !== 'exam' || examSubmitted || examConfig.timeLimit === 0) return;
    if (timeLeft <= 0) {
      submitExam(true);
      return;
    }
    const timer = setInterval(() => {
      setTimeLeft(prev => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [activeTab, examSubmitted, examConfig.timeLimit, timeLeft, submitExam]);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? '0' : ''}${s}`;
  };

  // Move to the corresponding standard and prepare problem generation when clicking a weak point
  const handleWeakPointClick = (weakStandardId: string) => {
    const targetStd = ALL_STANDARDS.find(s => s.id === weakStandardId);
    if (targetStd) {
      let targetCategory = '';
      for (const [catId, grades] of Object.entries(GRADES_MAP)) {
        if (grades.some(g => g.id === targetStd.grade)) {
          targetCategory = catId;
          break;
        }
      }

      if (targetCategory) {
        setCategory(targetCategory);
        setGrade(targetStd.grade);
        setStandard(weakStandardId);
        setShowDashboard(false); 
        setProblem(null);
        setSelectedAnswer(null);
        setIsCorrect(null);
        setShowExplanation(false);
        setHintIndex(-1);
        setActiveTab('settings');
        setActiveMode('study');
        setExamProblems([]);
      }
    }
  };

  // Retry problem from review note
  const handleRetryProblem = (savedProblem: any) => {
    setProblem(savedProblem);
    setSelectedAnswer(null);
    setIsCorrect(null);
    setShowExplanation(false);
    setHintIndex(-1);
    setShowWrongNote(false);
    setActiveTab('problem');
    setActiveMode('study');
    setShowScratchpad(false);
    setShowGraph(false);
    setExamProblems([]);
  };

  const toggleStandard = (stdId: string) => {
    setExpandedStandards(prev => {
      const next = new Set(prev);
      if (next.has(stdId)) next.delete(stdId);
      else next.add(stdId);
      return next;
    });
  };

  // Wrapper for category selection from Home
  const selectCategory = (catId: string) => {
    if (catId === 'AMC_10' || catId === 'AMC_12') {
      if (typeof window !== 'undefined') window.alert(`${catId} is coming soon!`);
      return;
    }
    handleCategoryChange(catId);
    setIsHome(false);
    setActiveMode('study');
    setProblem(null);
    setSelectedAnswer(null);
    setIsCorrect(null);
    setShowExplanation(false);
    setHintIndex(-1);
    setShowDashboard(false);
    setShowWrongNote(false);
    setActiveTab('settings');
    setShowScratchpad(false);
    setShowGraph(false);
    setExamProblems([]);
    setAmcMode('MOCK');
    setAmcBand('CHALLENGER');
    setAmcProblemNum('P01');
    setDrillLevel(1);
  };

  if (isHome) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 to-blue-100 flex flex-col items-center justify-center p-4 font-sans">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-extrabold text-indigo-900 mb-4 tracking-tight">AI MathMate</h1>
          <p className="text-xl text-indigo-700">AI-Powered Personalized Math Learning</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl w-full">
          {/* AMC 10 Card (Locked) */}
          <button 
            onClick={() => selectCategory('AMC_10')}
            className="bg-white/80 p-8 rounded-2xl shadow-lg border border-indigo-100 flex flex-col items-center group relative overflow-hidden grayscale cursor-not-allowed"
          >
            <div className="absolute top-2 right-2 bg-slate-800 text-white text-[10px] font-bold px-2 py-0.5 rounded-full z-10">COMING SOON</div>
            <div className="w-20 h-20 bg-indigo-50 rounded-full flex items-center justify-center mb-6">
              <span className="text-4xl opacity-50">🔟</span>
            </div>
            <h2 className="text-2xl font-bold text-slate-400 mb-2">AMC 10</h2>
            <p className="text-slate-400 text-center text-sm">Target: Grades 10 & below<br/>Coming Soon</p>
          </button>

          {/* AMC 12 Card (Locked) */}
          <button 
            onClick={() => selectCategory('AMC_12')}
            className="bg-white/80 p-8 rounded-2xl shadow-lg border border-indigo-100 flex flex-col items-center group relative overflow-hidden grayscale cursor-not-allowed"
          >
            <div className="absolute top-2 right-2 bg-slate-800 text-white text-[10px] font-bold px-2 py-0.5 rounded-full z-10">COMING SOON</div>
            <div className="w-20 h-20 bg-purple-50 rounded-full flex items-center justify-center mb-6">
              <span className="text-4xl opacity-50">🔢</span>
            </div>
            <h2 className="text-2xl font-bold text-slate-400 mb-2">AMC 12</h2>
            <p className="text-slate-400 text-center text-sm">Target: Grades 12 & below<br/>Coming Soon</p>
          </button>

          {/* AIME Card (Active) */}
          <button 
            onClick={() => selectCategory('AIME')}
            className="bg-white p-8 rounded-2xl shadow-xl hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 border border-emerald-100 flex flex-col items-center group"
          >
            <div className="absolute top-2 right-2 bg-emerald-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full z-10">ACTIVE</div>
            <div className="w-20 h-20 bg-emerald-100 rounded-full flex items-center justify-center mb-6 group-hover:bg-emerald-200 transition-colors">
              <span className="text-4xl">🏆</span>
            </div>
            <h2 className="text-2xl font-bold text-slate-800 mb-2">AIME</h2>
            <p className="text-slate-500 text-center text-sm">AIME Preparation<br/>The Ultimate Challenge</p>
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10 shadow-sm">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button 
               onClick={() => setIsHome(true)}
              className="text-slate-400 hover:text-slate-600 transition-colors p-1 rounded-full hover:bg-slate-100"
              title="Return to Home"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
              </svg>
            </button>
            <h1 className={`text-xl font-bold ${themeClasses.text} cursor-pointer`} onClick={() => setIsHome(true)}>AI MathMate</h1>
            <span className={`px-3 py-1 ${themeClasses.bg} ${themeClasses.text} text-xs font-bold rounded-full border ${themeClasses.border}`}>
              {CATEGORIES.find(c => c.id === category)?.name}
            </span>
          </div>
          
          <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 no-scrollbar w-full sm:w-auto justify-end">
            <button 
               onClick={() => { setActiveMode('study'); setShowWrongNote(false); setShowDashboard(false); }}
              className={`text-sm font-semibold px-3 sm:px-4 py-2 rounded-lg transition-all flex items-center gap-2 whitespace-nowrap flex-shrink-0 ${activeMode === 'study' && !showWrongNote && !showDashboard ? themeClasses.active : 'text-slate-600 hover:bg-slate-100'}`}
              title="Practice"
            >
              <span>📖</span>
              <span className="hidden sm:inline">Practice</span>
            </button>
            <button 
               onClick={() => { setShowWrongNote(true); setShowDashboard(false); }}
              className={`text-sm font-semibold px-3 sm:px-4 py-2 rounded-lg transition-all flex items-center gap-2 whitespace-nowrap flex-shrink-0 ${showWrongNote ? themeClasses.active : 'text-slate-600 hover:bg-slate-100'}`}
              title="Review Note"
            >
              <span>📒</span>
              <span className="hidden sm:inline">Review Note</span>
              {wrongAnswers.length > 0 && (
                <span className="bg-red-500 text-white text-xs font-bold px-1.5 py-0.5 rounded-full">{wrongAnswers.length}</span>
              )}
            </button>
            <button 
               onClick={() => { setActiveMode('exam'); setShowWrongNote(false); setShowDashboard(false); }}
              className={`text-sm font-semibold px-3 sm:px-4 py-2 rounded-lg transition-all flex items-center gap-2 whitespace-nowrap flex-shrink-0 ${activeMode === 'exam' && !showWrongNote && !showDashboard ? themeClasses.active : 'text-slate-600 hover:bg-slate-100'}`}
              title="Mock Exam"
            >
              <span>💯</span>
              <span className="hidden sm:inline">Mock Exam</span>
            </button>
            <button 
               onClick={() => { setShowDashboard(true); setShowWrongNote(false); }}
              className={`text-sm font-semibold px-3 sm:px-4 py-2 rounded-lg transition-all flex items-center gap-2 whitespace-nowrap flex-shrink-0 ${showDashboard ? themeClasses.active : 'text-slate-600 hover:bg-slate-100'}`}
              title="My Analysis"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
                <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
              </svg>
              <span className="hidden sm:inline">My Analysis</span>
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto py-8 px-4 sm:px-6 pb-24 flex-grow w-full max-w-3xl">

        {/* Learning Analysis Dashboard */}
        {showDashboard && analysis && (
          <Dashboard 
            analysis={analysis} 
            advice={advice} 
            onWeakPointClick={handleWeakPointClick} 
            themeColor={themeColor}
            category={category}
          />
        )}

        {/* Review Note Screen */}
        {showWrongNote && (
          <ReviewNoteModule
            wrongAnswers={wrongAnswers}
            expandedStandards={expandedStandards}
            toggleStandard={toggleStandard}
            renderContent={renderContent}
            handleRetryProblem={handleRetryProblem}
            themeClasses={themeClasses}
          />
        )}

        {/* Main Content (Visible only when Dashboard/Review Note are closed) */}
        {!showDashboard && !showWrongNote && (
        <>
        {/* Study Mode Settings Tab */}
        {activeMode === 'study' && (
          <div className="flex border-b border-slate-200 mb-6">
            <button
              onClick={() => {
                setActiveTab('settings');
              }}
              className={`flex-1 py-3 text-sm font-bold text-center transition-all border-b-2 ${
                activeTab === 'settings'
                  ? `${themeClasses.text} border-current` 
                  : 'text-slate-400 border-transparent hover:text-slate-600'
              }`}
            >
              Learning Settings
            </button>
            <button
              onClick={() => problem && setActiveTab('problem')}
              disabled={!problem}
              className={`flex-1 py-3 text-sm font-bold text-center transition-all border-b-2 ${
                activeTab === 'problem'
                  ? `${themeClasses.text} border-current`
                  : 'text-slate-400 border-transparent text-slate-400 opacity-50 cursor-not-allowed hover:text-slate-600'
              }`}
            >
              Problem Solving
            </button>
          </div>
        )}

        {/* Settings Tab */}
        {activeMode === 'study' && activeTab === 'settings' ? (
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 mb-8 animate-fade-in">
            {category === 'AIME' && grade === 'AIME_1' ? (
                <AIMEModule 
                  loading={loading}
                  amcMode={amcMode}
                  setAmcMode={setAmcMode}
                  amcBand={amcBand}
                  setAmcBand={setAmcBand}
                  amcProblemNum={amcProblemNum}
                  setAmcProblemNum={setAmcProblemNum}
                  amcYear={amcYear}
                  setAmcYear={setAmcYear}
                  amcExam={amcExam}
                  setAmcExam={setAmcExam}
                  amcLevels={amcLevels}
                  drillLevel={drillLevel}
                  setDrillLevel={setDrillLevel}
                  amcMetadata={amcMetadata}
                  amcArchives={amcArchives}
                  themeClasses={themeClasses}
                  onGenerate={() => generateProblem()}
                />
            ) : (
              <PracticeModule
                grade={grade}
                setGrade={setGrade}
                standard={standard}
                setStandard={setStandard}
                type={type}
                setType={setType}
                difficulty={difficulty}
                setDifficulty={setDifficulty}
                qType={qType}
                setQType={setQType}
                grades={GRADES_MAP[category] || []}
                standards={currentStandards}
                types={types}
                themeClasses={themeClasses}
              />
            )}
            {activeMode === 'study' && (
              <div className="mt-8 pt-6 border-t border-slate-100 flex justify-center">
                <button 
                  onClick={() => generateProblem()}
                  disabled={loading || (category === 'AIME' && grade === 'AIME_1' 
                    ? (amcMode === 'DRILL' && !amcProblemNum) 
                    : !type)}
                  className={`w-full py-4 ${themeClasses.button} text-white font-bold rounded-xl transition-all disabled:bg-slate-300 disabled:cursor-not-allowed shadow-md hover:shadow-lg transform hover:-translate-y-0.5 active:translate-y-0`}
                >
                  {loading ? 'Generating...' : 'Generate Problem'}
                </button>
              </div>
            )}
          </div>
        ) : null}


        {/* Mock Exam Tab */}
        {activeMode === 'exam' && (
          <ExamModule
            examProblems={examProblems}
            examAnswers={examAnswers}
            currentExamIndex={currentExamIndex}
            setCurrentExamIndex={setCurrentExamIndex}
            examSubmitted={examSubmitted}
            examScore={examScore}
            examConfig={examConfig}
            timeLeft={timeLeft}
            formatTime={formatTime}
            showScratchpad={showScratchpad}
            setShowScratchpad={setShowScratchpad}
            submitExam={submitExam}
            handleExamAnswer={handleExamAnswer}
            themeColor={themeColor}
            themeClasses={themeClasses}
            omrStyles={omrStyles}
            category={category}
            amcMode={amcMode}
            handleDrillBridge={handleDrillBridge}
          />
        )}

        {/* Problem Solving Tab */}
        {activeMode === 'study' && activeTab === 'problem' && (problem || drillProblem) && (
          <>
            <div className="bg-white p-5 rounded-2xl shadow-sm border border-slate-100 mb-8 flex flex-col md:flex-row items-center justify-between gap-5 animate-fade-in flex-wrap">
             <div className="flex flex-col items-center sm:items-start">
                {category === 'AIME' ? (
                  <>
                    <div className="flex items-center gap-2 mb-1.5 flex-wrap">
                      <span className={`px-2 py-0.5 rounded-md text-[9px] font-black uppercase tracking-wider border ${
                        (problem?.band || amcBand) === 'MASTER' ? 'bg-rose-50 text-rose-600 border-rose-100' : 
                        (problem?.band || amcBand) === 'EXPERT' ? 'bg-indigo-50 text-indigo-600 border-indigo-100' : 
                        'bg-blue-50 text-blue-600 border-blue-100'
                      }`}>
                        {(problem?.band || amcBand) === 'MASTER' ? 'MASTER PHASE' : (problem?.band || amcBand) === 'EXPERT' ? 'EXPERT PHASE' : 'CHALLENGER PHASE'}
                      </span>
                      <span className="text-[10px] text-slate-300 font-medium">•</span>
                      <span className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">
                        AIME MODULE
                      </span>
                      {problem?.engine_id && (
                        <span className="ml-1 px-2 py-0.5 bg-slate-50 text-slate-400 text-[9px] font-bold tracking-tight rounded border border-slate-100 italic">
                          source: {problem.engine_id.replace(/aime/g, 'AIME').replace(/p/g, 'P').replace(/-/g, ' ')}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-3">
                      <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
                        Current Challenge
                      </h2>
                      {amcMode !== 'DRILL' && (
                        <div className="flex items-center gap-1.5 px-2 py-1 bg-slate-50 text-slate-400 rounded-lg border border-slate-100 group cursor-help transition-all hover:bg-white" title="Insights will be unlocked upon submission">
                          <span className="text-[10px] font-bold uppercase tracking-tighter italic">Locked</span>
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                          </svg>
                        </div>
                      )}
                    </div>
                     {amcMode !== 'DRILL' && (
                        <p className="text-[11px] text-slate-400 font-medium mt-1 leading-none">
                          Details and conceptual DNA will be revealed after submission.
                        </p>
                     )}
                  </>
                ) : (
                  <>
                    <span className="text-xs text-slate-500 font-bold uppercase tracking-wider mb-1">Current Session</span>
                    <span className="text-sm font-medium text-slate-700 text-center sm:text-left">
                      {GRADES_MAP[category]?.find(g => g.id === grade)?.name} &gt; {types.find(t => t.id === type)?.name || 'Select Subtopic'} ({difficulty})
                    </span>
                  </>
                )}
             </div>
              <div className="flex flex-wrap gap-2 w-full md:w-auto justify-center md:justify-end">
                <button
                  onClick={() => setShowScratchpad(!showScratchpad)}
                  className={`flex-1 md:flex-none px-4 py-2.5 text-xs font-black uppercase tracking-tight rounded-xl transition-all flex items-center justify-center gap-2 ${showScratchpad ? 'bg-slate-900 text-white shadow-lg ring-4 ring-slate-100' : 'bg-white border border-slate-200 text-slate-600 hover:border-slate-300 hover:shadow-sm'}`}
                >
                  <span className="text-sm">✏️</span>
                  {showScratchpad ? 'Hide Pad' : 'Scratchpad'}
                </button>
                <button
                  onClick={() => setShowGraph(true)}
                  className="flex-1 md:flex-none px-4 py-2.5 text-xs font-black uppercase tracking-tight bg-white border border-slate-200 text-slate-600 rounded-xl hover:border-slate-300 hover:shadow-sm transition-all flex items-center justify-center gap-2"
                >
                  <span className="text-sm">📈</span>
                  Graph
                </button>
                <button
                  onClick={() => generateProblem()}
                  disabled={loading || amcMode === 'DRILL' || !!drillProblem}
                  className={`flex-1 md:flex-none px-5 py-2.5 text-xs font-black uppercase tracking-tight text-white rounded-xl ${themeClasses.button} shadow-md hover:shadow-lg transition-all flex items-center justify-center gap-2 ${(amcMode === 'DRILL' || !!drillProblem) ? 'opacity-20 cursor-not-allowed grayscale shadow-none' : ''}`}
                  title={amcMode === 'DRILL' ? "Next Problem navigation is for Mock mode only. Use Shuffle below for variants." : drillProblem ? "Close Drill Workshop to continue Mock." : ""}
                >
                  {loading ? (
                    <>
                      <svg className="animate-spin h-3 w-3 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Loading
                    </>
                  ) : 'Next Question'}
                </button>
             </div>
            </div>

            <div className="relative space-y-12">
              {/* Main Mock Problem */}
              {problem && (
                <div className={drillProblem ? "opacity-60 grayscale-[0.5] transition-all mb-12" : "mb-12"}>
                  <ProblemViewer
                    problem={problem}
                    selectedAnswer={selectedAnswer}
                    isCorrect={isCorrect}
                    showExplanation={showExplanation}
                    hintIndex={hintIndex}
                    onAnswerClick={(ans) => handleAnswerClick(ans, false)}
                    setHintIndex={setHintIndex}
                    setShowExplanation={setShowExplanation}
                    themeColor={themeColor}
                    onDrillClick={category === 'AIME' && !drillProblem ? (lvl) => handleDrillBridge(problem, lvl) : undefined}
                    band={problem.band}
                    metadata={null}
                  />
                </div>
              )}

              {/* Drill Workshop (Scaffolding Area) */}
              {drillProblem && (
                <div 
                  ref={drillRef}
                  className="bg-indigo-50/50 p-6 rounded-3xl border-2 border-indigo-200 shadow-xl animate-in zoom-in-95 duration-300"
                >
                  <div className="flex items-center justify-between mb-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-indigo-600 text-white rounded-xl flex items-center justify-center shadow-lg font-bold">
                        🧬
                      </div>
                      <div>
                        <h4 className="text-sm font-black text-indigo-900 uppercase tracking-tighter">Drill Workshop</h4>
                        <p className="text-[10px] text-indigo-500 font-bold uppercase tracking-widest">Mastering the underlying DNA</p>
                      </div>
                    </div>
                    <div className="flex gap-2">
                      <button
                        onClick={() => generateProblem(amcProblemNum, 'DRILL', drillLevel)}
                        disabled={loading}
                        className="flex items-center gap-1.5 px-3 py-1.5 bg-white text-indigo-600 text-[10px] font-black uppercase rounded-lg border border-indigo-100 shadow-sm hover:shadow-md hover:bg-indigo-50 transition-all disabled:opacity-50"
                      >
                        {loading ? (
                          <svg className="animate-spin h-3 w-3" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                        ) : '🔄 Shuffle'}
                      </button>
                      <button 
                        onClick={() => {
                          setDrillProblem(null);
                          if (problem) {
                            // If we bridged from a Mock problem, stay there
                            setAmcMode('MOCK');
                            if (selectedAnswer !== null) setShowExplanation(true);
                          } else {
                            // If we were in Practice Hub (Drill mode)
                            setActiveTab('settings');
                          }
                        }}
                        className="text-indigo-400 hover:text-indigo-600 transition-colors p-2 hover:bg-white rounded-full shadow-sm"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                          <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                        </svg>
                      </button>
                    </div>
                  </div>

                  {amcMetadata && (
                    <div className="mb-6 space-y-3">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="px-2.5 py-1 bg-indigo-600 text-white text-[10px] font-black rounded-lg shadow-sm uppercase tracking-wider">
                          DNA: {amcMetadata.domain}
                        </span>
                        <div className="flex flex-wrap gap-1.5">
                          {amcMetadata.dna_tags?.map((tag: string, i: number) => (
                            <span key={i} className="px-2 py-0.5 bg-white text-indigo-400 text-[9px] font-bold rounded border border-indigo-100 uppercase tracking-tighter shadow-sm">
                              #{tag}
                            </span>
                          ))}
                        </div>
                      </div>
                      
                      {amcMetadata.drill_config && (
                        <div className="p-3 bg-white/60 border border-indigo-100 rounded-2xl shadow-inner">
                          <span className="text-[9px] text-indigo-300 font-black uppercase tracking-[0.15em] block mb-1">Conceptual Mission Objective</span>
                          <p className="text-sm text-indigo-900 font-black leading-tight tracking-tight">
                            {amcMetadata.drill_config[`L${drillLevel}`] || 'Master the underlying mathematical structure.'}
                          </p>
                        </div>
                      )}
                    </div>
                  )}

                  <ProblemViewer
                    problem={drillProblem}
                    selectedAnswer={drillSelectedAnswer}
                    isCorrect={drillIsCorrect}
                    showExplanation={drillShowExplanation}
                    hintIndex={99}
                    onAnswerClick={(ans) => handleAnswerClick(ans, true)}
                    setHintIndex={() => {}}
                    setShowExplanation={setDrillShowExplanation}
                    themeColor="indigo"
                    band={drillProblem.band}
                    metadata={null} 
                  />
                  
                  <div className="mt-6 flex justify-center text-[10px] text-indigo-400 font-bold uppercase tracking-widest border-t border-indigo-100 pt-4">
                    Ready to tackle the mock again? Scroll up anytime.
                  </div>
                </div>
              )}

              <Scratchpad isActive={showScratchpad} onClose={() => setShowScratchpad(false)} />
              <GraphingCalculator isActive={showGraph} onClose={() => setShowGraph(false)} />
            </div>
          </>
        )}
        </>
        )}
      </main>

      {/* Footer */}
      <footer className="py-8 text-center text-slate-400 text-sm bg-slate-50 border-t border-slate-200">
        <p>© 2024 AI MathMate. All rights reserved.</p>
      </footer>
    </div>
  );
}
