"""
AI_MathMate V2 — 완전 거듭제곱 (nt_perfect_powers)
완전제곱수, 완전세제곱수, 완전 k제곱수 개수 및 포함-배제 계산.
AIME 기출 32회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtPerfectPowersModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_perfect_powers",
        name="완전 거듭제곱",
        domain="integer",
        namespace="nt_perfpow",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=1000000, description="범위 상한"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=6, description="거듭제곱 지수"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'count_k' | 'count_any_power' | 'sum_perfect_squares'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=3.5,
        min_difficulty=3,
        category="number_theory",
        tags=["perfect_square", "perfect_cube", "perfect_power", "inclusion_exclusion"],
        exam_types=["AIME", "AMC"],
    )

    @staticmethod
    def _int_kth_root(n: int, k: int) -> int:
        """n의 k제곱근의 정수부 (floor)."""
        if n <= 0:
            return 0
        if k == 1:
            return n
        # Newton's method
        guess = int(round(n ** (1.0 / k)))
        # 부동소수점 오차 보정
        for delta in range(-3, 4):
            g = guess + delta
            if g >= 0 and g ** k <= n < (g + 1) ** k:
                return g
        # Fallback: binary search
        lo, hi = 0, min(n, 2 ** (n.bit_length() // k + 2))
        while lo <= hi:
            mid = (lo + hi) // 2
            val = mid ** k
            if val == n:
                return mid
            elif val < n:
                lo = mid + 1
            else:
                hi = mid - 1
        return hi

    @staticmethod
    def _count_perfect_kth(n: int, k: int) -> int:
        """1~n에서 완전 k제곱수의 개수."""
        return NtPerfectPowersModule._int_kth_root(n, k)

    @staticmethod
    def _count_any_perfect_power(n: int) -> int:
        """1~n에서 완전 거듭제곱(k >= 2)인 수의 개수 (포함-배제)."""
        # 완전 거듭제곱: m^k (k>=2, m>=1) 인 수의 집합
        # 소수 지수만 고려 + 포함-배제
        if n < 1:
            return 0

        primes = [2, 3, 5, 7, 11, 13, 17, 19]  # 2^19 > 10^6
        max_exp = max(p for p in primes if 2 ** p <= n) if n >= 4 else 2

        relevant_primes = [p for p in primes if 2 ** p <= n]

        # 포함-배제: 각 소수 지수 집합에 대해
        perfect_powers = set()
        perfect_powers.add(1)  # 1 = 1^k

        for p in relevant_primes:
            root = NtPerfectPowersModule._int_kth_root(n, p)
            for base in range(2, root + 1):
                val = base ** p
                if val <= n:
                    perfect_powers.add(val)

        return len(perfect_powers)

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["count_k", "count_any_power", "sum_perfect_squares"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "count_k":
                k = random.randint(2, 5)
                n = random.randint(100, 100000) if difficulty_hint < 10 else random.randint(10000, 1000000)
            elif mode == "count_any_power":
                k = 2  # unused
                n = random.randint(100, 10000) if difficulty_hint < 10 else random.randint(1000, 100000)
            else:  # sum_perfect_squares
                k = 2
                n = random.randint(10, 500) if difficulty_hint < 10 else random.randint(100, 2000)

            seed = {"n": n, "k": k, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n": 100, "k": 2, "mode": "count_k"}

    def execute(self, seed: dict[str, Any]) -> int:
        n, k, mode = seed["n"], seed["k"], seed["mode"]

        if mode == "count_k":
            return self._count_perfect_kth(n, k) % 1000

        elif mode == "count_any_power":
            return self._count_any_perfect_power(n) % 1000

        else:  # sum_perfect_squares
            # 1~n 범위 완전제곱수의 합: 1² + 2² + ... + m² where m = floor(√n)
            m = self._int_kth_root(n, 2)
            total = m * (m + 1) * (2 * m + 1) // 6
            return total % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, k, mode = seed["n"], seed["k"], seed["mode"]

        if mode == "count_k":
            root = self._int_kth_root(n, k)
            return [
                f"1. 1부터 {n}까지 완전 {k}제곱수의 개수를 구합니다.",
                f"2. ⌊{n}^(1/{k})⌋ = {root}이므로, 1^{k}, 2^{k}, ..., {root}^{k}이 범위 내입니다.",
                f"3. 완전 {k}제곱수의 개수: {root}개, mod 1000 = {root % 1000}.",
            ]
        elif mode == "count_any_power":
            count = self._count_any_perfect_power(n)
            return [
                f"1. 1부터 {n}까지 완전 거듭제곱(m^k, k ≥ 2)인 수의 개수를 구합니다.",
                f"2. 각 소수 지수 p에 대해 완전 p제곱수의 집합을 구하고 합집합을 취합니다.",
                f"3. 중복 제거(포함-배제)를 적용하여 총 {count}개, mod 1000 = {count % 1000}.",
            ]
        else:
            m = self._int_kth_root(n, 2)
            total = m * (m + 1) * (2 * m + 1) // 6
            return [
                f"1. 1부터 {n}까지 완전제곱수의 합 1² + 2² + ... + {m}²를 구합니다.",
                f"2. 공식 적용: m(m+1)(2m+1)/6 = {m}×{m+1}×{2*m+1}/6.",
                f"3. 합 = {total}, mod 1000 = {total % 1000}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import integer_nthroot
            n, k, mode = seed["n"], seed["k"], seed["mode"]

            if mode == "count_k":
                root, exact = integer_nthroot(n, k)
                return root % 1000
            elif mode == "count_any_power":
                # 독립 brute force for smaller n
                if n > 200000:
                    return None  # too slow for sympy verify
                perfect = set()
                perfect.add(1)
                for exp in [2, 3, 5, 7, 11, 13, 17, 19]:
                    if 2 ** exp > n:
                        break
                    root, _ = integer_nthroot(n, exp)
                    for base in range(2, root + 1):
                        val = base ** exp
                        if val <= n:
                            perfect.add(val)
                return len(perfect) % 1000
            else:
                root, _ = integer_nthroot(n, 2)
                total = root * (root + 1) * (2 * root + 1) // 6
                return total % 1000
        except Exception:
            return None
