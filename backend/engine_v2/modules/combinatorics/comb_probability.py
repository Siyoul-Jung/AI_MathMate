"""
AI_MathMate V2 -- comb_probability (확률 / Probability)
기본 확률 계산: 유리한 경우 / 전체 경우 기약분수의 분자+분모.
기출 113회 (AIME). Bridge 타겟 모듈.
"""
from __future__ import annotations
import random
import math
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombProbabilityModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_probability",
        name="확률 (Probability)",
        domain="integer",
        namespace="comb_prob",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=20, description="전체 원소 수"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=10, description="선택/조건 원소 수"),
            "mode": FieldSpec(dtype=str, domain="str", description="'draw' | 'dice' | 'birthday'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="p+q 기약분수"),
        },
        logic_depth=4,
        daps_contribution=3.5,
        min_difficulty=4,
        category="combinatorics",
        tags=["probability", "combinatorial", "fraction", "counting"],
        exam_types=["AIME", "AMC"],
        bridge_input_accepts=["total_count", "n_elements"],
    )

    def generate_seed(self, difficulty_hint: float = 7.0) -> dict[str, Any]:
        modes = ["draw", "dice", "birthday"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "draw":
                n = random.randint(5, 20)
                k = random.randint(2, min(n - 1, 8))
            elif mode == "dice":
                n = random.randint(3, 8)  # 주사위 수
                k = random.randint(1, 6)  # 목표 합 범위 파라미터
            else:  # birthday
                n = random.randint(3, 12)
                k = random.randint(2, min(n, 5))

            seed = {"n": n, "k": k, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n": 10, "k": 3, "mode": "draw"}

    def execute(self, seed: dict[str, Any]) -> int:
        n, k, mode = seed["n"], seed["k"], seed["mode"]

        if mode == "draw":
            # n개 중 k개를 뽑을 때, 특정 2개가 모두 포함될 확률
            # = C(n-2, k-2) / C(n, k)
            if k < 2 or n < k:
                return 1
            favorable = math.comb(n - 2, k - 2)
            total = math.comb(n, k)
            prob = Fraction(favorable, total)
            return int(prob.numerator + prob.denominator)

        elif mode == "dice":
            # n개 주사위를 던져 합이 k 이상일 확률의 여사건
            # P(합 <= k*n/2) 계산 (단순화: 최소합 n, 최대합 6n)
            # 대신: n개 주사위 모두 같은 값이 나올 확률
            # = 6 / 6^n = 1/6^(n-1)
            prob = Fraction(1, 6 ** (n - 1))
            return int(prob.numerator + prob.denominator)

        else:  # birthday
            # n명 중 생일이 모두 다를 확률 (k=365 대신 k일 기준)
            # P = k!/((k-n)! * k^n) -- k가 너무 크면 간소화
            # AIME 스타일: n명, k종류 중 모두 다른 종류를 뽑을 확률
            if n > k:
                return 1  # 비둘기집: 반드시 중복
            # P(모두 다름) = k * (k-1) * ... * (k-n+1) / k^n
            numerator = 1
            for i in range(n):
                numerator *= (k - i)
            denominator = k ** n
            prob = Fraction(numerator, denominator)
            return int(prob.numerator + prob.denominator)

    def generate_seed_with_bridge(
        self, bridge: dict[str, Any], difficulty_hint: float = 7.0
    ) -> dict[str, Any]:
        """Bridge 수신: total_count, n_elements를 활용합니다."""
        total_count = bridge.get("total_count")
        n_elements = bridge.get("n_elements")

        if total_count is not None and n_elements is not None:
            n = int(n_elements)
            k = max(2, min(n - 1, int(n_elements) // 2))
            seed = {"n": n, "k": k, "mode": "draw"}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, k, mode = seed["n"], seed["k"], seed["mode"]

        if mode == "draw":
            return [
                f"1. {n}개 원소에서 {k}개를 비복원 추출합니다.",
                f"2. 특정 2개가 모두 포함되는 유리한 경우: C({n-2},{k-2}).",
                f"3. 전체 경우: C({n},{k}).",
                f"4. 확률 = C({n-2},{k-2})/C({n},{k})을 기약분수로 정리하고 p+q를 구합니다.",
            ]
        elif mode == "dice":
            return [
                f"1. {n}개의 공정한 주사위를 던집니다.",
                f"2. 모든 주사위가 같은 값을 보일 확률을 구합니다.",
                f"3. P = 6/6^{n} = 1/6^{n-1}.",
                f"4. 기약분수에서 p+q를 구합니다.",
            ]
        else:
            return [
                f"1. {k}종류 중에서 {n}명이 각각 하나씩 고를 때 모두 다를 확률을 구합니다.",
                f"2. P = {k}!/(({k}-{n})! x {k}^{n}).",
                f"3. 분자: {k} x {k-1} x ... x {k-n+1}, 분모: {k}^{n}.",
                f"4. 기약분수로 정리하고 p+q를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Rational, binomial, Integer, factorial
            n, k, mode = seed["n"], seed["k"], seed["mode"]

            if mode == "draw":
                if k < 2 or n < k:
                    return 1
                prob = Rational(int(binomial(n - 2, k - 2)), int(binomial(n, k)))
                return int(prob.p + prob.q)
            elif mode == "dice":
                prob = Rational(1, 6 ** (n - 1))
                return int(prob.p + prob.q)
            else:
                if n > k:
                    return 1
                num = int(factorial(k) // factorial(k - n))
                den = k ** n
                prob = Rational(num, den)
                return int(prob.p + prob.q)
        except Exception:
            return None
