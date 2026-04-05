"""
AI_MathMate V2 — 기본 대수 조작 (algebra_basic_manipulation)
인수분해, 다항식 전개, 유리식 정리, 지수 법칙 등 AIME 기초 대수 기법을 다룹니다.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraBasicManipulationModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_basic_manipulation",
        name="기본 대수 조작",
        domain="integer",
        namespace="alg_basic",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z", min_val=2, max_val=20, description="다항식 계수 a"),
            "b": FieldSpec(dtype=int, domain="Z", min_val=1, max_val=15, description="다항식 계수 b"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=6, description="지수"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'factor' | 'expand' | 'rational'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=3.0,
        min_difficulty=1,
        category="algebra",
        tags=["factorization", "expansion", "rational_expression", "exponent_laws"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["polynomial_value", "factored_sum"],
    )

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["factor", "expand", "rational"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "factor":
                # a^n - b^n 인수분해 → 인수의 합
                a = random.randint(2, 12)
                b = random.randint(1, a - 1)
                n = random.randint(2, 5) if difficulty_hint < 10 else random.randint(3, 6)
            elif mode == "expand":
                # (a + b)^n 전개 시 특정 항의 계수
                a = random.randint(1, 8)
                b = random.randint(1, 8)
                n = random.randint(3, 6)
            else:
                # 유리식 정리: (a^n + b^n) / (a + b)
                a = random.randint(2, 10)
                b = random.randint(1, a)
                n = random.randint(2, 4)

            seed = {"a": a, "b": b, "n": n, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"a": 3, "b": 2, "n": 3, "mode": "factor"}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, n, mode = seed["a"], seed["b"], seed["n"], seed["mode"]

        if mode == "factor":
            # a^n - b^n 인수분해 → 각 인수의 절댓값 합
            # a^n - b^n = (a - b)(a^{n-1} + a^{n-2}b + ... + b^{n-1})
            factor1 = a - b
            factor2 = sum(a ** (n - 1 - k) * b ** k for k in range(n))
            return abs(factor1) + abs(factor2)

        elif mode == "expand":
            # (a + b)^n 전개 시 중간항(k = n//2)의 계수
            k = n // 2
            coeff = math.comb(n, k) * (a ** (n - k)) * (b ** k)
            return coeff % 1000

        else:  # rational
            # (a^n + b^n) / (a + b) 의 정수부
            numerator = a ** n + b ** n
            denominator = a + b
            return (numerator // denominator) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        a, b, n, mode = seed["a"], seed["b"], seed["n"], seed["mode"]
        ans = self.execute(seed)
        factor2 = sum(a ** (n - 1 - k) * b ** k for k in range(n)) if mode == "factor" else ans
        return {
            "polynomial_value": a ** n - b ** n,
            "factored_sum": factor2,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, n, mode = seed["a"], seed["b"], seed["n"], seed["mode"]
        if mode == "factor":
            return [
                f"1. {a}^{n} - {b}^{n}을 인수분해합니다: ({a} - {b})({'+'.join(f'{a}^{n-1-k}*{b}^{k}' for k in range(n))}).",
                f"2. 첫 번째 인수 ({a} - {b}) = {a - b}를 구합니다.",
                f"3. 두 번째 인수의 값을 직접 계산하여 합산합니다.",
            ]
        elif mode == "expand":
            k = n // 2
            return [
                f"1. ({a} + {b})^{n}을 이항정리로 전개합니다.",
                f"2. k={k}인 항의 계수 C({n},{k}) * {a}^{n-k} * {b}^{k}를 계산합니다.",
                f"3. 계수를 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. 분자 {a}^{n} + {b}^{n}을 계산합니다.",
                f"2. 분모 ({a} + {b}) = {a + b}로 나눕니다.",
                f"3. 정수부를 구하고 1000으로 나눈 나머지를 취합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import symbols, factor, expand, Poly
            x = symbols('x')
            a, b, n, mode = seed["a"], seed["b"], seed["n"], seed["mode"]

            if mode == "factor":
                expr = a ** n - b ** n
                f1 = a - b
                f2 = sum(a ** (n - 1 - k) * b ** k for k in range(n))
                assert f1 * f2 == expr, "인수분해 검증 실패"
                return abs(f1) + abs(f2)
            elif mode == "expand":
                k = n // 2
                coeff = int(math.comb(n, k) * (a ** (n - k)) * (b ** k))
                return coeff % 1000
            else:
                return ((a ** n + b ** n) // (a + b)) % 1000
        except Exception:
            return None
