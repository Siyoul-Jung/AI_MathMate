from fastapi import APIRouter, HTTPException
from typing import List, Optional
import os
import json
import traceback
from app.schemas.problem import LogItem
from kmath_engine.amc_master import AMCSolverMaster

router = APIRouter()
amc_master = AMCSolverMaster()

@router.get("/types")
def get_types(standard: str, grade: str):
    """
    Returns available problem types for a given standard and grade.
    """
    if standard == "AIME":
        return {"types": ["Mock Exam", "Drill Mode"]}
    # Default for standard practice
    return {"types": ["Multiple Choice", "Short Answer"]}

@router.get("/problem")
def get_standard_problem(standard: str, type: str, difficulty: str, q_type: str, grade: str):
    """
    Placeholder for standard non-AIME problem generation.
    """
    return {
        "p_id": "STD-001",
        "question": f"This is a placeholder {difficulty} {type} question for {standard} {grade}.",
        "answer": "42",
        "explanation": "The answer is always 42."
    }

@router.get("/textbook/examples")
def get_textbook_examples():
    try:
        # backend 폴더 내부의 textbook_examples.json 읽기
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        file_path = os.path.join(current_dir, 'textbook_examples.json')
        if not os.path.exists(file_path):
             return {"error": f"File not found at {file_path}"}
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        return {"error": str(e)}

@router.get("/analysis/{student_id}")
def get_analysis(student_id: str):
    return {
        "weak_points": ["std_001", "std_002"], 
        "proficiency": {
            "std_001": 40,
            "std_002": 75,
            "std_003": 90
        }
    }

@router.get("/advice/{student_id}")
def get_advice(student_id: str, category: str):
    return {"advice": "기본 계산 실수가 조금 있습니다. 침착하게 문제를 풀어보세요!"}

@router.get("/amc/problems")
def get_amc_problems():
    problems = [f"P{i:02d}" for i in range(1, 16)]
    return {"problems": problems}

@router.get("/amc/levels/{p_id}")
def get_amc_levels(p_id: str):
    info = amc_master.get_supported_levels(p_id, year="2025", exam="AIME1")
    return info

@router.get("/amc/generate")
def generate_amc_problem(p_id: str, mode: str = "MOCK", level: int = 3):
    try:
        problem = amc_master.generate(
            p_id=p_id, 
            mode=mode, 
            level=level,
            year="2025",
            exam="AIME1"
        )
        return problem
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}

@router.post("/log")
def log_step(item: LogItem):
    return {"status": "ok"}
