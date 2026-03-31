from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import hashlib
import random


# ─── 타입 정의 ──────────────────────────────────────────────────────────────

@dataclass
class FieldSpec:
    """모듈의 입/출력 변수 하나의 스펙을 정의합니다."""
    dtype: type                          # int, float, str
    domain: str                          # "Z+" (양의 정수), "Z" (정수), "R" (실수)
    min_val: Any = None
    max_val: Any = None
    constraint: str = ""                 # 자유 텍스트 제약 조건 설명
    description: str = ""

@dataclass
class ModuleMeta:
    """모듈의 핵심 메타데이터 — 타입 계약의 핵심입니다."""
    module_id: str                         # 고유 식별자 (예: "nt_power_congruence")
    name: str                              # 한국어 이름 (예: "거듭제곱 합동식")
    domain: str                            # "integer" | "real" | "complex"
    namespace: str                         # 고유 변수 prefix (예: "nt_power")
    input_schema: dict[str, FieldSpec]
    output_schema: dict[str, FieldSpec]
    logic_depth: int                       # 이 모듈 단독의 논리 단계 수
    daps_contribution: float               # 이 모듈이 기여하는 DAPS 점수
    min_difficulty: int                    # 적합한 최소 문제 번호 (P01 = 1)
    heuristic_weight: float = 0.0          # δ(Heuristic/Trap) 변수 (기본 0.0)
    
    # Heritage 90 V2 확장 필드
    v2_compatible: bool = True
    v2_strategy_tags: list[str] = field(default_factory=list)  # ["conceal", "asymmetry", "anonymize"]
    logic_leap_points: list[str] = field(default_factory=list) # "도약"이 필요한 지점들 설명
    
    exam_types: list[str] = field(default_factory=lambda: ["AIME"])
    languages: list[str] = field(default_factory=lambda: ["en"])
    curriculum_standard: str = "AIME"
    category: str = ""                     # "algebra" | "geometry" | "nt" | "combo"
    tags: list[str] = field(default_factory=list)
    source_reference: str = ""             # 어떤 기출에서 추출됐는지


# ─── 전략 믹스인 (StrategyMixin) ─────────────────────────────────────────────

class StrategyMixin:
    """
    AIME V2 'Heritage 90'의 전략적 기능을 제공하는 믹스인.
    모든 AtomicModule이 이 기능을 사용하여 지능적인 문제 변형을 수행합니다.
    """

    def apply_asymmetry(self, seed: dict[str, Any], strength: float = 1.0) -> dict[str, Any]:
        """
        [Symmetry Breaker]
        시드 값에 비대칭성을 주입합니다. (예: 10 -> 13, 100 -> 101)
        :param strength: 비대칭 강도 (소수 주입 빈도 등)
        """
        primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        new_seed = seed.copy()
        for k, v in new_seed.items():
            if isinstance(v, int) and v > 5 and strength > 0.5:
                # 둥근 숫자를 소수나 비대칭 수로 교체
                if v % 10 == 0 or v % 5 == 0:
                    offset = random.choice([-1, 1, 2, -2])
                    new_seed[k] = v + offset
        return new_seed

    def apply_concealment(self, logic_steps: list[str]) -> list[str]:
        """
        [Logic Concealer]
        논리적 단계를 재구성하여 중간 '흔적'을 지웁니다.
        :param logic_steps: 원래의 논리 단계들
        """
        if len(logic_steps) < 2:
            return logic_steps
        
        # 중간 단계를 결합하거나 추상화하여 도약을 강제
        concealed = []
        for i, step in enumerate(logic_steps):
            if i % 2 == 0 and i + 1 < len(logic_steps):
                concealed.append(f"복합 추론 단계: {step}와 {logic_steps[i+1]}의 관계를 통합 분석합니다.")
            elif i % 2 == 0:
                concealed.append(step)
        return concealed

    def anonymize_variables(self, seed: dict[str, Any]) -> dict[str, Any]:
        """
        [Anonymization]
        변수명을 표준형(a, b, c)에서 익명형(X_1, Y_k)으로 변환합니다.
        """
        return {f"VAR_{hashlib.md5(k.encode()).hexdigest()[:4]}": v for k, v in seed.items()}


# ─── AtomicModule 베이스 클래스 ─────────────────────────────────────────────

class AtomicModule(ABC, StrategyMixin):
    """
    모든 원자 모듈의 기반 클래스.
    하위 클래스는 META, generate_seed(), execute(), get_logic_steps()를 구현해야 합니다.
    """

    # 하위 클래스에서 반드시 정의
    META: ModuleMeta

    # ── 필수 구현 메서드 ────────────────────────────────────────────────────

    @abstractmethod
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        """
        수학적으로 유효한 시드(변수 집합)를 생성합니다.
        :param difficulty_hint: DAPS 목표 점수 (1.0 ~ 15.0)
        :return: 변수 이름 → 값의 딕셔너리
        """
        ...

    @abstractmethod
    def execute(self, seed: dict[str, Any]) -> int:
        """
        시드를 받아 정답(0~999 정수)을 계산합니다.
        AIME 정답 형식: 0 ≤ answer ≤ 999
        :return: 정수 정답
        """
        ...

    @abstractmethod
    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        """
        이 문제를 풀기 위한 논리적 단계들을 반환합니다.
        DAPS의 'logical_depth' 계산에 사용됩니다.
        :return: 논리 단계 설명 리스트
        """
        ...

    # ── 자동 제공 메서드 (오버라이드 불필요) ────────────────────────────────

    def get_daps_contribution(self, seed: dict[str, Any]) -> float:
        """이 모듈이 기여하는 DAPS 점수를 계산합니다."""
        base = self.META.daps_contribution
        depth_bonus = len(self.get_logic_steps(seed)) * 0.3
        
        # V2 전략 보너스
        strategy_bonus = 0.0
        if "conceal" in self.META.v2_strategy_tags:
            strategy_bonus += 0.5
        if "asymmetry" in self.META.v2_strategy_tags:
            strategy_bonus += 0.3
            
        heuristic_bonus = self.META.heuristic_weight
        daps_total = base + depth_bonus + heuristic_bonus + strategy_bonus
        return min(daps_total, 7.5)   # V2에서는 전략 요소로 인해 천장 7.5로 상향

    def validate_seed(self, seed: dict[str, Any]) -> tuple[bool, str]:
        """
        시드가 INPUT_SCHEMA를 만족하는지 검사합니다.
        """
        for field_name, spec in self.META.input_schema.items():
            if field_name not in seed:
                return False, f"필수 변수 누락: '{field_name}'"
            val = seed[field_name]
            # dtype 검사 (익명화된 경우 스킵하거나 유연하게 대응 필요)
            if not isinstance(val, spec.dtype):
                # float/int 호환성 예외 처리
                if spec.dtype == float and isinstance(val, int):
                    pass
                else:
                    return False, f"'{field_name}': {spec.dtype.__name__} 필요, {type(val).__name__} 입력됨"
        return True, "OK"

    def validate_answer(self, answer: int) -> tuple[bool, str]:
        """AIME 정답 유효성 검사 (0 ≤ answer ≤ 999)."""
        if not isinstance(answer, (int, float)):
            return False, f"정답이 숫자가 아님: {type(answer).__name__}"
        
        # float인 경우 정수 여부 확인
        if isinstance(answer, float):
            if not answer.is_integer():
                return False, f"정답이 정수가 아님: {answer}"
            answer = int(answer)

        if not (0 <= answer <= 999):
            return False, f"정답 범위 초과: {answer} (허용: 0~999)"
        return True, "OK"

    def get_module_hash(self) -> str:
        """모듈의 고유 해시."""
        return hashlib.md5(self.META.module_id.encode()).hexdigest()[:8]

    @classmethod
    def get_namespace(cls) -> str:
        """이 모듈의 변수 네임스페이스를 반환합니다."""
        return cls.META.namespace

    def __repr__(self) -> str:
        return f"<AtomicModule: {self.META.module_id} (V2={self.META.v2_compatible})>"


# ─── 조합 충돌 검사 유틸 ────────────────────────────────────────────────────

def check_namespace_conflict(mod_a: AtomicModule, mod_b: AtomicModule) -> tuple[bool, str]:
    if mod_a.META.namespace == mod_b.META.namespace:
        return False, f"네임스페이스 충돌: '{mod_a.META.namespace}'"
    return True, "OK"


def check_domain_compatibility(mod_a: AtomicModule, mod_b: AtomicModule) -> tuple[bool, str]:
    if mod_a.META.domain != mod_b.META.domain:
        return False, (
            f"도메인 불일치: {mod_a.META.module_id}({mod_a.META.domain}) ↔ "
            f"{mod_b.META.module_id}({mod_b.META.domain})"
        )
    return True, "OK"


def check_answer_scale_compatibility(mod_a: AtomicModule, mod_b: AtomicModule) -> tuple[bool, str]:
    scale_a = mod_a.META.output_schema.get("answer_scale", {})
    scale_b = mod_b.META.output_schema.get("answer_scale", {})
    if scale_a != scale_b:
        return False, f"정답 스케일 불일치"
    return True, "OK"

