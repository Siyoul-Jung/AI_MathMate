"""
AI_MathMate V2 — 사인/코사인 법칙 (geometry_trigonometry_laws)
AIME 기출 67회. 삼각형에서 사인/코사인 법칙을 적용합니다.
Bridge 이중 수신: triangle_properties에서 변/각, algebra_trigonometry에서 삼각함수 값.
"""
from __future__ import annotations
import random
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryTrigonometryLawsModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_trigonometry_laws",
        name="사인/코사인 법칙",
        domain="integer",
        namespace="geo_trig_law",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+", description="변 a"),
            "b": FieldSpec(dtype=int, domain="Z+", description="변 b"),
            "c": FieldSpec(dtype=int, domain="Z+", description="변 c"),
            "mode": FieldSpec(dtype=str, domain="str", description="'cos_law' | 'sine_law'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=4, daps_contribution=4.0, min_difficulty=5,
        category="geometry",
        tags=["law_of_cosines", "law_of_sines", "trigonometry_geometry", "cosine_rule", "sine_rule"],
        exam_types=["AIME"],
        bridge_input_accepts=["side_a", "side_b", "side_c", "circumradius", "trig_value", "angle_deg"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            a = random.randint(5, 40)
            b = random.randint(5, 40)
            c = random.randint(abs(a - b) + 1, a + b - 1)
            mode = random.choice(["cos_law", "sine_law"])
            seed = {"a": a, "b": b, "c": c, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return {"a": 7, "b": 8, "c": 9, "mode": "cos_law"}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
        if mode == "cos_law":
            # cos(A) = (b^2 + c^2 - a^2) / (2bc) → |분자| + 분모
            num = b * b + c * c - a * a
            den = 2 * b * c
            f = Fraction(num, den)
            return (abs(f.numerator) + f.denominator) % 1000
        else:
            # 사인 법칙: a/sin(A) = 2R → 4R^2 = (abc)^2 / (area_sq * 4)
            # 16R^2 * K^2 = (abc)^2, K^2 = s(s-a)(s-b)(s-c)
            s = Fraction(a + b + c, 2)
            area_sq = s * (s - a) * (s - b) * (s - c)
            if area_sq <= 0:
                return 0
            r_sq = Fraction(a * b * c) ** 2 / (16 * area_sq)
            return (r_sq.numerator + r_sq.denominator) % 1000

    def generate_seed_with_bridge(self, bridge: dict[str, Any], difficulty_hint: float = 10.0) -> dict[str, Any]:
        sa = bridge.get("side_a")
        sb = bridge.get("side_b")
        sc = bridge.get("side_c")
        if sa and sb and sc:
            return {"a": int(sa), "b": int(sb), "c": int(sc), "mode": "cos_law"}
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
        if mode == "cos_law":
            return [
                f"1. 세 변 {a}, {b}, {c}인 삼각형에서 코사인 법칙을 적용합니다.",
                f"2. cos(A) = (b^2+c^2-a^2)/(2bc) = ({b}^2+{c}^2-{a}^2)/(2*{b}*{c}).",
                "3. 기약분수로 정리하여 |분자|+분모를 구합니다.",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. 세 변 {a}, {b}, {c}인 삼각형의 외접원 반지름 R을 구합니다.",
                "2. 사인 법칙: a/sin(A) = 2R, R = abc/(4K).",
                "3. R^2를 분수로 계산합니다.",
                "4. 분자+분모를 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Rational
            a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
            if mode == "cos_law":
                f = Rational(b**2 + c**2 - a**2, 2*b*c)
                return (abs(f.p) + f.q) % 1000
            else:
                s = Rational(a+b+c, 2)
                area_sq = s*(s-a)*(s-b)*(s-c)
                if area_sq <= 0: return 0
                r_sq = Rational(a*b*c)**2 / (16*area_sq)
                return (r_sq.p + r_sq.q) % 1000
        except Exception:
            return None
