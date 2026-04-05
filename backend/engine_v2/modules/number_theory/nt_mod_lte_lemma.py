"""
AI_MathMate V2 — LTE 보조정리 (nt_mod_lte_lemma)
Lifting the Exponent (LTE) Lemma: v_p(a^n - b^n) 또는 v_p(a^n + b^n) 계산.
AIME 기출 4회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtModLteLemmaModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_mod_lte_lemma",
        name="LTE 보조정리",
        domain="integer",
        namespace="nt_lte",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=200, description="밑 a"),
            "b": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=200, description="밑 b"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=500, description="지수 n"),
            "p": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=97, description="소수 p"),
            "mode": FieldSpec(dtype=str, domain="str", description="'v_diff' | 'v_sum'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=5.5,
        min_difficulty=8,
        category="number_theory",
        tags=["LTE", "lifting_the_exponent", "p_adic_valuation", "advanced"],
        exam_types=["AIME"],
        bridge_input_accepts=["prime", "order"],
        bridge_output_keys=["prime", "valuation_result"],
    )

    @staticmethod
    def _is_prime(n: int) -> bool:
        if n < 2:
            return False
        if n < 4:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    @staticmethod
    def _v_p(n: int, p: int) -> int:
        """p-adic valuation: n에서 소수 p의 지수."""
        if n == 0:
            return float('inf')  # type: ignore
        count = 0
        n = abs(n)
        while n % p == 0:
            count += 1
            n //= p
        return count

    @staticmethod
    def _lte_diff(a: int, b: int, n: int, p: int) -> int:
        """
        LTE for v_p(a^n - b^n):
        - p odd, p | (a-b), p ∤ a, p ∤ b:
          v_p(a^n - b^n) = v_p(a - b) + v_p(n)
        - p = 2, 2 | (a-b), n even:
          v_p(a^n - b^n) = v_2(a - b) + v_2(a + b) + v_2(n) - 1
        - Otherwise: direct computation
        """
        val = abs(pow(a, n) - pow(b, n))
        if val == 0:
            return 0
        return NtModLteLemmaModule._v_p(val, p)

    @staticmethod
    def _lte_sum(a: int, b: int, n: int, p: int) -> int:
        """v_p(a^n + b^n) — 직접 계산."""
        val = pow(a, n) + pow(b, n)
        if val == 0:
            return 0
        return NtModLteLemmaModule._v_p(val, p)

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        primes = [p for p in range(2, 50) if self._is_prime(p)]
        modes = ["v_diff", "v_sum"]

        for _ in range(100):
            mode = random.choice(modes)
            p = random.choice(primes)

            if mode == "v_diff":
                # p | (a - b) 조건을 만족하도록 생성
                b = random.randint(2, 50)
                a = b + p * random.randint(1, 10)
                n = random.randint(2, 100) if difficulty_hint < 12 else random.randint(10, 500)
            else:
                # v_sum: p odd, n odd, p | (a + b) 조건
                if p == 2:
                    continue  # p=2일 때 a^n+b^n 은 LTE가 복잡
                b = random.randint(2, 50)
                a = p * random.randint(1, 10) - b
                if a <= 0:
                    a += p * (abs(a) // p + 2)
                n = random.choice([k for k in range(3, 100, 2)])  # 홀수

            if a <= 0 or b <= 0 or a % p == 0 or b % p == 0:
                continue

            seed = {"a": a, "b": b, "n": n, "p": p, "mode": mode}
            try:
                ans = self.execute(seed)
                if 0 <= ans <= 999:
                    return seed
            except (OverflowError, ValueError):
                continue

        return {"a": 7, "b": 2, "n": 10, "p": 5, "mode": "v_diff"}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, n, p, mode = seed["a"], seed["b"], seed["n"], seed["p"], seed["mode"]

        if mode == "v_diff":
            return self._lte_diff(a, b, n, p) % 1000
        else:
            return self._lte_sum(a, b, n, p) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, n, p, mode = seed["a"], seed["b"], seed["n"], seed["p"], seed["mode"]

        if mode == "v_diff":
            vp_ab = self._v_p(a - b, p)
            vp_n = self._v_p(n, p)
            result = self._lte_diff(a, b, n, p)
            return [
                f"1. v_{p}({a}^{n} - {b}^{n})를 LTE 보조정리로 구합니다.",
                f"2. p = {p}, a - b = {a - b}이므로 v_{p}(a - b) = {vp_ab}, v_{p}(n) = v_{p}({n}) = {vp_n}.",
                f"3. LTE 조건을 확인하고 v_{p} = {result}를 계산합니다.",
                f"4. 결과: {result} mod 1000 = {result % 1000}.",
            ]
        else:
            result = self._lte_sum(a, b, n, p)
            return [
                f"1. v_{p}({a}^{n} + {b}^{n})를 구합니다.",
                f"2. LTE (합 버전): p = {p}, n = {n} (홀수), a + b = {a + b}.",
                f"3. v_{p}(a + b) = {self._v_p(a + b, p)}, v_{p}(n) = {self._v_p(n, p)}를 계산합니다.",
                f"4. 결과: {result} mod 1000 = {result % 1000}.",
            ]

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        return {"prime": seed["p"], "valuation_result": self.execute(seed)}

    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float = 10.0) -> dict[str, Any]:
        p = bridge.get("prime")
        if p and self._is_prime(int(p)):
            for _ in range(100):
                a = random.randint(2, 100)
                b = random.randint(1, a - 1)
                if (a - b) % int(p) == 0 and a % int(p) != 0:
                    n = random.randint(2, 200)
                    seed = {"a": a, "b": b, "n": n, "p": int(p), "mode": "v_diff"}
                    ans = self.execute(seed)
                    if 0 < ans <= 999:
                        return seed
        return self.generate_seed(difficulty_hint)

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import multiplicity
            a, b, n, p, mode = seed["a"], seed["b"], seed["n"], seed["p"], seed["mode"]

            if mode == "v_diff":
                val = abs(pow(a, n) - pow(b, n))
            else:
                val = pow(a, n) + pow(b, n)

            if val == 0:
                return 0
            return int(multiplicity(p, val)) % 1000
        except Exception:
            return None
