"""
AI_MathMate V2 — 약수와 소수 (nt_divisibility_and_primes)
소인수분해, 약수 개수, 약수 합, GCD/LCM 기반 문제. AIME 기출 75회.
Bridge 소스 모듈: prime_factors, divisor_count, gcd_value, lcm_value 출력.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtDivisibilityAndPrimesModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_divisibility_and_primes",
        name="약수와 소수",
        domain="integer",
        namespace="nt_divprime",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=100000, description="대상 정수"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'divisor_count' | 'divisor_sum' | 'prime_factorization_sum' | 'largest_prime_factor'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=3.5,
        min_difficulty=3,
        category="number_theory",
        tags=["prime_factorization", "divisor_count", "divisor_sum", "prime_factor", "fundamental_theorem"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["prime_factors", "divisor_count", "gcd_value", "lcm_value"],
    )

    @staticmethod
    def _factorize(n: int) -> dict[int, int]:
        """n의 소인수분해를 {소수: 지수} 딕셔너리로 반환."""
        factors: dict[int, int] = {}
        d = 2
        while d * d <= n:
            while n % d == 0:
                factors[d] = factors.get(d, 0) + 1
                n //= d
            d += 1
        if n > 1:
            factors[n] = factors.get(n, 0) + 1
        return factors

    @staticmethod
    def _divisor_count(factors: dict[int, int]) -> int:
        """약수의 개수: Π(e_i + 1)."""
        result = 1
        for e in factors.values():
            result *= (e + 1)
        return result

    @staticmethod
    def _divisor_sum(factors: dict[int, int]) -> int:
        """약수의 합: Π((p^{e+1} - 1) / (p - 1))."""
        result = 1
        for p, e in factors.items():
            result *= (pow(p, e + 1) - 1) // (p - 1)
        return result

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["divisor_count", "divisor_sum", "prime_factorization_sum", "largest_prime_factor"]
        for _ in range(100):
            mode = random.choice(modes)
            if difficulty_hint < 8:
                n = random.randint(100, 10000)
            elif difficulty_hint < 12:
                n = random.randint(1000, 50000)
            else:
                n = random.randint(5000, 100000)

            seed = {"n": n, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n": 360, "mode": "divisor_count"}

    def execute(self, seed: dict[str, Any]) -> int:
        n, mode = seed["n"], seed["mode"]
        factors = self._factorize(n)

        if mode == "divisor_count":
            return self._divisor_count(factors) % 1000

        elif mode == "divisor_sum":
            return self._divisor_sum(factors) % 1000

        elif mode == "prime_factorization_sum":
            # 소인수 × 지수의 합: Σ(p_i × e_i)
            total = sum(p * e for p, e in factors.items())
            return total % 1000

        else:  # largest_prime_factor
            return max(factors.keys()) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        n = seed["n"]
        factors = self._factorize(n)
        dc = self._divisor_count(factors)
        # GCD/LCM은 n 자체와 관련된 값을 전달
        return {
            "prime_factors": factors,
            "divisor_count": dc,
            "gcd_value": n,
            "lcm_value": n,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, mode = seed["n"], seed["mode"]
        factors = self._factorize(n)
        factorization_str = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factors.items()))

        steps = [
            f"1. {n}을 소인수분해합니다: {n} = {factorization_str}.",
        ]
        if mode == "divisor_count":
            parts = " × ".join(f"({e}+1)" for _, e in sorted(factors.items()))
            dc = self._divisor_count(factors)
            steps.append(f"2. 약수의 개수 = {parts} = {dc}.")
            steps.append(f"3. {dc} mod 1000 = {dc % 1000}.")
        elif mode == "divisor_sum":
            ds = self._divisor_sum(factors)
            steps.append(f"2. 약수의 합 공식 Π((p^(e+1)-1)/(p-1))을 적용합니다.")
            steps.append(f"3. 약수의 합 = {ds}, mod 1000 = {ds % 1000}.")
        elif mode == "prime_factorization_sum":
            total = sum(p * e for p, e in factors.items())
            steps.append(f"2. 각 소인수 × 지수의 합을 구합니다: {' + '.join(f'{p}×{e}' for p, e in sorted(factors.items()))} = {total}.")
            steps.append(f"3. {total} mod 1000 = {total % 1000}.")
        else:
            lp = max(factors.keys())
            steps.append(f"2. 가장 큰 소인수를 찾습니다: {lp}.")
            steps.append(f"3. {lp} mod 1000 = {lp % 1000}.")
        return steps

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import factorint, divisor_count as sym_dc, divisor_sigma
            n, mode = seed["n"], seed["mode"]
            factors = factorint(n)

            if mode == "divisor_count":
                return int(sym_dc(n)) % 1000
            elif mode == "divisor_sum":
                return int(divisor_sigma(n, 1)) % 1000
            elif mode == "prime_factorization_sum":
                total = sum(p * e for p, e in factors.items())
                return total % 1000
            else:
                return max(factors.keys()) % 1000
        except Exception:
            return None
