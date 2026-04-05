"""
AI_MathMate V2 -- meta_logic_concealer (논리 은폐 전략)
풀이 과정에서 핵심 중간 단계(징검다리)를 지문에서 은폐하여
학생이 스스로 논리적 도약(leap)을 수행하도록 강제합니다.
AIME 13-15번급의 핵심 난이도 요소.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class MetaLogicConcealerModule(AtomicModule):
    META = ModuleMeta(
        module_id="meta_logic_concealer",
        name="논리 은폐 전략 (Logic Concealer)",
        domain="integer",
        namespace="meta_conceal",
        input_schema={
            "logic_steps": FieldSpec(dtype=list, domain="Steps", description="원본 논리 단계 목록"),
            "conceal_ratio": FieldSpec(dtype=float, domain="[0.2, 0.8]", description="은폐 비율"),
            "conceal_strategy": FieldSpec(dtype=str, domain=["merge", "abstract", "reorder"],
                                           description="은폐 전략"),
        },
        output_schema={
            "concealed_steps": FieldSpec(dtype=list, domain="Steps", description="은폐된 논리 단계 목록"),
            "leap_count": FieldSpec(dtype=int, domain="Z+", description="도약이 필요한 지점 수"),
            "daps_multiplier": FieldSpec(dtype=float, domain="R+", description="난이도 증폭 계수"),
        },
        logic_depth=4,
        daps_contribution=3.5,
        min_difficulty=12,
        category="meta",
        tags=["concealment", "logic_leap", "scaffolding_removal", "difficulty_amplifier"],
        v2_strategy_tags=["conceal"],
    )

    def generate_seed(self, difficulty_hint: float = 13.0) -> dict[str, Any]:
        strategies = ["merge", "abstract", "reorder"]
        # 난이도에 비례한 은폐 비율
        ratio = min(0.8, max(0.2, (difficulty_hint - 10) / 10))
        sample_steps = [
            "주어진 조건에서 핵심 등식을 유도합니다.",
            "등식을 변형하여 중간값을 구합니다.",
            "중간값을 대입하여 새로운 관계를 얻습니다.",
            "최종 조건을 만족하는 해를 구합니다.",
        ]
        return {
            "logic_steps": sample_steps,
            "conceal_ratio": ratio,
            "conceal_strategy": random.choice(strategies),
        }

    def execute(self, seed: dict[str, Any]) -> int:
        """은폐 전략에서 결정론적 난이도 점수를 반환."""
        steps = seed["logic_steps"]
        ratio = seed["conceal_ratio"]
        strategy = seed["conceal_strategy"]
        n_conceal = max(1, int(len(steps) * ratio))
        strategy_val = {"merge": 7, "abstract": 11, "reorder": 13}.get(strategy, 5)
        daps_multiplier = int((1.0 + ratio * 0.8) * 100)
        return (n_conceal * strategy_val * len(steps) + daps_multiplier) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n_conceal = max(1, int(len(seed["logic_steps"]) * seed["conceal_ratio"]))
        strategy = seed["conceal_strategy"]
        return [
            f"1. 원본 {len(seed['logic_steps'])}단계의 풀이 과정을 분석합니다.",
            f"2. '{strategy}' 전략으로 은폐 비율 {seed['conceal_ratio']:.0%}를 적용합니다.",
            f"3. {n_conceal}개의 논리적 도약 지점을 생성합니다.",
        ]
