"""
AI_MathMate V2 — 이항정리 (algebra_binomial_theorem)
(a+b)^n 전개에서 특정 항의 계수, 이항계수 합, 교대 합 등을 다룹니다.
기출 빈도: 33회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraBinomialTheoremModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_binomial_theorem",
        name="이항정리",
        domain="integer",
        namespace="alg_binom",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z", min_val=1, max_val=10, description="이항식의 첫 번째 항 계수"),
            "b": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="이항식의 두 번째 항 계수"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=20, description="지수"),
            "target_k": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=20, description="구하려는 항의 인덱스"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'coeff' | 'sum_coeffs' | 'alternating'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답 mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=3,
        category="algebra",
        tags=["binomial_theorem", "combinatorics", "coefficient", "expansion", "pascal"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["coefficient_value", "expansion_sum"],
    )

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["coeff", "sum_coeffs", "alternating"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "coeff":
                # (a + b*x)^n 에서 x^target_k 의 계수
                n = random.randint(4, 16) if difficulty_hint < 10 else random.randint(8, 20)
                a = random.randint(1, 6)
                b = random.randint(1, 6) * random.choice([1, -1])
                target_k = random.randint(1, n - 1)
            elif mode == "sum_coeffs":
                # Σ_{k=0}^{n} C(n,k) * a^(n-k) * b^k  = (a+b)^n
                # 특정 mod 연산으로 흥미로운 값 생성
                n = random.randint(5, 18)
                a = random.randint(1, 5)
                b = random.randint(1, 5)
                target_k = 0  # 사용하지 않음
            else:  # alternating
                # Σ_{k=0}^{n} (-1)^k * C(n,k) * a^(n-k) * b^k = (a - b)^n
                n = random.randint(4, 15)
                a = random.randint(2, 8)
                b = random.randint(1, a - 1)  # a > b 보장으로 양수 결과
                target_k = 0

            seed = {"a": a, "b": b, "n": n, "target_k": target_k, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"a": 2, "b": 3, "n": 5, "target_k": 2, "mode": "coeff"}

    def execute(self, seed: dict[str, Any]) -> int:
        a = seed["a"]
        b = seed["b"]
        n = seed["n"]
        target_k = seed["target_k"]
        mode = seed["mode"]

        if mode == "coeff":
            # (a + b*x)^n 에서 x^target_k 의 계수
            # = C(n, target_k) * a^(n - target_k) * b^target_k
            coeff = math.comb(n, target_k) * (a ** (n - target_k)) * (b ** target_k)
            return abs(coeff) % 1000

        elif mode == "sum_coeffs":
            # (a + b)^n mod 1000
            result = (a + b) ** n
            return result % 1000

        else:  # alternating
            # (a - b)^n — 교대 합
            result = (a - b) ** n
            return abs(result) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        a, b, n, target_k, mode = (
            seed["a"], seed["b"], seed["n"], seed["target_k"], seed["mode"],
        )
        ans = self.execute(seed)
        if mode == "coeff":
            coeff = math.comb(n, target_k) * (a ** (n - target_k)) * (b ** target_k)
        else:
            coeff = ans
        return {
            "coefficient_value": coeff,
            "expansion_sum": (a + b) ** n,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, n, target_k, mode = (
            seed["a"], seed["b"], seed["n"], seed["target_k"], seed["mode"],
        )
        if mode == "coeff":
            coeff_val = math.comb(n, target_k)
            return [
                f"1. ({a} + {b}x)^{n}을 이항정리로 전개합니다.",
                f"2. x^{target_k} 항은 C({n},{target_k}) * {a}^{n - target_k} * ({b})^{target_k} 입니다.",
                f"3. C({n},{target_k}) = {coeff_val}을 계산합니다.",
                f"4. 계수의 절댓값을 구하고 1000으로 나눈 나머지를 취합니다.",
            ]
        elif mode == "sum_coeffs":
            return [
                f"1. ({a} + {b})^{n}의 모든 이항계수의 가중 합을 구합니다.",
                f"2. 이항정리에 의해 Σ C({n},k)*{a}^({n}-k)*{b}^k = ({a}+{b})^{n}입니다.",
                f"3. ({a} + {b})^{n} = {a + b}^{n}을 직접 계산합니다.",
                f"4. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. ({a} - {b})^{n}의 교대 합을 구합니다.",
                f"2. 이항정리에 의해 Σ (-1)^k * C({n},k)*{a}^({n}-k)*{b}^k = ({a}-{b})^{n}입니다.",
                f"3. ({a} - {b})^{n} = {a - b}^{n}을 직접 계산합니다.",
                f"4. 절댓값을 취하고 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import binomial, Symbol, Abs
            a, b, n, target_k, mode = (
                seed["a"], seed["b"], seed["n"], seed["target_k"], seed["mode"],
            )

            if mode == "coeff":
                coeff = int(binomial(n, target_k)) * (a ** (n - target_k)) * (b ** target_k)
                return abs(coeff) % 1000
            elif mode == "sum_coeffs":
                return ((a + b) ** n) % 1000
            else:
                return abs((a - b) ** n) % 1000
        except Exception:
            return None
