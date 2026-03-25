from fastapi import APIRouter, HTTPException
from typing import List, Optional
import os
import json
import re
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

@router.get("/amc/archives")
def get_amc_archives():
    """
    Scans all years and exams to build a domain-based archive of all AIME missions.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
    exams_root = os.path.join(base_dir, 'amc_engine', 'exams')
    archives = {}
    
    if not os.path.exists(exams_root):
        return {"archives": {}}
        
    for year in os.listdir(exams_root):
        year_path = os.path.join(exams_root, year)
        if not os.path.isdir(year_path): continue
        for exam in os.listdir(year_path):
            exam_path = os.path.join(year_path, exam)
            if not os.path.isdir(exam_path): continue
            
            for band in ["CHALLENGER", "EXPERT", "MASTER"]:
                band_path = os.path.join(exam_path, band)
                if not os.path.exists(band_path): continue
                
                for p_id in os.listdir(band_path):
                    p_path = os.path.join(band_path, p_id)
                    meta_path = os.path.join(p_path, 'metadata.json')
                    if os.path.exists(meta_path):
                        with open(meta_path, 'r', encoding='utf-8') as f:
                            meta = json.load(f)
                            domain_raw = meta.get('domain', 'Other')
                            # Split hybrid domains (e.g., "Algebra / Number Theory")
                            domains = [d.strip() for d in re.split(r'[/,]', domain_raw)]
                            
                             # Normalize DNA tags (handle both 'tags' and 'dna_tags')
                            dna_tags = meta.get('dna_tags', meta.get('tags', []))
                            title = meta.get('title') or f"Mission {p_id}"
                            
                            for domain in domains:
                                if domain not in archives: archives[domain] = []
                                # Add year/exam context to the mission (will be hidden in UI but kept in data)
                                archives[domain].append({
                                    **meta,
                                    'p_id': p_id,
                                    'title': title,
                                    'dna_tags': dna_tags,
                                    'year': year,
                                    'exam': exam
                                })
                            
    return {"archives": archives}

@router.get("/amc/problems")
def get_amc_problems():
    problems = [f"P{i:02d}" for i in range(1, 16)]
    return {"problems": problems}

@router.get("/amc/levels/{p_id}")
def get_amc_levels(p_id: str, year: str = "2025", exam: str = "AIME1"):
    info = amc_master.get_supported_levels(p_id, year=year, exam=exam)
    return info

@router.get("/amc/generate")
def generate_amc_problem(p_id: str, mode: str = "MOCK", level: Optional[int] = None, year: str = "2025", exam: str = "AIME1"):
    effective_level = level if level is not None else 3
    try:
        problem = amc_master.generate(
            p_id=p_id, 
            mode=mode, 
            level=effective_level,
            year=year,
            exam=exam
        )
        return problem
    except Exception as e:
        return {"error": str(e), "trace": traceback.format_exc()}

@router.post("/log")
def log_step(item: LogItem):
    return {"status": "ok"}
