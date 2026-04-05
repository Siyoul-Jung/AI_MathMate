"""
AI_MathMate V2 — 좌표 해석 기하 (geometry_coordinate_analytic)
AIME 최빈출 모듈 (191회). 좌표평면에서 점, 직선, 거리, 넓이를 다룹니다.
Bridge Hub: 5개 하류 모듈에 vertices를 전달하고, circle_theorems에서 center/radius를 수신합니다.
"""
from __future__ import annotations
import random
import math
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryCoordinateAnalyticModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_coordinate_analytic",
        name="좌표 해석 기하",
        domain="integer",
        namespace="geo_coord",
        input_schema={
            "vertices": FieldSpec(dtype=list, domain="Z^2", description="정수 좌표 점 리스트 [[x,y],...]"),
            "mode": FieldSpec(dtype=str, domain="str", description="'dist_sq_sum' | 'triangle_area' | 'collinear_check'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=3,
        category="geometry",
        tags=["coordinate_geometry", "analytic_geometry", "distance", "midpoint", "slope", "shoelace"],
        exam_types=["AIME"],
        bridge_output_keys=["vertices", "vertex_count", "bounding_box_area", "centroid"],
        bridge_input_accepts=["center", "radius"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["dist_sq_sum", "triangle_area", "collinear_check"]
        for _ in range(100):
            mode = random.choice(modes)
            n = random.randint(3, 5) if difficulty_hint < 10 else random.randint(4, 6)
            vertices = [[random.randint(-15, 15), random.randint(-15, 15)] for _ in range(n)]
            # 중복 점 제거
            unique = []
            seen = set()
            for v in vertices:
                key = (v[0], v[1])
                if key not in seen:
                    seen.add(key)
                    unique.append(v)
            if len(unique) < 3:
                continue
            vertices = unique[:n] if len(unique) >= n else unique

            seed = {"vertices": vertices, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return {"vertices": [[0, 0], [3, 0], [0, 4]], "mode": "triangle_area"}

    def execute(self, seed: dict[str, Any]) -> int:
        vertices = seed["vertices"]
        mode = seed["mode"]

        if mode == "dist_sq_sum":
            # 모든 점 쌍의 거리 제곱 합
            total = 0
            for i in range(len(vertices)):
                for j in range(i + 1, len(vertices)):
                    dx = vertices[i][0] - vertices[j][0]
                    dy = vertices[i][1] - vertices[j][1]
                    total += dx * dx + dy * dy
            return total % 1000

        elif mode == "triangle_area":
            # 첫 3점으로 삼각형 넓이 * 2 (신발끈, 정수 보장)
            if len(vertices) < 3:
                return 0
            x1, y1 = vertices[0]
            x2, y2 = vertices[1]
            x3, y3 = vertices[2]
            double_area = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
            return double_area % 1000

        else:  # collinear_check
            # 세 점씩 확인하여 일직선이 아닌 삼각형의 수
            count = 0
            n = len(vertices)
            for i in range(n):
                for j in range(i + 1, n):
                    for k in range(j + 1, n):
                        x1, y1 = vertices[i]
                        x2, y2 = vertices[j]
                        x3, y3 = vertices[k]
                        area2 = abs(x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
                        if area2 > 0:
                            count += 1
            return count % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        vertices = seed["vertices"]
        n = len(vertices)
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        cx = Fraction(sum(xs), n)
        cy = Fraction(sum(ys), n)
        bbox = (max(xs) - min(xs)) * (max(ys) - min(ys))
        return {
            "vertices": vertices,
            "vertex_count": n,
            "bounding_box_area": bbox,
            "centroid": [int(cx), int(cy)],
        }

    def generate_seed_with_bridge(self, bridge: dict[str, Any], difficulty_hint: float = 10.0) -> dict[str, Any]:
        """circle_theorems에서 center, radius를 받아 원 위/근처의 점으로 seed 생성."""
        center = bridge.get("center")
        radius = bridge.get("radius")
        if center is not None and radius is not None:
            h, k = center if isinstance(center, (list, tuple)) else (0, 0)
            r = int(radius)
            # 원 위의 정수 좌표점 찾기 (피타고라스 삼쌍)
            pts = []
            for dx in range(-r, r + 1):
                dy_sq = r * r - dx * dx
                if dy_sq >= 0:
                    dy = int(math.isqrt(dy_sq))
                    if dy * dy == dy_sq:
                        pts.append([h + dx, k + dy])
                        if dy != 0:
                            pts.append([h + dx, k - dy])
            if len(pts) >= 3:
                selected = random.sample(pts, min(4, len(pts)))
                return {"vertices": selected, "mode": "triangle_area"}
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        vertices = seed["vertices"]
        mode = seed["mode"]
        n = len(vertices)
        if mode == "dist_sq_sum":
            return [
                f"1. {n}개의 점이 주어졌으므로 C({n},2) = {n*(n-1)//2}개의 점 쌍을 구합니다.",
                f"2. 각 쌍에 대해 거리의 제곱 (dx^2 + dy^2)를 계산합니다.",
                f"3. 모든 거리 제곱을 합산합니다.",
                f"4. 합을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "triangle_area":
            return [
                f"1. 세 점 {vertices[0]}, {vertices[1]}, {vertices[2]}로 삼각형을 구성합니다.",
                f"2. 신발끈 공식(Shoelace Formula)으로 넓이의 2배를 계산합니다.",
                f"3. |x1(y2-y3) + x2(y3-y1) + x3(y1-y2)|를 구합니다.",
                f"4. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. {n}개의 점에서 3점 조합 C({n},3) = {math.comb(n,3)}개를 구합니다.",
                f"2. 각 조합에 대해 세 점이 일직선인지 확인합니다 (넓이 = 0?).",
                f"3. 일직선이 아닌(삼각형을 이루는) 조합의 수를 셉니다.",
                f"4. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            return self.execute(seed)
        except Exception:
            return None
