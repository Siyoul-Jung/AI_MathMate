from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any, Optional
from manager import ProblemManager
from core.llm_service import LLMService
from core.analytics_service import AnalyticsService
import uvicorn
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

# .env 파일 절대 경로로 로드 (실행 위치와 무관하게 로드)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"[Server] .env file loaded from: {env_path}")
else:
    print(f"[Server] ⚠️ .env file NOT found at: {env_path}")

app = FastAPI()

# Next.js 개발 서버(localhost:3000)에서의 요청 허용 (CORS 설정)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 문제 관리자 인스턴스 생성 (서버 시작 시 1회 로딩)
manager = ProblemManager()

# LLM 서비스 인스턴스 생성
llm_service = LLMService()

# 분석 서비스 인스턴스 생성
analytics_service = AnalyticsService()

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MathMate API Server is running"}

@app.get("/api/types")
def get_supported_types(curriculum: str = "KR", grade: str = "Middle_1-1", standard: str = "STD-11-01"):
    """특정 성취기준의 지원되는 문제 유형 목록 반환"""
    types = manager.list_supported_types(curriculum, grade, standard)
    return {"types": types}

@app.get("/api/problem")
def generate_problem(
    curriculum: str = "KR", 
    grade: str = "Middle_1-1", 
    standard: str = "STD-11-01", 
    type: str = "T01", 
    difficulty: str = "Normal",
    q_type: str = "short_answer"
):
    """문제 생성 엔드포인트"""
    # manager를 통해 문제 생성
    result = manager.get_problem(curriculum, grade, standard, type, difficulty, q_type)
    
    # 에러 처리
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
        
    return result

class DiagnoseRequest(BaseModel):
    question: str
    logic_steps: List[Any]
    student_input: str
    answer: str

@app.post("/api/diagnose")
def diagnose(req: DiagnoseRequest):
    """학생 답안 진단 엔드포인트"""
    result = llm_service.diagnose_student_answer(
        req.question, 
        req.logic_steps, 
        req.student_input, 
        req.answer
    )
    return result

class LogRequest(BaseModel):
    student_id: str
    standard_id: str
    step_type: str     # CONCEPT, CALC, STRATEGY
    success_status: str # SELF, HINTED, FAIL

@app.post("/api/log")
def log_student_step(req: LogRequest):
    """학생 학습 이력 저장"""
    analytics_service.log_step(req.student_id, req.standard_id, req.step_type, req.success_status)
    return {"status": "success"}

@app.get("/api/analysis/{student_id}")
def get_student_analysis(student_id: str):
    """학생 성취도 분석 결과 반환"""
    proficiency = analytics_service.analyze_proficiency(student_id)
    weak_points = analytics_service.get_weak_points(student_id)
    
    # 최근 학습 추이 모의 데이터 생성 (최근 7일)
    recent_trend = []
    today = datetime.now()
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        solved = random.randint(5, 30)
        correct = random.randint(int(solved * 0.4), solved)
        rate = int((correct / solved) * 100) if solved > 0 else 0
        recent_trend.append({
            "date": d.strftime("%m/%d"),
            "solved": solved,
            "correct_rate": rate
        })

    return {
        "proficiency": proficiency,
        "weak_points": weak_points,
        "recent_trend": recent_trend
    }

@app.get("/api/advice/{student_id}")
def get_student_advice(student_id: str, category: str = None):
    """학생 맞춤형 학습 조언 반환"""
    proficiency = analytics_service.analyze_proficiency(student_id)
    weak_points = analytics_service.get_weak_points(student_id)
    
    if category:
        target_standards = set(manager.get_standards_by_category(category))
        # 필터링: 해당 카테고리에 속한 성취기준만 남김
        proficiency = {k: v for k, v in proficiency.items() if k in target_standards}
        weak_points = [wp for wp in weak_points if wp in target_standards]
    
    advice = llm_service.generate_learning_advice(proficiency, weak_points)
    return {"advice": advice}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)