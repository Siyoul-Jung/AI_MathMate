const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8088';

export const api = {
  async fetchTypes(standard: string, grade: string) {
    const res = await fetch(`${API_BASE_URL}/api/types?standard=${standard}&grade=${grade}`);
    return res.json();
  },

  async generateProblem(standard: string, type: string, difficulty: string, qType: string, grade: string) {
    const res = await fetch(`${API_BASE_URL}/api/problem?standard=${standard}&type=${type}&difficulty=${difficulty}&q_type=${qType}&grade=${grade}`);
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

  async logStep(logData: any) {
    const res = await fetch(`${API_BASE_URL}/api/log`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(logData)
    });
    return res.json();
  },

  // --- AIME Exclusive ---
  async fetchAmcLevels(pId: string, year: string = '2025', exam: string = 'AIME1') {
    const res = await fetch(`${API_BASE_URL}/api/amc/levels/${pId}?year=${year}&exam=${exam}`);
    return res.json();
  },

  async fetchAmcArchives() {
    const res = await fetch(`${API_BASE_URL}/api/amc/archives`);
    return res.json();
  },

  async generateAmcProblem(pId: string, mode: string = 'MOCK', level: number = 1, year: string = '2025', exam: string = 'AIME1') {
    const res = await fetch(`${API_BASE_URL}/api/amc/generate?p_id=${pId}&mode=${mode}&level=${level}&year=${year}&exam=${exam}`);
    return res.json();
  },

  async fetchTextbookExamples() {
    const res = await fetch(`${API_BASE_URL}/api/textbook/examples`);
    return res.json();
  }
};
