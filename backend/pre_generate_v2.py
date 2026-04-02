import sqlite3
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from engine_v2.pipeline_v2 import EngineV2Pipeline
from engine_v2.config import DB

# ─── 동적 모듈 자동 등록 로직 ──────────────────────────────────────────────────
def auto_register_v2_modules(pipeline: EngineV2Pipeline):
    """
    engine_v2/modules 디렉토리 내의 모든 원자적 모듈을 찾아 파이프라인에 등록합니다.
    """
    import inspect
    import pkgutil
    import engine_v2.modules as modules_pkg
    from engine_v2.modules.base_module import AtomicModule

    print("🔍 모듈 자동 검색 및 등록 시작...")
    package_path = os.path.dirname(modules_pkg.__file__)
    
    count = 0
    for loader, module_name, is_pkg in pkgutil.walk_packages([package_path], modules_pkg.__name__ + "."):
        try:
            module = loader.find_module(module_name).load_module(module_name)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, AtomicModule) and obj is not AtomicModule:
                    pipeline.registry.register(obj())
                    count += 1
        except Exception as e:
            print(f"  ⚠️ 모듈 로드 실패 ({module_name}): {e}")
            
    print(f"✅ 총 {count}개의 모듈이 성공적으로 등록되었습니다.\n")

# ─── 배치 생성 메인 로직 ────────────────────────────────────────────────────────
def pre_generate_batch(count: int, difficulty: str = "MASTER"):
    pipeline = EngineV2Pipeline()
    auto_register_v2_modules(pipeline)
    
    db_path = Path(DB["v2_path"])
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 테이블 구조 보장 (만약 없을 경우)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blueprint_id TEXT,
            mode TEXT,
            difficulty_band TEXT,
            narrative TEXT,
            variables_json TEXT,
            solution_json TEXT,
            correct_answer TEXT,
            status TEXT,
            exam_type TEXT,
            language TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    print(f"🚀 Batch Generation 시작: {count}개 문항 (난이도: {difficulty})")
    
    success_count = 0
    for i in range(count):
        print(f"\n[{i+1}/{count}] 문항 합성 중...")
        try:
            result = pipeline.generate_problem(
                difficulty_band=difficulty,
                target_daps=13.5 if difficulty == "MASTER" else 9.0
            )
            
            if result.get("success", True):
                # SQLite 저장
                cursor.execute("""
                    INSERT INTO variants 
                    (blueprint_id, mode, difficulty_band, narrative, variables_json, 
                     solution_json, correct_answer, status, exam_type, language)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(uuid.uuid4()), "MOCK", difficulty,
                    result["narrative"],
                    json.dumps(result.get("metadata", {}), ensure_ascii=False),
                    json.dumps(result.get("solution_steps", []), ensure_ascii=False),
                    result["answer"],
                    "VERIFIED", "AIME", "en"
                ))
                conn.commit()
                success_count += 1
                print(f"✨ 저장 완료 (SQLite ID: {cursor.lastrowid})")
            else:
                print(f"❌ 합성 실패: {result.get('error')}")
                
        except Exception as e:
            print(f"💥 치명적 오류 발생: {e}")

    conn.close()
    print(f"\n🏁 작업 종료: {success_count}/{count}개 문항 생성 및 저장 완료.")

if __name__ == "__main__":
    import sys
    batch_count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    pre_generate_batch(batch_count)
