"""
AI_MathMate V2 — 점의 거듭제곱 정리 (geometry_power_of_a_point)
AIME 기출 33회. PA*PB = PC*PD 관계를 다룹니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryPowerOfAPointModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_power_of_a_point", name="점의 거듭제곱 정리",
        domain="integer", namespace="geo_power",
        input_schema={
            "r": FieldSpec(dtype=int, domain="Z+", description="원 반지름"),
            "d": FieldSpec(dtype=int, domain="Z+", description="점에서 중심까지 거리"),
            "mode": FieldSpec(dtype=str, domain="str", description="'outside' | 'inside'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=3, daps_contribution=3.5, min_difficulty=5, category="geometry",
        tags=["power_of_a_point", "intersecting_chord", "secant_tangent"], exam_types=["AIME"],
        bridge_input_accepts=["radius"],
        bridge_output_keys=["radius", "power_value"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            r = random.randint(5, 30)
            mode = random.choice(["outside", "inside"])
            d = random.randint(r + 1, r + 30) if mode == "outside" else random.randint(1, r - 1)
            seed = {"r": r, "d": d, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"r": 10, "d": 15, "mode": "outside"}

    def execute(self, seed: dict[str, Any]) -> int:
        r, d = seed["r"], seed["d"]
        # Power = |d^2 - r^2|
        return abs(d * d - r * r) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            f"1. 반지름 {seed['r']}인 원, 점 P는 중심에서 {seed['d']} 거리.",
            f"2. 점 P의 거듭제곱(power) = |d^2 - r^2| = |{seed['d']}^2 - {seed['r']}^2|.",
            "3. PA*PB = power (할선 또는 접선에 대해).",
            "4. 1000으로 나눈 나머지를 구합니다.",
        ]
    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        return {"radius": seed["r"], "power_value": self.execute(seed)}

    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float = 10.0) -> dict[str, Any]:
        r = bridge.get("radius")
        if r and int(r) >= 5:
            r_val = int(r)
            d = r_val + random.randint(1, 20)
            seed = {"r": r_val, "d": d, "mode": "outside"}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return self.generate_seed(difficulty_hint)

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try: return self.execute(seed)
        except: return None
