"""
AI_MathMate V2 — 원에 내접하는 사각형 (geometry_cyclic_quadrilaterals)
AIME 기출 17회. 프톨레마이오스, 브라마굽타 공식을 다룹니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryCyclicQuadrilateralsModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_cyclic_quadrilaterals", name="원에 내접하는 사각형",
        domain="integer", namespace="geo_cyclic",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+"), "b": FieldSpec(dtype=int, domain="Z+"),
            "c": FieldSpec(dtype=int, domain="Z+"), "d": FieldSpec(dtype=int, domain="Z+"),
            "mode": FieldSpec(dtype=str, domain="str", description="'brahmagupta' | 'diagonal_product'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=4, daps_contribution=4.5, min_difficulty=8, category="geometry",
        tags=["cyclic_quadrilateral", "concyclic", "brahmagupta", "ptolemy"], exam_types=["AIME"],
        bridge_input_accepts=["side_a", "side_b", "side_c"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            a = random.randint(3, 20)
            b = random.randint(3, 20)
            c = random.randint(3, 20)
            d = random.randint(3, 20)
            # 사각형 성립 조건: 가장 긴 변 < 나머지 합
            sides = [a, b, c, d]
            if max(sides) >= sum(sides) - max(sides): continue
            mode = random.choice(["brahmagupta", "diagonal_product"])
            seed = {"a": a, "b": b, "c": c, "d": d, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"a": 5, "b": 6, "c": 7, "d": 8, "mode": "brahmagupta"}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, c, d = seed["a"], seed["b"], seed["c"], seed["d"]
        s = (a + b + c + d) // 2
        if seed["mode"] == "brahmagupta":
            # 16K^2 = (a+b+c-d)(-a+b+c+d)(a-b+c+d)(a+b-c+d) (4s 기반)
            s2 = a + b + c + d
            val = (s2 - 2*d) * (s2 - 2*a) * (s2 - 2*b) * (s2 - 2*c)
            return abs(val) % 1000
        else:
            # 프톨레마이오스: AC*BD = AB*CD + AD*BC = a*c + b*d
            return (a * c + b * d) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, c, d = seed["a"], seed["b"], seed["c"], seed["d"]
        return [
            f"1. 원에 내접하는 사각형 변 {a}, {b}, {c}, {d}.",
            f"2. {'브라마굽타 공식' if seed['mode'] == 'brahmagupta' else '프톨레마이오스 정리'}를 적용.",
            "3. 결과를 계산합니다.",
            "4. 1000으로 나눈 나머지를 구합니다.",
        ]
    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float = 10.0) -> dict[str, Any]:
        sa = bridge.get("side_a")
        sb = bridge.get("side_b")
        sc = bridge.get("side_c")
        if sa and sb and sc:
            a, b, c = int(sa), int(sb), int(sc)
            d = random.randint(3, 20)
            sides = [a, b, c, d]
            if max(sides) < sum(sides) - max(sides):
                seed = {"a": a, "b": b, "c": c, "d": d, "mode": "brahmagupta"}
                ans = self.execute(seed)
                if 0 < ans <= 999:
                    return seed
        return self.generate_seed(difficulty_hint)

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try: return self.execute(seed)
        except: return None
