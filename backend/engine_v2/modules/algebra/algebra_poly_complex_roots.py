"""
AI_MathMate V2 — 다항식 복소근 (algebra_poly_complex_roots)
정수 계수 다항식의 켤레 복소근 쌍, 근의 절대값 합, 실수부 합을 다룹니다.
기출 빈도: 32회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraPolyComplexRootsModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_poly_complex_roots",
        name="다항식 복소근",
        domain="complex",
        namespace="alg_cplxroot",
        input_schema={
            "real_roots": FieldSpec(dtype=list, domain="Z", description="실수 근 리스트"),
            "complex_pairs": FieldSpec(dtype=list, domain="Z", description="복소근 쌍 [(a, b), ...] → a+bi, a-bi"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'abs_sum' | 'real_part_sum' | 'coeff_sum'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답 (mod 1000)"),
        },
        logic_depth=4,
        daps_contribution=5.0,
        min_difficulty=7,
        category="algebra",
        tags=["polynomial", "complex_roots", "conjugate", "absolute_value", "vieta"],
        exam_types=["AIME"],
        bridge_output_keys=["root_abs_sum", "polynomial_degree"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["abs_sum", "real_part_sum", "coeff_sum"]
        for _ in range(100):
            mode = random.choice(modes)

            # 실수 근 0~2개
            n_real = random.randint(0, 2)
            real_roots = [random.randint(-10, 10) for _ in range(n_real)]

            # 복소근 켤레쌍 1~3개: (a, b) → a+bi, a-bi
            n_cpx = random.randint(1, 3)
            complex_pairs = []
            for _ in range(n_cpx):
                a = random.randint(-8, 8)
                b = random.randint(1, 8)  # b > 0 보장
                complex_pairs.append([a, b])

            seed = {"real_roots": real_roots, "complex_pairs": complex_pairs, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"real_roots": [1], "complex_pairs": [[2, 3]], "mode": "abs_sum"}

    def execute(self, seed: dict[str, Any]) -> int:
        real_roots = seed["real_roots"]
        complex_pairs = seed["complex_pairs"]
        mode = seed["mode"]

        if mode == "abs_sum":
            # 모든 근의 절대값 합의 정수부
            total = 0.0
            for r in real_roots:
                total += abs(r)
            for a, b in complex_pairs:
                # |a+bi| = |a-bi| = sqrt(a^2 + b^2), 쌍이므로 x2
                total += 2 * math.sqrt(a * a + b * b)
            # 분자+분모 패턴 대신 floor 사용
            return int(total) % 1000

        elif mode == "real_part_sum":
            # 모든 근의 실수부 합의 절대값
            total = sum(real_roots) + sum(2 * a for a, b in complex_pairs)
            return abs(total) % 1000

        else:  # coeff_sum
            # 다항식의 계수 절대값 합 (mod 1000)
            # 다항식 = product of (x - r) for real roots * product of (x^2 - 2ax + a^2+b^2) for complex pairs
            # 계수를 직접 곱셈으로 구함
            poly = [1]  # 상수 다항식 1로 시작

            for r in real_roots:
                # (x - r)과 곱
                new_poly = [0] * (len(poly) + 1)
                for i, c in enumerate(poly):
                    new_poly[i] += c          # x 항
                    new_poly[i + 1] -= c * r  # 상수 항
                poly = new_poly

            for a, b in complex_pairs:
                # (x^2 - 2a*x + (a^2 + b^2))과 곱
                quad = [1, -2 * a, a * a + b * b]
                new_poly = [0] * (len(poly) + 2)
                for i, c in enumerate(poly):
                    for j, q in enumerate(quad):
                        new_poly[i + j] += c * q
                poly = new_poly

            return sum(abs(c) for c in poly) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        real_roots = seed["real_roots"]
        complex_pairs = seed["complex_pairs"]
        total = 0.0
        for r in real_roots:
            total += abs(r)
        for a, b in complex_pairs:
            total += 2 * math.sqrt(a * a + b * b)
        degree = len(real_roots) + 2 * len(complex_pairs)
        return {"root_abs_sum": int(total), "polynomial_degree": degree}

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        real_roots = seed["real_roots"]
        complex_pairs = seed["complex_pairs"]
        mode = seed["mode"]
        degree = len(real_roots) + 2 * len(complex_pairs)

        if mode == "abs_sum":
            pairs_str = ", ".join(f"{a}+{b}i / {a}-{b}i" for a, b in complex_pairs)
            return [
                f"1. {degree}차 다항식의 근을 파악합니다. 실근: {real_roots}, 복소근 쌍: {pairs_str}.",
                f"2. 각 실근의 절대값을 구합니다.",
                f"3. 각 복소근 쌍의 절대값 |a+bi| = sqrt(a^2+b^2)를 구하고, 켤레이므로 2배 합산합니다.",
                f"4. 전체 절대값 합의 정수부를 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "real_part_sum":
            return [
                f"1. {degree}차 다항식의 모든 근의 실수부를 구합니다.",
                f"2. 실근의 실수부 합: {sum(real_roots)}.",
                f"3. 복소근 쌍 (a+bi, a-bi)의 실수부 합 = 2a. 총합: {sum(2*a for a,b in complex_pairs)}.",
                f"4. 전체 실수부 합의 절대값을 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. 실근 {real_roots}과 복소근 켤레쌍에서 다항식을 구성합니다.",
                f"2. (x-r) 인수와 (x^2-2ax+a^2+b^2) 인수를 차례로 곱합니다.",
                f"3. 전개된 {degree}차 다항식의 모든 계수를 구합니다.",
                f"4. 계수 절대값의 합을 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import symbols, Poly, Abs, sqrt as sym_sqrt, expand, prod
            x = symbols('x')
            real_roots = seed["real_roots"]
            complex_pairs = seed["complex_pairs"]
            mode = seed["mode"]

            if mode == "abs_sum":
                total = 0.0
                for r in real_roots:
                    total += abs(r)
                for a, b in complex_pairs:
                    total += 2 * float(sym_sqrt(a**2 + b**2))
                return int(total) % 1000

            elif mode == "real_part_sum":
                total = sum(real_roots) + sum(2 * a for a, b in complex_pairs)
                return abs(total) % 1000

            else:  # coeff_sum
                factors = []
                for r in real_roots:
                    factors.append(x - r)
                for a, b in complex_pairs:
                    factors.append(x**2 - 2*a*x + a**2 + b**2)

                poly_expr = expand(prod(factors))
                p = Poly(poly_expr, x)
                return sum(abs(c) for c in p.all_coeffs()) % 1000
        except Exception:
            return None
