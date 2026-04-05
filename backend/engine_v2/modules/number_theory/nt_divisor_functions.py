"""
AI_MathMate V2 — 약수 함수 (nt_divisor_functions)
sigma_k(n) (약수 거듭제곱 합), tau(n) (약수 개수), 완전수/부족수/과잉수 판별.
AIME 기출 36회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtDivisorFunctionsModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_divisor_functions",
        name="약수 함수",
        domain="integer",
        namespace="nt_divfunc",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=50000, description="대상 정수"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=3, description="sigma_k의 지수 k"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'sigma_k' | 'tau' | 'perfect_count' | 'abundant_count'"),
            "upper": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=5000,
                               description="범위 상한 (perfect_count, abundant_count 모드)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=4.0,
        min_difficulty=4,
        category="number_theory",
        tags=["sigma_function", "tau_function", "divisor_sum", "perfect_number", "abundant_number"],
        exam_types=["AIME", "AMC"],
    )

    @staticmethod
    def _factorize(n: int) -> dict[int, int]:
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
    def _sigma(n: int, k: int) -> int:
        """sigma_k(n) = 약수 d의 d^k 합."""
        if k == 0:
            # tau(n)
            factors = NtDivisorFunctionsModule._factorize(n)
            result = 1
            for e in factors.values():
                result *= (e + 1)
            return result
        factors = NtDivisorFunctionsModule._factorize(n)
        result = 1
        for p, e in factors.items():
            # (p^{k(e+1)} - 1) / (p^k - 1)
            pk = pow(p, k)
            result *= (pow(pk, e + 1) - 1) // (pk - 1)
        return result

    @staticmethod
    def _is_abundant(n: int) -> bool:
        """진약수의 합 > n인지 (과잉수)."""
        return NtDivisorFunctionsModule._sigma(n, 1) - n > n

    @staticmethod
    def _is_perfect(n: int) -> bool:
        """진약수의 합 == n인지 (완전수)."""
        return NtDivisorFunctionsModule._sigma(n, 1) - n == n

    def generate_seed(self, difficulty_hint: float = 7.0) -> dict[str, Any]:
        modes = ["sigma_k", "tau", "perfect_count", "abundant_count"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode in ("sigma_k", "tau"):
                n = random.randint(100, 20000) if difficulty_hint < 10 else random.randint(1000, 50000)
                k = random.randint(0, 2) if mode == "sigma_k" else 0
                upper = n  # unused
            else:
                n = 1  # unused
                k = 1
                upper = random.randint(50, 2000) if difficulty_hint < 10 else random.randint(500, 5000)

            seed = {"n": n, "k": k, "mode": mode, "upper": upper}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n": 360, "k": 1, "mode": "sigma_k", "upper": 100}

    def execute(self, seed: dict[str, Any]) -> int:
        n, k, mode = seed["n"], seed["k"], seed["mode"]

        if mode == "sigma_k":
            return self._sigma(n, k) % 1000

        elif mode == "tau":
            return self._sigma(n, 0) % 1000

        elif mode == "perfect_count":
            upper = seed["upper"]
            count = sum(1 for i in range(2, upper + 1) if self._is_perfect(i))
            return count % 1000

        else:  # abundant_count
            upper = seed["upper"]
            count = sum(1 for i in range(2, upper + 1) if self._is_abundant(i))
            return count % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, k, mode = seed["n"], seed["k"], seed["mode"]

        if mode == "sigma_k":
            factors = self._factorize(n)
            fs = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factors.items()))
            val = self._sigma(n, k)
            return [
                f"1. {n}을 소인수분해합니다: {n} = {fs}.",
                f"2. σ_{k}({n}) = Π((p^{{{k}(e+1)}} - 1)/(p^{k} - 1))을 각 소인수에 적용합니다.",
                f"3. σ_{k}({n}) = {val}, mod 1000 = {val % 1000}.",
            ]
        elif mode == "tau":
            factors = self._factorize(n)
            fs = " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(factors.items()))
            val = self._sigma(n, 0)
            return [
                f"1. {n}을 소인수분해합니다: {n} = {fs}.",
                f"2. τ({n}) = Π(e_i + 1) = {' × '.join(str(e + 1) for _, e in sorted(factors.items()))}.",
                f"3. τ({n}) = {val}.",
            ]
        elif mode == "perfect_count":
            upper = seed["upper"]
            count = sum(1 for i in range(2, upper + 1) if self._is_perfect(i))
            return [
                f"1. 2부터 {upper}까지 각 수 n에 대해 σ(n) - n = n인지 확인합니다.",
                f"2. 완전수의 성질을 이용하여 후보를 좁힙니다 (2^(p-1)(2^p - 1) 형태).",
                f"3. 범위 내 완전수의 개수: {count}개.",
            ]
        else:
            upper = seed["upper"]
            count = sum(1 for i in range(2, upper + 1) if self._is_abundant(i))
            return [
                f"1. 2부터 {upper}까지 각 수 n에 대해 σ(n) - n > n인지 확인합니다.",
                f"2. 과잉수(진약수 합 > 자기 자신)의 개수를 셉니다.",
                f"3. 범위 내 과잉수의 개수: {count}개, mod 1000 = {count % 1000}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import divisor_sigma
            n, k, mode = seed["n"], seed["k"], seed["mode"]

            if mode == "sigma_k":
                return int(divisor_sigma(n, k)) % 1000
            elif mode == "tau":
                return int(divisor_sigma(n, 0)) % 1000
            elif mode == "perfect_count":
                upper = seed["upper"]
                count = sum(1 for i in range(2, upper + 1) if int(divisor_sigma(i, 1)) == 2 * i)
                return count % 1000
            else:
                upper = seed["upper"]
                count = sum(1 for i in range(2, upper + 1) if int(divisor_sigma(i, 1)) > 2 * i)
                return count % 1000
        except Exception:
            return None
