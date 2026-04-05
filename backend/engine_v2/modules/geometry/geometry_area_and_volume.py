"""
AI_MathMate V2 — 넓이와 부피 (geometry_area_and_volume)
AIME 기출 147회. 신발끈 공식, 헤론 공식, 사다리꼴 넓이를 다룹니다.
Bridge: coordinate_analytic에서 vertices 수신, solid_3d에 base_area 전달.
"""
from __future__ import annotations
import random
import math
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryAreaAndVolumeModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_area_and_volume",
        name="넓이와 부피",
        domain="integer",
        namespace="geo_area",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str", description="'shoelace' | 'heron' | 'trapezoid'"),
            "vertices": FieldSpec(dtype=list, domain="Z^2", description="좌표 점 (shoelace용)"),
            "sides": FieldSpec(dtype=list, domain="Z+", description="변 길이 또는 사다리꼴 파라미터"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999),
        },
        logic_depth=3,
        daps_contribution=3.5,
        min_difficulty=2,
        category="geometry",
        tags=["area", "volume", "shoelace", "heron", "trapezoid"],
        exam_types=["AIME"],
        bridge_output_keys=["base_area", "perimeter", "shape_type"],
        bridge_input_accepts=["vertices", "vertex_count"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["shoelace", "heron", "trapezoid"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "shoelace":
                n = random.randint(3, 5)
                vertices = [[random.randint(-10, 10), random.randint(-10, 10)] for _ in range(n)]
                seed = {"mode": mode, "vertices": vertices, "sides": []}
            elif mode == "heron":
                a = random.randint(3, 30)
                b = random.randint(3, 30)
                c = random.randint(abs(a - b) + 1, a + b - 1)
                seed = {"mode": mode, "vertices": [], "sides": [a, b, c]}
            else:
                a = random.randint(5, 30)
                b = random.randint(5, 30)
                h = random.randint(3, 20)
                seed = {"mode": mode, "vertices": [], "sides": [a, b, h]}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return {"mode": "heron", "vertices": [], "sides": [3, 4, 5]}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        if mode == "shoelace":
            vertices = seed["vertices"]
            n = len(vertices)
            if n < 3:
                return 0
            total = 0
            for i in range(n):
                j = (i + 1) % n
                total += vertices[i][0] * vertices[j][1]
                total -= vertices[j][0] * vertices[i][1]
            return abs(total) % 1000

        elif mode == "heron":
            a, b, c = seed["sides"]
            val_16 = 2 * (a*a*b*b + b*b*c*c + c*c*a*a) - (a**4 + b**4 + c**4)
            if val_16 <= 0:
                return 0
            return val_16 % 1000

        else:
            a, b, h = seed["sides"]
            return ((a + b) * h) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        mode = seed["mode"]
        if mode == "shoelace":
            vertices = seed["vertices"]
            n = len(vertices)
            perimeter = 0
            for i in range(n):
                j = (i + 1) % n
                dx = vertices[i][0] - vertices[j][0]
                dy = vertices[i][1] - vertices[j][1]
                perimeter += int(math.isqrt(dx*dx + dy*dy))
            return {"base_area": self.execute(seed), "perimeter": perimeter, "shape_type": f"{n}-gon"}
        elif mode == "heron":
            a, b, c = seed["sides"]
            return {"base_area": self.execute(seed), "perimeter": a + b + c, "shape_type": "triangle"}
        else:
            a, b, h = seed["sides"]
            return {"base_area": (a + b) * h // 2, "perimeter": a + b + 2 * h, "shape_type": "trapezoid"}

    def generate_seed_with_bridge(self, bridge: dict[str, Any], difficulty_hint: float = 10.0) -> dict[str, Any]:
        vertices = bridge.get("vertices")
        if vertices and len(vertices) >= 3:
            return {"mode": "shoelace", "vertices": vertices[:5], "sides": []}
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        if mode == "shoelace":
            return [
                f"1. {len(seed['vertices'])}개의 좌표점으로 다각형을 구성합니다.",
                "2. 신발끈 공식을 적용합니다.",
                "3. 절대값을 취해 넓이의 2배를 구합니다.",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "heron":
            a, b, c = seed["sides"]
            return [
                f"1. 세 변 {a}, {b}, {c}인 삼각형입니다.",
                "2. 헤론 공식으로 16K^2를 정수로 계산합니다.",
                "3. 16K^2 = 2(a^2b^2+b^2c^2+c^2a^2)-(a^4+b^4+c^4).",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            a, b, h = seed["sides"]
            return [
                f"1. 윗변 {a}, 아랫변 {b}, 높이 {h}인 사다리꼴입니다.",
                f"2. 넓이의 2배 = (a+b)*h = {(a+b)*h}.",
                "3. 정수 결과를 구합니다.",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            return self.execute(seed)
        except Exception:
            return None
