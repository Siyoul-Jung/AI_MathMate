"""
AI_MathMate V2 — PostgreSQL DB 스키마 정의
V2의 모든 테이블(pgvector 포함)을 정의하고 생성합니다.
"""

import os
import psycopg2
from typing import Dict

# ─── DDL 정의 ───────────────────────────────────────────────────────────────

SCHEMA_PG = """
-- ═══════════════════════════════════════════════════════════
-- pgvector 확장 설정
-- ═══════════════════════════════════════════════════════════
CREATE EXTENSION IF NOT EXISTS vector;

-- ═══════════════════════════════════════════════════════════
-- 원자 모듈 테이블
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS modules (
    module_id           TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    category            TEXT NOT NULL,      
    domain              TEXT NOT NULL,      
    namespace           TEXT NOT NULL UNIQUE,
    logic_depth         INTEGER NOT NULL,
    daps_contribution   REAL NOT NULL,
    min_difficulty      INTEGER NOT NULL,
    exam_types          JSONB NOT NULL,      
    languages           JSONB DEFAULT '["en"]'::jsonb,
    curriculum_standard TEXT DEFAULT 'AIME',
    tags                JSONB DEFAULT '[]'::jsonb,
    source_reference    TEXT DEFAULT '',    
    registered_at       TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- 모듈 간 호환성 매트릭스
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS module_compatibility (
    module_a_id         TEXT NOT NULL,
    module_b_id         TEXT NOT NULL,
    status              TEXT NOT NULL,      
    conflict_reason     TEXT DEFAULT '',
    tested_at           TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (module_a_id, module_b_id),
    FOREIGN KEY (module_a_id) REFERENCES modules(module_id),
    FOREIGN KEY (module_b_id) REFERENCES modules(module_id)
);

-- ═══════════════════════════════════════════════════════════
-- Architect 에이전트의 설계 의도 (Blueprint)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS blueprints (
    blueprint_id        TEXT PRIMARY KEY,
    target_daps         REAL NOT NULL,
    difficulty_band     TEXT NOT NULL,      
    exam_type           TEXT DEFAULT 'AIME',
    language            TEXT DEFAULT 'en',
    curriculum_standard TEXT DEFAULT 'AIME',
    architect_model     TEXT NOT NULL,      
    architect_reasoning TEXT DEFAULT '',    
    status              TEXT DEFAULT 'PENDING',  
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- Blueprint에 포함된 모듈 조합 내역
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS blueprint_modules (
    blueprint_id        TEXT NOT NULL,
    module_id           TEXT NOT NULL,
    combination_order   INTEGER NOT NULL,   
    PRIMARY KEY (blueprint_id, module_id),
    FOREIGN KEY (blueprint_id) REFERENCES blueprints(blueprint_id),
    FOREIGN KEY (module_id) REFERENCES modules(module_id)
);

-- ═══════════════════════════════════════════════════════════
-- 생성된 변체 문항
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS variants (
    id                  SERIAL PRIMARY KEY,
    blueprint_id        TEXT,               
    mode                TEXT NOT NULL,      
    difficulty_band     TEXT DEFAULT '',    
    problem_position    INTEGER DEFAULT 0,  
    narrative           TEXT NOT NULL,
    variables_json      JSONB NOT NULL,
    solution_json       JSONB NOT NULL,
    correct_answer      INTEGER NOT NULL,
    theme_name          TEXT DEFAULT '',
    image_url           TEXT DEFAULT '',
    seed_key            TEXT DEFAULT '',
    status              TEXT DEFAULT 'PENDING',  
    exam_type           TEXT DEFAULT 'AIME',
    language            TEXT DEFAULT 'en',
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (blueprint_id) REFERENCES blueprints(blueprint_id)
);

-- ═══════════════════════════════════════════════════════════
-- MAS 에이전트 대화 전체 기록 (학습 데이터 원천)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS mas_logs (
    id                  SERIAL PRIMARY KEY,
    variant_id          INTEGER,
    blueprint_id        TEXT,
    agent_role          TEXT NOT NULL,      
    agent_model         TEXT NOT NULL,      
    input_sent          TEXT NOT NULL,
    output_received     TEXT NOT NULL,
    verdict             TEXT DEFAULT '',    
    fix_instruction     TEXT DEFAULT '',    
    attempt_number      INTEGER DEFAULT 1,
    duration_ms         INTEGER DEFAULT 0,
    created_at          TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variant_id) REFERENCES variants(id)
);

-- ═══════════════════════════════════════════════════════════
-- DAPS 점수 세부 내역
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS daps_scores (
    variant_id              INTEGER PRIMARY KEY,
    computational_complexity REAL DEFAULT 0.0,
    logical_depth           REAL DEFAULT 0.0,
    module_combination_score REAL DEFAULT 0.0,
    narrative_complexity    REAL DEFAULT 0.0,
    heuristic_score         REAL DEFAULT 0.0,   
    final_daps              REAL DEFAULT 0.0,
    scored_at               TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variant_id) REFERENCES variants(id)
);

-- ═══════════════════════════════════════════════════════════
-- IRT 캘리브레이션 데이터
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS irt_calibration (
    id                      SERIAL PRIMARY KEY,
    module_id               TEXT,
    exam_type               TEXT DEFAULT 'AIME',
    compendium_year         INTEGER,
    compendium_position     INTEGER,        
    real_difficulty_label   REAL,           
    predicted_daps          REAL,
    error                   REAL,           
    calibrated_at           TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- Vector DB: 참신성(Novelty) 및 중복 검사를 위한 임베딩 데이터
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS variant_embeddings (
    variant_id      INTEGER PRIMARY KEY,
    seed_hash       TEXT NOT NULL UNIQUE,     
    narrative_vec   vector(1536),             -- OpenAI text-embedding-3-small 등
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variant_id) REFERENCES variants(id)
);
"""

INDEXES_PG = """
CREATE INDEX IF NOT EXISTS idx_variants_blueprint on variants(blueprint_id);
CREATE INDEX IF NOT EXISTS idx_variants_status on variants(status);
CREATE INDEX IF NOT EXISTS idx_mas_logs_variant on mas_logs(variant_id);
CREATE INDEX IF NOT EXISTS idx_compat_a on module_compatibility(module_a_id);
CREATE INDEX IF NOT EXISTS idx_daps_variant on daps_scores(variant_id);
CREATE INDEX IF NOT EXISTS idx_variant_embeddings_vec ON variant_embeddings USING hnsw (narrative_vec vector_l2_ops);
"""

# ─── 스키마 생성 함수 ────────────────────────────────────────────────────────

def create_pg_schema(dsn: str) -> bool:
    """
    PostgreSQL 시스템에 V2 DB 스키마를 생성합니다.
    """
    try:
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_PG)
                cur.execute(INDEXES_PG)
            conn.commit()
        print(f"✅ V2 PostgreSQL 스키마 생성 완료")
        return True
    except Exception as e:
        print(f"❌ PostgreSQL 스키마 생성 실패: {e}")
        return False


def verify_pg_schema(dsn: str) -> Dict[str, bool]:
    """
    V2 DB의 모든 테이블이 존재하는지 확인합니다.
    """
    expected_tables = [
        "modules", "module_compatibility", "blueprints",
        "blueprint_modules", "variants", "mas_logs",
        "daps_scores", "irt_calibration", "variant_embeddings"
    ]
    results = {}
    
    try:
        with psycopg2.connect(dsn) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
                existing = {row[0] for row in cur.fetchall()}
                for table in expected_tables:
                    results[table] = table in existing
        return results
    except Exception as e:
        print(f"❌ 검증 연결 실패: {e}")
        return {t: False for t in expected_tables}

if __name__ == "__main__":
    from engine_v2.config import get_pg_dsn
    dsn = get_pg_dsn()
    print("🐘 V2 PostgreSQL 스키마 생성 중...")
    if create_pg_schema(dsn):
        print("\\n테이블 검증 (PostgreSQL):")
        results = verify_pg_schema(dsn)
        for table, exists in results.items():
            icon = "✅" if exists else "❌"
            print(f"  {icon} {table}")
