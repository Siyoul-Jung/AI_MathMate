"""
AI_MathMate V2 — 각의 이등분선 정리 (geometry_angle_bisector_theorem)
AIME 기출 27회. 이등분선이 대변을 나누는 비, 이등분선 길이를 다룹니다.
"""
from __future__ import annotations
import random
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryAngleBisectorTheoremModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_angle_bisector_theorem", name="각의 이등분선 정리",
        domain="integer", namespace="geo_bisector",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+", description="변 a (BC)"),
            "b": FieldSpec(dtype=int, domain="Z+", description="변 b (AC)"),
            "c": FieldSpec(dtype=int, domain="Z+", description="변 c (AB)"),
            "mode": FieldSpec(dtype=str, domain="str", description="'bisector_length_sq' | 'ratio'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=4, daps_contribution=4.0, min_difficulty=6, category="geometry",
        tags=["angle_bisector", "bisector_theorem", "stewart"], exam_types=["AIME"],
        bridge_input_accepts=["side_a", "side_b", "side_c"],
        bridge_output_keys=["side_a", "side_b", "side_c", "bisector_ratio_num", "bisector_ratio_den"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            a = random.randint(5, 40)
            b = random.randint(5, 40)
            c = random.randint(abs(a - b) + 1, a + b - 1)
            mode = random.choice(["bisector_length_sq", "ratio"])
            seed = {"a": a, "b": b, "c": c, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"a": 7, "b": 8, "c": 9, "mode": "bisector_length_sq"}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
        if mode == "ratio":
            # 꼭짓점 A의 이등분선이 BC를 BD:DC = c:b로 나눔
            f = Fraction(c, b)
            return (f.numerator + f.denominator) % 1000
        else:
            # 스튜어트 정리로 이등분선 길이^2
            # t_a^2 = bc[(b+c)^2 - a^2] / (b+c)^2
            num = b * c * ((b + c) ** 2 - a * a)
            den = (b + c) ** 2
            f = Fraction(num, den)
            return (abs(f.numerator) + f.denominator) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, c = seed["a"], seed["b"], seed["c"]
        return [
            f"1. 삼각형 세 변 a={a}, b={b}, c={c}.",
            "2. 각의 이등분선 정리: BD/DC = AB/AC = c/b.",
            "3. 스튜어트 정리로 이등분선 길이를 구합니다.",
            "4. 분자+분모를 1000으로 나눈 나머지.",
        ]
    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        from fractions import Fraction
        f = Fraction(seed["c"], seed["b"])
        return {"side_a": seed["a"], "side_b": seed["b"], "side_c": seed["c"],
                "bisector_ratio_num": f.numerator, "bisector_ratio_den": f.denominator}

    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float = 10.0) -> dict[str, Any]:
        sa = bridge.get("side_a")
        sb = bridge.get("side_b")
        sc = bridge.get("side_c")
        if sa and sb and sc:
            a, b, c = int(sa), int(sb), int(sc)
            if a + b > c and b + c > a and a + c > b and a > 0 and b > 0 and c > 0:
                seed = {"a": a, "b": b, "c": c, "mode": "bisector_length_sq"}
                ans = self.execute(seed)
                if 0 < ans <= 999:
                    return seed
        return self.generate_seed(difficulty_hint)

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Rational
            a, b, c = seed["a"], seed["b"], seed["c"]
            if seed["mode"] == "ratio":
                f = Rational(c, b)
                return (abs(f.p) + f.q) % 1000
            else:
                f = Rational(b*c*((b+c)**2 - a*a), (b+c)**2)
                return (abs(f.p) + f.q) % 1000
        except: return None
