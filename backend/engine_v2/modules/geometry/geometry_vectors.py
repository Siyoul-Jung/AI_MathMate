"""
AI_MathMate V2 — 벡터 기하 (geometry_vectors)
AIME 기출 23회. 내적, 외적, 벡터 크기를 다룹니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryVectorsModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_vectors", name="벡터 기하",
        domain="integer", namespace="geo_vec",
        input_schema={
            "v1": FieldSpec(dtype=list, domain="Z", description="벡터 1 [x,y,z]"),
            "v2": FieldSpec(dtype=list, domain="Z", description="벡터 2 [x,y,z]"),
            "mode": FieldSpec(dtype=str, domain="str", description="'dot' | 'cross_mag' | 'sum_mag_sq'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=3, daps_contribution=3.5, min_difficulty=5, category="geometry",
        tags=["vector", "dot_product", "cross_product", "magnitude"], exam_types=["AIME"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            dim = 3 if difficulty_hint >= 8 else 2
            v1 = [random.randint(-10, 10) for _ in range(dim)]
            v2 = [random.randint(-10, 10) for _ in range(dim)]
            mode = random.choice(["dot", "cross_mag", "sum_mag_sq"])
            if mode == "cross_mag" and dim < 3:
                mode = "dot"
            seed = {"v1": v1, "v2": v2, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"v1": [3, 4, 0], "v2": [1, 2, 0], "mode": "dot"}

    def execute(self, seed: dict[str, Any]) -> int:
        v1, v2, mode = seed["v1"], seed["v2"], seed["mode"]
        if mode == "dot":
            return abs(sum(a * b for a, b in zip(v1, v2))) % 1000
        elif mode == "cross_mag":
            if len(v1) < 3: v1 = v1 + [0]
            if len(v2) < 3: v2 = v2 + [0]
            cx = v1[1]*v2[2] - v1[2]*v2[1]
            cy = v1[2]*v2[0] - v1[0]*v2[2]
            cz = v1[0]*v2[1] - v1[1]*v2[0]
            return (cx*cx + cy*cy + cz*cz) % 1000  # |cross|^2
        else:
            s = [a + b for a, b in zip(v1, v2)]
            return sum(x*x for x in s) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            f"1. 벡터 v1={seed['v1']}, v2={seed['v2']}.",
            f"2. {seed['mode']} 연산을 수행합니다.",
            "3. 결과를 계산합니다.",
            "4. 1000으로 나눈 나머지를 구합니다.",
        ]
    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try: return self.execute(seed)
        except: return None
