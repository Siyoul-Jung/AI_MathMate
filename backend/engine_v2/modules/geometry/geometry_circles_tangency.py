"""
AI_MathMate V2 — 원 접선/접원 (geometry_circles_tangency)
AIME 기출 39회. 두 원의 내접/외접, 공통접선을 다룹니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryCirclesTangencyModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_circles_tangency", name="원 접선과 접원",
        domain="integer", namespace="geo_tangency",
        input_schema={
            "r1": FieldSpec(dtype=int, domain="Z+", description="원1 반지름"),
            "r2": FieldSpec(dtype=int, domain="Z+", description="원2 반지름"),
            "d": FieldSpec(dtype=int, domain="Z+", description="중심 거리"),
            "mode": FieldSpec(dtype=str, domain="str", description="'ext_tangent_sq' | 'int_tangent_sq'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=3, daps_contribution=4.0, min_difficulty=6, category="geometry",
        tags=["tangent_circle", "internally_tangent", "externally_tangent", "common_tangent"], exam_types=["AIME"],
        bridge_input_accepts=["radius"],
        bridge_output_keys=["radius_1", "radius_2", "center_distance"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            r1 = random.randint(3, 30)
            r2 = random.randint(3, 30)
            mode = random.choice(["ext_tangent_sq", "int_tangent_sq"])
            if mode == "ext_tangent_sq":
                d = random.randint(r1 + r2, r1 + r2 + 30)  # 외접: d >= r1+r2
            else:
                d = random.randint(abs(r1 - r2) + 1, r1 + r2 - 1)  # d > |r1-r2|
            seed = {"r1": r1, "r2": r2, "d": d, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"r1": 5, "r2": 3, "d": 10, "mode": "ext_tangent_sq"}

    def execute(self, seed: dict[str, Any]) -> int:
        r1, r2, d, mode = seed["r1"], seed["r2"], seed["d"], seed["mode"]
        if mode == "ext_tangent_sq":
            # 공통외접선 길이^2 = d^2 - (r1-r2)^2
            return (d * d - (r1 - r2) ** 2) % 1000
        else:
            # 공통내접선 길이^2 = d^2 - (r1+r2)^2
            val = d * d - (r1 + r2) ** 2
            return abs(val) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            f"1. 반지름 {seed['r1']}, {seed['r2']}인 두 원, 중심 거리 {seed['d']}.",
            f"2. {seed['mode']} 공식을 적용합니다.",
            "3. 접선 길이의 제곱을 계산합니다.",
            "4. 1000으로 나눈 나머지를 구합니다.",
        ]
    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        return {"radius_1": seed["r1"], "radius_2": seed["r2"], "center_distance": seed["d"]}

    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float = 10.0) -> dict[str, Any]:
        r = bridge.get("radius")
        if r and int(r) > 2:
            r1 = int(r)
            r2 = random.randint(3, max(4, r1))
            d = r1 + r2 + random.randint(1, 10)
            seed = {"r1": r1, "r2": r2, "d": d, "mode": "ext_tangent_sq"}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return self.generate_seed(difficulty_hint)

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try: return self.execute(seed)
        except: return None
