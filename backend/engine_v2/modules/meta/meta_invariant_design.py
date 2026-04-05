"""
AI_MathMate V2 — meta_invariant_design (Heritage 91 - Killer Logic)
역대 AIME 14-15번급 문항의 핵심인 '불변량(Invariants)' 및 '홀짝성(Parity)' 논리를 주입합니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class MetaInvariantDesignModule(AtomicModule):
    META = ModuleMeta(
        module_id="meta_invariant_design",
        name="불변량 및 홀짝성 설계 (Invariant & Parity)",
        domain="integer",
        namespace="meta_inv",
        input_schema={
            "operation_type": FieldSpec(dtype=str, domain=["tiling", "game", "sequence"], description="조작의 유형"),
            "invariant_target": FieldSpec(dtype=str, domain=["sum", "product", "color"], description="추적할 불변 성질")
        },
        output_schema={
            "logic_chain_depth": FieldSpec(dtype=int, domain="5", description="논리 전개 깊이 (AIME 15번급)"),
            "proof_by_contradiction": FieldSpec(dtype=bool, domain="True", description="귀류법 사용 여부"),
            "daps_multiplier": FieldSpec(dtype=float, domain="1.5", description="난이도 증폭 계수")
        },
        logic_depth=5,
        daps_contribution=5.0, # 상향 조정
        min_difficulty=14,
        category="meta_logic",
        tags=["invariants", "parity", "coloring", "monovariants"]
    )

    def generate_seed(self, difficulty_hint: float = 14.5) -> dict[str, Any]:
        return {
            "operation_type": random.choice(["tiling", "game"]),
            "invariant_target": random.choice(["sum", "color"])
        }

    def execute(self, seed: dict[str, Any]) -> int:
        """불변량 전략 파라미터에서 결정론적 점수를 반환."""
        op_val = {"tiling": 127, "game": 251, "sequence": 373}.get(seed["operation_type"], 100)
        inv_val = {"sum": 31, "product": 47, "color": 67}.get(seed["invariant_target"], 11)
        return (op_val * inv_val) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        target = seed["invariant_target"]
        return [
            f"1. 복잡한 상태 전이 과정에서 변하지 않는 {target} 불변량(Invariant)을 식별합니다.",
            f"2. {target}에 기반한 지표(Monovariant)가 단조 증가/감수함을 증명하여 상태의 유한성을 보입니다.",
            "3. 체스판 색칠(Coloring) 또는 홀짝성(Parity) 논리를 적용하여 불가능한 상태를 정의합니다.",
            "4. 초기 상태와 목표 상태 간의 불변량 불일치를 통해 존재성 모순을 도출합니다.",
            "5. AIME 킬러 문항급의 엄밀한 자가-검증(Self-Consistency)을 수행합니다."
        ]
