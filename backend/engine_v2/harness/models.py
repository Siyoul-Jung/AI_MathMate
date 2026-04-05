"""Harness 데이터 클래스 — 개별 실행 결과 및 집계 리포트."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class HarnessResult:
    """단일 문제 생성 실행의 전체 메트릭."""

    # 식별
    run_id: str = ""
    timestamp: str = ""

    # 입력 파라미터
    target_daps: float = 0.0
    writer_model: str = ""
    combo_size: int = 2

    # 결과
    success: bool = False
    error: str = ""

    # 모듈 정보
    selected_modules: list[str] = field(default_factory=list)
    bridge_used: bool = False

    # 정답
    correct_answer: int | None = None
    evaluator_answer: int | None = None

    # DAPS
    daps_estimated: float | None = None
    daps_measured: float | None = None
    daps_alpha: float | None = None
    daps_beta: float | None = None
    daps_gamma: float | None = None
    daps_delta: float | None = None
    difficulty_band: str | None = None

    # 품질
    beq_verdict: str = ""
    evaluator_confidence: str = ""
    novelty_pass: bool | None = None
    novelty_structural_sim: float | None = None
    novelty_textual_sim: float | None = None
    technique_concealment: bool = True
    exposed_techniques: list[str] = field(default_factory=list)

    # 성능
    total_duration_ms: int = 0
    writer_attempts: int = 0
    evaluator_attempts: int = 0
    loop_count: int = 0

    # 지문 (선택 저장)
    narrative: str | None = None


@dataclass
class HarnessReport:
    """N문제 배치 실행의 집계 통계."""

    # 메타
    run_tag: str = ""
    total_runs: int = 0
    config: dict = field(default_factory=dict)

    # 통과율
    beq_pass_rate: float = 0.0
    novelty_pass_rate: float = 0.0
    overall_success_rate: float = 0.0

    # DAPS
    daps_measured_mean: float = 0.0
    daps_measured_std: float = 0.0
    daps_deviation_mean: float = 0.0
    delta_distribution: dict = field(default_factory=dict)
    confidence_distribution: dict = field(default_factory=dict)

    # 구조
    bridge_usage_rate: float = 0.0
    module_frequency: dict = field(default_factory=dict)

    # 품질
    technique_concealment_rate: float = 0.0

    # 비용/속도
    avg_duration_ms: float = 0.0
    avg_writer_attempts: float = 0.0
    avg_llm_calls: float = 0.0

    # 상세 데이터
    results: list[dict] = field(default_factory=list)
