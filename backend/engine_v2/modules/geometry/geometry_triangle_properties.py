"""
AI_MathMate V2 — 삼각형 성질 (geometry_triangle_properties)
AIME 기출 116회. 변, 각, 외접원/내접원 반지름 관계를 다룹니다.
Bridge: coordinate_analytic에서 vertices 수신, trigonometry_laws에 변/각 전달.
"""
from __future__ import annotations
import random
import math
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryTrianglePropertiesModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_triangle_properties",
        name="삼각형 성질",
        domain="integer",
        namespace="geo_tri",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+", description="변 a"),
            "b": FieldSpec(dtype=int, domain="Z+", description="변 b"),
            "c": FieldSpec(dtype=int, domain="Z+", description="변 c"),
            "mode": FieldSpec(dtype=str, domain="str", description="'circumradius' | 'inradius' | 'median'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=5,
        category="geometry",
        tags=["triangle", "circumradius", "inradius", "median", "heron", "angle_chasing", "ceva"],
        exam_types=["AIME"],
        bridge_output_keys=["side_a", "side_b", "side_c", "circumradius", "area"],
        bridge_input_accepts=["vertices"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["circumradius", "inradius", "median"]
        for _ in range(100):
            mode = random.choice(modes)
            a = random.randint(5, 50)
            b = random.randint(5, 50)
            c = random.randint(abs(a - b) + 1, a + b - 1)
            seed = {"a": a, "b": b, "c": c, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return {"a": 13, "b": 14, "c": 15, "mode": "circumradius"}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
        s = Fraction(a + b + c, 2)
        area_sq = s * (s - a) * (s - b) * (s - c)
        if area_sq <= 0:
            return 0

        if mode == "circumradius":
            # R = abc / (4K), 4K = sqrt(16*area_sq)
            # R^2 = (abc)^2 / (16 * area_sq) -> (abc)^2 / (16 * s(s-a)(s-b)(s-c))
            # 분자+분모 반환
            num = Fraction(a * b * c) ** 2
            den = 16 * area_sq
            r_sq = num / den
            return (r_sq.numerator + r_sq.denominator) % 1000

        elif mode == "inradius":
            # r = K / s, r^2 = area_sq / s^2
            r_sq = area_sq / (s * s)
            return (r_sq.numerator + r_sq.denominator) % 1000

        else:  # median
            # 변 a의 중선 길이^2 = (2b^2 + 2c^2 - a^2) / 4
            m_sq = Fraction(2 * b * b + 2 * c * c - a * a, 4)
            if m_sq <= 0:
                return 0
            return (m_sq.numerator + m_sq.denominator) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        a, b, c = seed["a"], seed["b"], seed["c"]
        s = Fraction(a + b + c, 2)
        area_sq = s * (s - a) * (s - b) * (s - c)
        r_sq_num = (a * b * c) ** 2
        r_sq_den = 16 * int(area_sq) if area_sq > 0 else 1
        return {
            "side_a": a,
            "side_b": b,
            "side_c": c,
            "circumradius": int(Fraction(r_sq_num, r_sq_den)),
            "area": int(area_sq),
        }

    def generate_seed_with_bridge(self, bridge: dict[str, Any], difficulty_hint: float = 10.0) -> dict[str, Any]:
        vertices = bridge.get("vertices")
        if vertices and len(vertices) >= 3:
            p1, p2, p3 = vertices[0], vertices[1], vertices[2]
            a_sq = (p2[0]-p3[0])**2 + (p2[1]-p3[1])**2
            b_sq = (p1[0]-p3[0])**2 + (p1[1]-p3[1])**2
            c_sq = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
            a = int(math.isqrt(a_sq)) if math.isqrt(a_sq)**2 == a_sq else int(math.sqrt(a_sq) + 0.5)
            b = int(math.isqrt(b_sq)) if math.isqrt(b_sq)**2 == b_sq else int(math.sqrt(b_sq) + 0.5)
            c = int(math.isqrt(c_sq)) if math.isqrt(c_sq)**2 == c_sq else int(math.sqrt(c_sq) + 0.5)
            if a > 0 and b > 0 and c > 0 and a + b > c and b + c > a and a + c > b:
                return {"a": a, "b": b, "c": c, "mode": "circumradius"}
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
        s_val = (a + b + c) / 2
        if mode == "circumradius":
            return [
                f"1. 세 변 {a}, {b}, {c}인 삼각형의 반둘레 s = {s_val}.",
                f"2. 헤론 공식으로 넓이 K를 구합니다: K^2 = s(s-a)(s-b)(s-c).",
                f"3. 외접원 반지름 R = abc/(4K), R^2 = (abc)^2/(16K^2) 분수로 계산.",
                "4. 분자+분모를 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "inradius":
            return [
                f"1. 세 변 {a}, {b}, {c}의 반둘레 s = {s_val}.",
                "2. 헤론 공식으로 넓이의 제곱 K^2를 구합니다.",
                "3. 내접원 반지름 r = K/s, r^2 = K^2/s^2 분수로 계산.",
                "4. 분자+분모를 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. 세 변 {a}, {b}, {c}인 삼각형에서 변 a의 중선을 구합니다.",
                f"2. 중선 공식: m_a^2 = (2b^2 + 2c^2 - a^2) / 4.",
                f"3. m_a^2 = (2*{b}^2 + 2*{c}^2 - {a}^2) / 4를 분수로 계산.",
                "4. 분자+분모를 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Rational, sqrt
            a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
            s = Rational(a + b + c, 2)
            area_sq = s * (s - a) * (s - b) * (s - c)
            if area_sq <= 0:
                return 0
            if mode == "circumradius":
                r_sq = Rational(a * b * c) ** 2 / (16 * area_sq)
                return int((r_sq.p + r_sq.q) % 1000)
            elif mode == "inradius":
                r_sq = area_sq / (s * s)
                return int((r_sq.p + r_sq.q) % 1000)
            else:
                m_sq = Rational(2 * b**2 + 2 * c**2 - a**2, 4)
                return int((m_sq.p + m_sq.q) % 1000)
        except Exception:
            return None
