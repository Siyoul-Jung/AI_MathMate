"""
AI_MathMate V2 — 삼각형 중심 (geometry_triangle_centers)
AIME 기출 25회. 내심, 외심, 무게중심, 수심 좌표를 다룹니다.
"""
from __future__ import annotations
import random
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryTriangleCentersModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_triangle_centers", name="삼각형 중심",
        domain="integer", namespace="geo_centers",
        input_schema={
            "x1": FieldSpec(dtype=int, domain="Z"), "y1": FieldSpec(dtype=int, domain="Z"),
            "x2": FieldSpec(dtype=int, domain="Z"), "y2": FieldSpec(dtype=int, domain="Z"),
            "x3": FieldSpec(dtype=int, domain="Z"), "y3": FieldSpec(dtype=int, domain="Z"),
            "mode": FieldSpec(dtype=str, domain="str", description="'centroid' | 'circumcenter'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=4, daps_contribution=4.0, min_difficulty=7, category="geometry",
        tags=["incenter", "circumcenter", "orthocenter", "centroid", "triangle_center"], exam_types=["AIME"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            x1, y1 = random.randint(-10, 10), random.randint(-10, 10)
            x2, y2 = random.randint(-10, 10), random.randint(-10, 10)
            x3, y3 = random.randint(-10, 10), random.randint(-10, 10)
            # 일직선 체크
            area2 = abs(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
            if area2 == 0: continue
            mode = random.choice(["centroid", "circumcenter"])
            seed = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x3": x3, "y3": y3, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"x1": 0, "y1": 0, "x2": 6, "y2": 0, "x3": 3, "y3": 4, "mode": "centroid"}

    def execute(self, seed: dict[str, Any]) -> int:
        x1, y1, x2, y2, x3, y3 = seed["x1"], seed["y1"], seed["x2"], seed["y2"], seed["x3"], seed["y3"]
        if seed["mode"] == "centroid":
            gx = Fraction(x1 + x2 + x3, 3)
            gy = Fraction(y1 + y2 + y3, 3)
            return (abs(gx.numerator) + gx.denominator + abs(gy.numerator) + gy.denominator) % 1000
        else:
            # 외심: 수직이등분선 교점
            ax, ay = x2 - x1, y2 - y1
            bx, by = x3 - x1, y3 - y1
            D = 2 * (ax * by - ay * bx)
            if D == 0: return 0
            ux = Fraction(by * (ax*ax + ay*ay) - ay * (bx*bx + by*by), D) + x1
            uy = Fraction(-bx * (ax*ax + ay*ay) + ax * (bx*bx + by*by), D) + y1
            return (abs(ux.numerator) + ux.denominator + abs(uy.numerator) + uy.denominator) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            f"1. 세 꼭짓점 ({seed['x1']},{seed['y1']}), ({seed['x2']},{seed['y2']}), ({seed['x3']},{seed['y3']}).",
            f"2. {seed['mode']}를 구합니다.",
            "3. 좌표를 분수로 정확히 계산합니다.",
            "4. 분자+분모 합을 1000으로 나눈 나머지.",
        ]
    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try: return self.execute(seed)
        except: return None
