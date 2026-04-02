"""
AI_MathMate V2 — Heritage 90 Synthesis API
역할: 전 세계 최상위권 수학 영재들을 위한 지능형 문항 합성 엔드포인트 구축
"""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional, Any
import uuid
import json
import os
import psycopg2
import sqlite3
from pathlib import Path
from pydantic import BaseModel

from engine_v2.pipeline_v2 import EngineV2Pipeline
from engine_v2.config import get_pg_dsn, DB
from app.schemas.problem import LogItem 

router = APIRouter()
_pipeline_instance: Optional[EngineV2Pipeline] = None

class SynthesisRequest(BaseModel):
    mode: str = "MASTER" # CHALLENGER, EXPERT, MASTER
    target_daps: float = 14.5
    theme_hint: str = "Extremal Principle"
    max_loop: int = 3

def auto_register_v2_modules(pipeline: EngineV2Pipeline):
    """지연 로딩 시점에 모든 원자적 모듈을 자동으로 검색하고 등록합니다."""
    import inspect
    import pkgutil
    import engine_v2.modules as modules_pkg
    from engine_v2.modules.base_module import AtomicModule

    package_path = os.path.dirname(modules_pkg.__file__)
    count = 0
    for loader, module_name, is_pkg in pkgutil.walk_packages([package_path], modules_pkg.__name__ + "."):
        try:
            module = loader.find_module(module_name).load_module(module_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, AtomicModule) and obj is not AtomicModule:
                    pipeline.registry.register(obj())
                    count += 1
        except Exception:
            pass
    print(f"✅ [Synthesis API] {count} modules registered via auto-discovery.")

def get_v2_pipeline() -> EngineV2Pipeline:
    """Lazy loader for EngineV2Pipeline."""
    global _pipeline_instance
    if _pipeline_instance is None:
        try:
            _pipeline_instance = EngineV2Pipeline()
            auto_register_v2_modules(_pipeline_instance)
        except Exception as e:
            import traceback
            print(f"FAILED TO INITIALIZE V2 PIPELINE: {traceback.format_exc()}")
            raise e
    return _pipeline_instance

def fetch_cached_variant(difficulty_band: str):
    """
    DB에서 검증된 문항을 우선 조회 (Postgres -> SQLite)
    """
    # 1. PostgreSQL 시도
    try:
        dsn = get_pg_dsn()
        with psycopg2.connect(dsn) as conn:
            import psycopg2.extras
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("""
                    SELECT * FROM variants 
                    WHERE difficulty_band = %s AND status = 'VERIFIED'
                    ORDER BY RANDOM() LIMIT 1
                """, (difficulty_band,))
                row = cursor.fetchone()
                if row: return dict(row)
    except Exception:
        pass

    # 2. SQLite 시도
    try:
        db_path = Path(DB["v2_path"])
        if db_path.exists():
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM variants 
                WHERE difficulty_band = ? AND status = 'VERIFIED'
                ORDER BY RANDOM() LIMIT 1
            """, (difficulty_band,))
            row = cursor.fetchone()
            conn.close()
            if row: return dict(row)
    except Exception:
        pass
    
    return None

@router.post("/generate")
async def generate_aime_problem(request: SynthesisRequest):
    """
    Heritage 90 엔진 문항 서빙 (DB 우선 -> 실시간Fallback)
    """
    print(f"🎯 [Synthesis Request] Mode: {request.mode}")
    
    # [1] DB 조회 (Cache-First)
    cached = fetch_cached_variant(request.mode)
    if cached:
        print(f"✨ [DB_HIT] Returning variant: {cached.get('id')}")
        return {
            "success": True,
            "id": cached.get("id", str(uuid.uuid4())),
            "narrative": cached.get("narrative") or cached.get("problem_text"),
            "question": cached.get("narrative") or cached.get("problem_text"), # Correct mapping for Frontend
            "problem": cached.get("narrative") or cached.get("problem_text"),  # Fallback
            "answer": cached.get("correct_answer"),
            "options": [],
            "metadata": json.loads(cached.get("variables_json", "{}")),
            "solution_steps": json.loads(cached.get("solution_json", "[]")),
            "logic_steps": json.loads(cached.get("solution_json", "[]")),
            "explanation": json.loads(cached.get("solution_json", "[]")),
            "band": cached.get("difficulty_band", "MASTER") # Use difficulty_band column
        }

    # [2] 실시간 합성 (Fallback)
    print(f"🔥 [DB_MISS] Initiating real-time synthesis for {request.mode}")
    pipeline = get_v2_pipeline()
    try:
        difficulty_map = {"CHALLENGER": 9.0, "EXPERT": 11.5, "MASTER": 13.5}
        target_daps = difficulty_map.get(request.mode, 13.0)
        
        result = pipeline.generate_problem(
            difficulty_band=request.mode,
            target_daps=target_daps,
            exam_type="AIME"
        )
        
        if not result.get("success", True):
             raise HTTPException(status_code=500, detail=result.get("error", "Unknown error"))

        return {
            "success": True,
            "id": result.get("id", str(uuid.uuid4())),
            "narrative": result["narrative"],
            "question": result["narrative"],   # Added for Frontend
            "problem": result["narrative"],    # Fallback
            "answer": result["answer"],
            "options": [], 
            "metadata": result.get("metadata", {}),
            "solution_steps": result.get("solution_steps", []),
            "logic_steps": result.get("solution_steps", []),
            "explanation": result.get("solution_steps", []),
            "band": result.get("difficulty_band", request.mode)
        }
    except Exception as e:
        import traceback
        print(f"Synthesis System Error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
def get_synthesis_stats():
    return {"engine": "Heritage 90 (RC1)", "status": "operational", "mode": "DB-First"}
