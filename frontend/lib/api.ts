const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';

export interface Problem {
  p_id: string;
  narrative: string;
  answer: string | number;
  explanation?: string;
  metadata?: any;
  [key: string]: any;
}

export const api = {
  async fetchTypes(standard: string, grade: string) {
    const res = await fetch(`${API_BASE_URL}/api/types?standard=${standard}&grade=${grade}`);
    return res.json();
  },

  async fetchAnalysis(studentId: string) {
    const res = await fetch(`${API_BASE_URL}/api/analysis/${studentId}`);
    return res.json();
  },

  async fetchAdvice(studentId: string, category: string) {
    const res = await fetch(`${API_BASE_URL}/api/advice/${studentId}?category=${category}`);
    return res.json();
  },

  async fetchAmcLevels(pId: string) {
    const res = await fetch(`${API_BASE_URL}/api/amc/levels/${pId}`);
    return res.json();
  },

  async generateAmcProblem(pId: string, mode: string, level: number) {
    const res = await fetch(
      `${API_BASE_URL}/api/amc/generate?p_id=${pId}&mode=${mode}&level=${level}`
    );
    return res.json();
  },

  async generateProblem(standard: string, type: string, difficulty: string, qType: string, grade: string) {
    const res = await fetch(
      `${API_BASE_URL}/api/problem?standard=${standard}&type=${type}&difficulty=${difficulty}&q_type=${qType}&grade=${grade}`
    );
    return res.json();
  },

  async logStep(data: { student_id: string; standard_id: string; step_type: string; success_status: string }) {
    const res = await fetch(`${API_BASE_URL}/api/log`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    return res.json();
  },
  
  async fetchTextbookExamples() {
    const res = await fetch(`${API_BASE_URL}/api/textbook/examples`);
    return res.json();
  }
};
