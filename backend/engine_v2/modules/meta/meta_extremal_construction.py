"""
AI_MathMate V2 — meta_extremal_construction (Heritage 91 - Killer Logic)
AIME 14-15번급 문항의 핵심인 '극단성의 원리(Extremal Principle)' 및 '무한 강하법' 논리를 주입합니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class MetaExtremalConstructionModule(AtomicModule):
    META = ModuleMeta(
        module_id="meta_extremal_construction",
        name="극단성의 원리 설계 (Extremal Principle)",
        domain="meta",
        namespace="meta_ext",
        input_schema={
            "extremal_element": FieldSpec(dtype=str, domain=["max", "min", "hull"], description="가정할 극단적인 대상"),
            "proof_strategy": FieldSpec(dtype=str, domain=["contradiction", "infinite_descent"], description="증명 전략")
        },
        output_schema={
            "logic_chain_depth": FieldSpec(dtype=int, domain="5", description="논리 전개 깊이"),
            "existence_guarantee": FieldSpec(dtype=bool, domain="True", description="존재성 증명 여부"),
            "daps_multiplier": FieldSpec(dtype=float, domain="1.5", description="난이도 증폭 계수")
        },
        logic_depth=5,
        daps_contribution=5.0, # 상향 조정
        min_difficulty=14,
        category="meta_logic",
        tags=["extremal", "infinite_descent", "existence", "combinatorial_geometry"]
    )

    def generate_seed(self, difficulty_hint: float = 14.5) -> dict[str, Any]:
        return {
            "extremal_element": random.choice(["max", "min"]),
            "proof_strategy": random.choice(["contradiction", "infinite_descent"])
        }

    def execute(self, seed: dict[str, Any]) -> dict[str, Any]:
        return {
            "logic_chain_depth": 5,
            "existence_guarantee": True,
            "daps_multiplier": 1.5
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        element = seed["extremal_element"]
        strategy = seed["proof_strategy"]
        return [
            f"1. 집합 S의 원소 중 {element}인 대상을 선택하여 극단적인 상태를 가정합니다.",
            f"2. {strategy} 전략을 통해, 이보다 더 극단적인 원소가 존재할 수 없음을 수식으로 전개합니다.",
            "3. (Infinite Descent) 만약 더 작은 원소가 존재한다면 무한히 내려가야 하는 모순을 유도합니다.",
            "4. 이산적인 집합에서의 웰-오더링성(Well-ordering)을 활용하여 최종 존재 증명을 마무리합니다.",
            "5. AIME 15번급의 고난도 직관적 도약 포인트를 지문에 배치합니다."
        ]
