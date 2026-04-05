"""
AI_MathMate V2 — 다각형 성질 (geometry_polygons)
정다각형의 내각, 대각선, 넓이 및 비정규 다각형의 기하학적 성질을 다룹니다.
"""
from __future__ import annotations
import random
import math
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryPolygonsModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_polygons",
        name="다각형 성질",
        domain="integer",
        namespace="geo_polygon",
        input_schema={
            "n_sides": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=30, description="다각형 변의 수"),
            "side_length": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=50, description="한 변의 길이"),
            "mode": FieldSpec(dtype=str, domain="str", description="'diagonal_count' | 'area_regular' | 'angle_sum'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=3.5,
        min_difficulty=1,
        category="geometry",
        tags=["polygon", "regular_polygon", "diagonal", "interior_angle", "area"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["n_sides", "diagonal_count", "interior_angle"],
    )

    def generate_seed(self, difficulty_hint: float = 7.0) -> dict[str, Any]:
        modes = ["diagonal_count", "area_regular", "angle_sum"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "diagonal_count":
                # 대각선 조합 문제: n(n-3)/2 + 추가 교차점 관련
                n_sides = random.randint(5, 25) if difficulty_hint < 10 else random.randint(10, 30)
                side_length = 1  # 불필요하지만 스키마 일관성
            elif mode == "area_regular":
                # 정n각형 넓이: (n * s^2) / (4 * tan(pi/n)) → 정수 근사
                n_sides = random.choice([3, 4, 6, 8, 12])  # tan(pi/n)이 깔끔한 경우
                side_length = random.randint(2, 30)
            else:
                # 내각 합 응용: 볼록 다각형에서 특정 꼭짓점의 외각 합 관련
                n_sides = random.randint(5, 20)
                side_length = 1

            seed = {"n_sides": n_sides, "side_length": side_length, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n_sides": 6, "side_length": 10, "mode": "area_regular"}

    def execute(self, seed: dict[str, Any]) -> int:
        n, s, mode = seed["n_sides"], seed["side_length"], seed["mode"]

        if mode == "diagonal_count":
            # 대각선 수 n(n-3)/2 + 내부 교차점 수 C(n,4) 의 합
            diagonals = n * (n - 3) // 2
            intersections = math.comb(n, 4)  # 볼록 n각형 내 대각선 교차점
            return (diagonals + intersections) % 1000

        elif mode == "area_regular":
            # 정n각형 넓이 = (n * s^2) / (4 * tan(pi/n))
            # 넓이의 floor를 1000으로 나눈 나머지
            area = (n * s * s) / (4 * math.tan(math.pi / n))
            return int(area) % 1000

        else:  # angle_sum
            # 내각 합 (n-2)*180 + 대각선 수 n(n-3)/2 의 합
            angle_sum = (n - 2) * 180
            diagonals = n * (n - 3) // 2
            return (angle_sum + diagonals) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        n = seed["n_sides"]
        return {
            "n_sides": n,
            "diagonal_count": n * (n - 3) // 2,
            "interior_angle": Fraction((n - 2) * 180, n),
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, s, mode = seed["n_sides"], seed["side_length"], seed["mode"]
        if mode == "diagonal_count":
            return [
                f"1. {n}각형의 대각선 수 공식 n(n-3)/2 = {n}({n}-3)/2 = {n*(n-3)//2}개를 구합니다.",
                f"2. 볼록 {n}각형에서 대각선의 내부 교차점 수는 C({n},4) = {math.comb(n,4)}개입니다.",
                f"3. 대각선 수와 교차점 수의 합을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "area_regular":
            return [
                f"1. 정{n}각형의 넓이 공식 A = n*s^2 / (4*tan(pi/n))을 적용합니다.",
                f"2. s = {s}, n = {n}을 대입하여 넓이를 계산합니다.",
                f"3. 넓이의 정수부를 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. {n}각형의 내각의 합 (n-2)*180 = {(n-2)*180}도를 구합니다.",
                f"2. 대각선의 수 {n}({n}-3)/2 = {n*(n-3)//2}개를 구합니다.",
                f"3. 내각의 합과 대각선 수의 합을 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import pi, tan, floor, binomial, Rational
            n, s, mode = seed["n_sides"], seed["side_length"], seed["mode"]

            if mode == "diagonal_count":
                diag = n * (n - 3) // 2
                inter = int(binomial(n, 4))
                return (diag + inter) % 1000
            elif mode == "area_regular":
                area = Rational(n * s * s, 4) / tan(pi / n)
                return int(float(area)) % 1000
            else:
                return ((n - 2) * 180 + n * (n - 3) // 2) % 1000
        except Exception:
            return None
