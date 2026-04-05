"""
AI_MathMate V2 -- meta_rationale_layering (다층 추론 강제 전략)
단일 계산 단계로 풀 수 있는 문제를 여러 겹의 추론 레이어로 감싸서
학생이 최소 N단계의 논리적 사슬을 밟도록 강제합니다.
AIME 10-15번급 문항의 'logical_depth' 확장 핵심 전략.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class MetaRationaleLayeringModule(AtomicModule):
    META = ModuleMeta(
        module_id="meta_rationale_layering",
        name="다층 추론 강제 전략 (Rationale Layering)",
        domain="integer",
        namespace="meta_layer",
        input_schema={
            "base_depth": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=5, description="원본 논리 깊이"),
            "target_depth": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=8, description="목표 논리 깊이"),
            "layering_method": FieldSpec(dtype=str, domain=["substitution", "composition", "constraint_chain"],
                                          description="레이어링 방법"),
        },
        output_schema={
            "added_layers": FieldSpec(dtype=list, domain="Steps", description="추가된 추론 레이어"),
            "final_depth": FieldSpec(dtype=int, domain="Z+", description="최종 논리 깊이"),
            "daps_bonus": FieldSpec(dtype=float, domain="R+", description="레이어링으로 인한 DAPS 보너스"),
        },
        logic_depth=4,
        daps_contribution=3.0,
        min_difficulty=10,
        category="meta",
        tags=["rationale_layering", "depth_extension", "multi_step", "substitution_chain"],
        v2_strategy_tags=["conceal", "asymmetry"],
    )

    # 레이어 템플릿
    _SUBSTITUTION_LAYERS = [
        "변수 t = f(x)로 치환하여 새로운 등식을 유도합니다.",
        "치환된 등식에서 t에 대한 조건을 재정립합니다.",
        "역치환을 통해 원래 변수의 범위를 확정합니다.",
    ]
    _COMPOSITION_LAYERS = [
        "함수 합성 g(f(x))를 분석하여 중첩된 구조를 파악합니다.",
        "내부 함수의 치역이 외부 함수의 정의역에 포함됨을 검증합니다.",
        "합성 함수의 고정점 또는 주기를 결정합니다.",
    ]
    _CONSTRAINT_LAYERS = [
        "첫 번째 제약 조건에서 후보 집합을 축소합니다.",
        "두 번째 제약 조건을 적용하여 교집합을 구합니다.",
        "최종 제약 조건으로 유일한 해를 결정합니다.",
    ]

    def generate_seed(self, difficulty_hint: float = 12.0) -> dict[str, Any]:
        methods = ["substitution", "composition", "constraint_chain"]
        base_depth = random.randint(1, 3)
        target_depth = random.randint(max(3, base_depth + 1), min(8, base_depth + 5))
        return {
            "base_depth": base_depth,
            "target_depth": target_depth,
            "layering_method": random.choice(methods),
        }

    def execute(self, seed: dict[str, Any]) -> int:
        """레이어링 파라미터에서 결정론적 점수를 반환."""
        base = seed["base_depth"]
        target = seed["target_depth"]
        method = seed["layering_method"]
        method_val = {"substitution": 31, "composition": 37, "constraint_chain": 43}.get(method, 29)
        n_layers = target - base
        return (target * method_val + n_layers * 100 + base * 7) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n_layers = seed["target_depth"] - seed["base_depth"]
        method = seed["layering_method"]
        return [
            f"1. 원본 논리 깊이 {seed['base_depth']}에서 목표 깊이 {seed['target_depth']}로 확장합니다.",
            f"2. '{method}' 방법으로 {n_layers}개의 추론 레이어를 삽입합니다.",
            f"3. 각 레이어가 수학적 무결성을 유지하면서 풀이 경로를 연장합니다.",
        ]
