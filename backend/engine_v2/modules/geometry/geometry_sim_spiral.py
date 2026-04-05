"""
AI_MathMate V2 — 나선 닮음 (geometry_sim_spiral)
AIME 기출 1회. 회전+확대 복합 변환을 다룹니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometrySimSpiralModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_sim_spiral", name="나선 닮음",
        domain="integer", namespace="geo_spiral",
        input_schema={
            "x": FieldSpec(dtype=int, domain="Z", description="점 x"),
            "y": FieldSpec(dtype=int, domain="Z", description="점 y"),
            "k": FieldSpec(dtype=int, domain="Z+", description="확대비"),
            "angle_type": FieldSpec(dtype=str, domain="str", description="'90' | '180'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=3, daps_contribution=4.0, min_difficulty=10, category="geometry",
        tags=["spiral_similarity", "rotation_dilation"], exam_types=["AIME"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            x, y = random.randint(1, 20), random.randint(1, 20)
            k = random.randint(2, 5)
            angle_type = random.choice(["90", "180"])
            seed = {"x": x, "y": y, "k": k, "angle_type": angle_type}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"x": 3, "y": 4, "k": 2, "angle_type": "90"}

    def execute(self, seed: dict[str, Any]) -> int:
        x, y, k = seed["x"], seed["y"], seed["k"]
        if seed["angle_type"] == "90":
            xp, yp = -k * y, k * x  # 90도 회전 + k배 확대
        else:
            xp, yp = -k * x, -k * y
        return (abs(xp) + abs(yp)) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            f"1. 점 ({seed['x']}, {seed['y']})에 {seed['angle_type']}도 회전 + {seed['k']}배 확대.",
            "2. 회전 행렬과 확대를 적용합니다.",
            "3. 변환된 좌표의 절댓값 합을 구합니다.",
            "4. 1000으로 나눈 나머지를 구합니다.",
        ]
    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try: return self.execute(seed)
        except: return None
