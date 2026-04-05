"""
AI_MathMate V2 — 복소수 기하 (geometry_complex_numbers_in_geometry)
복소평면 위의 점들 사이 거리 제곱합, 삼각형 넓이 등을 다룹니다.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryComplexNumbersInGeometryModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_complex_numbers_in_geometry",
        name="복소수 기하",
        domain="integer",
        namespace="geom_complex",
        input_schema={
            "x1": FieldSpec(dtype=int, domain="Z", min_val=-15, max_val=15, description="z1 실수부"),
            "y1": FieldSpec(dtype=int, domain="Z", min_val=-15, max_val=15, description="z1 허수부"),
            "x2": FieldSpec(dtype=int, domain="Z", min_val=-15, max_val=15, description="z2 실수부"),
            "y2": FieldSpec(dtype=int, domain="Z", min_val=-15, max_val=15, description="z2 허수부"),
            "x3": FieldSpec(dtype=int, domain="Z", min_val=-15, max_val=15, description="z3 실수부"),
            "y3": FieldSpec(dtype=int, domain="Z", min_val=-15, max_val=15, description="z3 허수부"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'distance' | 'area'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=6,
        category="geometry",
        tags=["complex_plane", "distance", "triangle_area", "modulus"],
        exam_types=["AIME"],
        bridge_output_keys=["distance_squared_sum", "triangle_area_double"],
        bridge_input_accepts=["modulus_squared", "argument_degrees"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["distance", "area"]
        for _ in range(100):
            mode = random.choice(modes)
            lo, hi = (-8, 8) if difficulty_hint < 10 else (-15, 15)
            x1 = random.randint(lo, hi)
            y1 = random.randint(lo, hi)
            x2 = random.randint(lo, hi)
            y2 = random.randint(lo, hi)
            x3 = random.randint(lo, hi)
            y3 = random.randint(lo, hi)

            seed = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x3": x3, "y3": y3, "mode": mode}

            # area 모드: 비퇴화 삼각형(넓이 > 0) 보장
            if mode == "area":
                cross = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
                if cross == 0:
                    continue

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        # Fallback seed
        return {"x1": 1, "y1": 2, "x2": 4, "y2": 6, "x3": 7, "y3": 3, "mode": "distance"}

    def execute(self, seed: dict[str, Any]) -> int:
        x1, y1 = seed["x1"], seed["y1"]
        x2, y2 = seed["x2"], seed["y2"]
        x3, y3 = seed["x3"], seed["y3"]
        mode = seed["mode"]

        if mode == "distance":
            # |z1 - z2|^2 + |z2 - z3|^2
            d12_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
            d23_sq = (x2 - x3) ** 2 + (y2 - y3) ** 2
            return (d12_sq + d23_sq) % 1000
        else:
            # 삼각형 넓이의 2배 = |외적| = |(x2-x1)(y3-y1) - (x3-x1)(y2-y1)|
            cross = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
            return cross % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        x1, y1 = seed["x1"], seed["y1"]
        x2, y2 = seed["x2"], seed["y2"]
        x3, y3 = seed["x3"], seed["y3"]
        d12_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
        d23_sq = (x2 - x3) ** 2 + (y2 - y3) ** 2
        cross = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
        return {
            "distance_squared_sum": d12_sq + d23_sq,
            "triangle_area_double": cross,
        }

    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float = 10.0) -> dict[str, Any]:
        mod_sq = bridge.get("modulus_squared")
        arg_deg = bridge.get("argument_degrees")
        if mod_sq is not None:
            r = int(math.isqrt(int(mod_sq))) if int(mod_sq) > 0 else 3
            r = max(1, min(r, 15))
            angle = int(arg_deg) if arg_deg is not None else 45
            rad = math.radians(angle)
            x1, y1 = int(r * math.cos(rad)), int(r * math.sin(rad))
            x2, y2 = random.randint(-8, 8), random.randint(-8, 8)
            x3, y3 = random.randint(-8, 8), random.randint(-8, 8)
            seed = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x3": x3, "y3": y3, "mode": "distance"}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        x1, y1 = seed["x1"], seed["y1"]
        x2, y2 = seed["x2"], seed["y2"]
        x3, y3 = seed["x3"], seed["y3"]
        mode = seed["mode"]

        if mode == "distance":
            d12_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
            d23_sq = (x2 - x3) ** 2 + (y2 - y3) ** 2
            return [
                f"1. 복소평면 위 세 점 z1=({x1}+{y1}i), z2=({x2}+{y2}i), z3=({x3}+{y3}i)를 설정합니다.",
                f"2. |z1-z2|^2 = ({x1}-{x2})^2 + ({y1}-{y2})^2 = {d12_sq}를 계산합니다.",
                f"3. |z2-z3|^2 = ({x2}-{x3})^2 + ({y2}-{y3})^2 = {d23_sq}를 계산합니다.",
                f"4. 두 거리 제곱의 합 {d12_sq} + {d23_sq} = {d12_sq + d23_sq}를 구하고 1000으로 나눈 나머지를 취합니다.",
            ]
        else:
            cross = abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
            return [
                f"1. 복소평면 위 세 점 z1=({x1}+{y1}i), z2=({x2}+{y2}i), z3=({x3}+{y3}i)를 설정합니다.",
                f"2. 외적을 이용한 삼각형 넓이 공식: 2*Area = |(x2-x1)(y3-y1) - (x3-x1)(y2-y1)|을 적용합니다.",
                f"3. 2*Area = |({x2}-{x1})*({y3}-{y1}) - ({x3}-{x1})*({y2}-{y1})| = {cross}을 계산합니다.",
                f"4. 결과 {cross}을 1000으로 나눈 나머지를 취합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Integer, Abs
            x1, y1 = Integer(seed["x1"]), Integer(seed["y1"])
            x2, y2 = Integer(seed["x2"]), Integer(seed["y2"])
            x3, y3 = Integer(seed["x3"]), Integer(seed["y3"])
            mode = seed["mode"]

            if mode == "distance":
                d12_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
                d23_sq = (x2 - x3) ** 2 + (y2 - y3) ** 2
                return int((d12_sq + d23_sq) % 1000)
            else:
                cross = Abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1))
                return int(cross % 1000)
        except Exception:
            return None
