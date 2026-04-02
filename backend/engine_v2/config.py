"""
AI_MathMate V2 — 중앙 설정 파일
모델명, API 설정을 한 곳에서 관리합니다.
언제든 모델을 교체할 때는 이 파일만 수정하면 됩니다.
"""

# ─── LLM 모델 설정 ───────────────────────────────────────────
MODELS = {
    # 시나리오 작성 에이전트 (비용 효율 우선)
    "writer": "gpt-4o-mini",

    # 역추론 검증 에이전트 (논리 정밀도 우선, 다른 회사 모델로 편향 분리)
    "evaluator": "gemini-2.5-flash",

    # 모듈 조합 설계 에이전트 (전략적 판단)
    "architect": "gemini-2.5-flash",

    # 모듈 추출용 (대용량 PDF 분석)
    "module_extractor": "gemini-2.5-flash",
}

# 모델 업그레이드 시 여기서만 변경:
# "evaluator": "gemini-2.5-pro"  ← Pro 접근 권한 확보 후 교체

# ─── API 설정 ────────────────────────────────────────────────
GEMINI_TIMEOUT_SECONDS = 60
OPENAI_TIMEOUT_SECONDS = 30
MAX_RETRIES = 3

# ─── 생성 파이프라인 설정 ────────────────────────────────────
PIPELINE = {
    # IIPC 이중 분기: 두 결과가 이 오차 이내일 때만 통과
    "answer_tolerance": 0,        # AIME 정답은 정수이므로 오차 0

    # DAPS 점수 가중치 (α, β, γ, δ)
    # α: 계산 복잡도, β: 논리 깊이, γ: 모듈 조합 수, δ: 인지적 함정(Heuristic)
    "daps_weights": {
        "computational_complexity": 0.30,
        "logical_depth": 0.30,
        "module_combination": 0.20,
        "heuristic": 0.20,
    },

    # MASTER급 문항 최소 DAPS 기준
    "master_min_daps": 11.0,
    "master_max_daps": 15.0,

    # BEq 검증 통과 기준 (역추론 정답 일치율)
    "beq_pass_threshold": 1.0,    # 100% 일치해야 통과
}

# ─── DB 설정 ─────────────────────────────────────────────────
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB = {
    "v2_path": str(BASE_DIR / "engine_v2" / "amc_factory_v2.db"),
    "v1_legacy_path": str(BASE_DIR / "amc_factory.db")
}   # 레거시 참조용

PG_DB = {
    "dbname": os.environ.get("PG_DBNAME", "amc_factory_v2"),
    "user": os.environ.get("PG_USER", "postgres"),
    "password": os.environ.get("PG_PASSWORD", "postgres"),
    "host": os.environ.get("PG_HOST", "localhost"),
    "port": os.environ.get("PG_PORT", "5432"),
}

def get_pg_dsn() -> str:
    """PostgreSQL DSN 문자열 반환"""
    return f"dbname={PG_DB['dbname']} user={PG_DB['user']} password={PG_DB['password']} host={PG_DB['host']} port={PG_DB['port']}"

# ─── 미래 확장성 ──────────────────────────────────────────────
# 지원 exam_type 목록 (현재 구현된 것과 예정된 것 구분)
SUPPORTED_EXAM_TYPES = {
    "AIME":  {"status": "active",  "answer_format": "integer_0_999"},
    "AMC":   {"status": "planned", "answer_format": "multiple_choice_5"},
    "수능":  {"status": "planned", "answer_format": "integer_0_999"},
    "USAMO": {"status": "future",  "answer_format": "proof"},
}

SUPPORTED_LANGUAGES = ["en", "ko"]
