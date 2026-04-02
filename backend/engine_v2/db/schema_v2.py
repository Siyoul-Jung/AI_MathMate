"""
AI_MathMate V2 — DB 스키마 정의
V2의 모든 테이블을 정의하고 생성합니다.
"""

import sqlite3
from pathlib import Path

# ─── DDL 정의 ───────────────────────────────────────────────────────────────

SCHEMA_V2 = """
-- ═══════════════════════════════════════════════════════════
-- 원자 모듈 테이블 (V1의 engines 테이블 완전 교체)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS modules (
    module_id           TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    category            TEXT NOT NULL,      -- 'algebra'|'geometry'|'nt'|'combo'
    domain              TEXT NOT NULL,      -- 'integer'|'real'|'complex'
    namespace           TEXT NOT NULL UNIQUE,
    logic_depth         INTEGER NOT NULL,
    daps_contribution   REAL NOT NULL,
    min_difficulty      INTEGER NOT NULL,
    exam_types          TEXT NOT NULL,      -- JSON: ["AIME", "AMC"]
    languages           TEXT DEFAULT '["en"]',
    curriculum_standard TEXT DEFAULT 'AIME',
    tags                TEXT DEFAULT '[]',
    source_reference    TEXT DEFAULT '',    -- 어떤 기출에서 추출됐는지
    registered_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- 모듈 간 호환성 매트릭스
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS module_compatibility (
    module_a_id         TEXT NOT NULL,
    module_b_id         TEXT NOT NULL,
    status              TEXT NOT NULL,      -- 'COMPATIBLE'|'INCOMPATIBLE'
    conflict_reason     TEXT DEFAULT '',
    tested_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    difficulty_band     TEXT NOT NULL,      -- 'MASTER'|'EXPERT'|'CHALLENGER'
    exam_type           TEXT DEFAULT 'AIME',
    language            TEXT DEFAULT 'en',
    curriculum_standard TEXT DEFAULT 'AIME',
    architect_model     TEXT NOT NULL,      -- 사용된 LLM 모델명
    architect_reasoning TEXT DEFAULT '',    -- Architect의 선택 근거
    status              TEXT DEFAULT 'PENDING',  -- 'PENDING'|'GENERATING'|'DONE'|'FAILED'
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- Blueprint에 포함된 모듈 조합 내역
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS blueprint_modules (
    blueprint_id        TEXT NOT NULL,
    module_id           TEXT NOT NULL,
    combination_order   INTEGER NOT NULL,   -- 조합 순서
    PRIMARY KEY (blueprint_id, module_id),
    FOREIGN KEY (blueprint_id) REFERENCES blueprints(blueprint_id),
    FOREIGN KEY (module_id) REFERENCES modules(module_id)
);

-- ═══════════════════════════════════════════════════════════
-- 생성된 변체 문항 (V1의 variants 테이블 확장)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS variants (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    blueprint_id        TEXT,               -- NULL이면 V1 레거시 문항
    mode                TEXT NOT NULL,      -- 'MOCK'|'DRILL'
    difficulty_band     TEXT DEFAULT '',    -- 'MASTER'|'EXPERT' 등
    problem_position    INTEGER DEFAULT 0,  -- P01=1 ~ P15=15
    narrative           TEXT NOT NULL,
    variables_json      TEXT NOT NULL,
    solution_json       TEXT NOT NULL,
    correct_answer      INTEGER NOT NULL,
    theme_name          TEXT DEFAULT '',
    image_url           TEXT DEFAULT '',
    seed_key            TEXT DEFAULT '',
    status              TEXT DEFAULT 'PENDING',  -- 'PENDING'|'VERIFIED'|'REJECTED'
    exam_type           TEXT DEFAULT 'AIME',
    language            TEXT DEFAULT 'en',
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (blueprint_id) REFERENCES blueprints(blueprint_id)
);

-- ═══════════════════════════════════════════════════════════
-- MAS 에이전트 대화 전체 기록 (학습 데이터 원천)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS mas_logs (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    variant_id          INTEGER,
    blueprint_id        TEXT,
    agent_role          TEXT NOT NULL,      -- 'WRITER'|'EVALUATOR'|'JUDGE'|'ARCHITECT'
    agent_model         TEXT NOT NULL,      -- 실제 사용된 모델명
    input_sent          TEXT NOT NULL,
    output_received     TEXT NOT NULL,
    verdict             TEXT DEFAULT '',    -- 'PASS'|'FAIL'|'FIX_REQUIRED'
    fix_instruction     TEXT DEFAULT '',    -- Judge의 수정 지시 내용
    attempt_number      INTEGER DEFAULT 1,
    duration_ms         INTEGER DEFAULT 0,
    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
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
    heuristic_score         REAL DEFAULT 0.0,   -- 인지적 함정/트릭 (δ)
    final_daps              REAL DEFAULT 0.0,
    scored_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variant_id) REFERENCES variants(id)
);

-- ═══════════════════════════════════════════════════════════
-- IRT 캘리브레이션 데이터
-- (Compendium 1,000문항으로 DAPS 가중치 보정)
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS irt_calibration (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id               TEXT,
    exam_type               TEXT DEFAULT 'AIME',
    compendium_year         INTEGER,
    compendium_position     INTEGER,        -- 문제 번호 (1~15)
    real_difficulty_label   REAL,           -- Ground Truth (P01=1.0, P15=15.0)
    predicted_daps          REAL,
    error                   REAL,           -- |real - predicted|
    calibrated_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ═══════════════════════════════════════════════════════════
-- Vector DB: 참신성(Novelty) 및 중복 검사를 위한 임베딩 데이터
-- ═══════════════════════════════════════════════════════════
CREATE TABLE IF NOT EXISTS variant_embeddings (
    variant_id      INTEGER PRIMARY KEY,
    seed_hash       TEXT NOT NULL UNIQUE,     -- Seed 클론 차단
    narrative_vec   BLOB,                     -- 지문 임베딩 (L2 거리 계산용)
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (variant_id) REFERENCES variants(id)
);
"""

INDEXES_V2 = """
CREATE INDEX IF NOT EXISTS idx_variants_blueprint ON variants(blueprint_id);
CREATE INDEX IF NOT EXISTS idx_variants_status ON variants(status);
CREATE INDEX IF NOT EXISTS idx_mas_logs_variant ON mas_logs(variant_id);
CREATE INDEX IF NOT EXISTS idx_compat_a ON module_compatibility(module_a_id);
CREATE INDEX IF NOT EXISTS idx_daps_variant ON daps_scores(variant_id);
"""


# ─── 스키마 생성 함수 ────────────────────────────────────────────────────────

def create_v2_schema(db_path: str) -> bool:
    """
    V2 DB 스키마를 생성합니다.
    :param db_path: SQLite DB 파일 경로
    :return: 성공 여부
    """
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect(path) as conn:
            conn.executescript(SCHEMA_V2)
            conn.executescript(INDEXES_V2)
            conn.commit()
        print(f"✅ V2 DB 스키마 생성 완료: {path}")
        return True
    except Exception as e:
        print(f"❌ DB 스키마 생성 실패: {e}")
        return False


def verify_v2_schema(db_path: str) -> dict:
    """
    V2 DB의 모든 테이블이 존재하는지 확인합니다.
    :return: 테이블별 존재 여부
    """
    expected_tables = [
        "modules", "module_compatibility", "blueprints",
        "blueprint_modules", "variants", "mas_logs",
        "daps_scores", "irt_calibration", "variant_embeddings"
    ]
    results = {}
    with sqlite3.connect(db_path) as conn:
        existing = {
            row[0] for row in
            conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        for table in expected_tables:
            results[table] = table in existing
    return results


if __name__ == "__main__":
    from engine_v2.config import DB
    print("V2 DB 스키마 생성 중...")
    create_v2_schema(DB["v2_path"])

    print("\n테이블 검증:")
    results = verify_v2_schema(DB["v2_path"])
    for table, exists in results.items():
        icon = "✅" if exists else "❌"
        print(f"  {icon} {table}")
