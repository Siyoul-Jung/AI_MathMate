"""
AI_MathMate V2 — 르장드르 공식과 바닥함수 (nt_floor_legendre)
n!에서 소수 p의 지수(르장드르 공식), 바닥함수 합 등을 다룹니다.
AIME 기출 8회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtFloorLegendreModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_floor_legendre",
        name="르장드르 공식과 바닥함수",
        domain="integer",
        namespace="nt_floor_leg",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=5, max_val=10000, description="팩토리얼 또는 합산 범위"),
            "p": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=97, description="소수 p"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'legendre' | 'floor_sum' | 'trailing_zeros'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=4.0,
        min_difficulty=5,
        category="number_theory",
        tags=["legendre_formula", "floor_function", "factorial", "trailing_zeros", "p_adic_valuation"],
        exam_types=["AIME"],
    )

    @staticmethod
    def _legendre(n: int, p: int) -> int:
        """n!에서 소수 p의 지수: Σ⌊n/p^k⌋."""
        total = 0
        pk = p
        while pk <= n:
            total += n // pk
            pk *= p
        return total

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

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        primes = [p for p in range(2, 98) if self._is_prime(p)]
        modes = ["legendre", "floor_sum", "trailing_zeros"]

        for _ in range(100):
            mode = random.choice(modes)
            p = random.choice(primes)
            if mode == "legendre":
                n = random.randint(50, 5000) if difficulty_hint < 10 else random.randint(500, 10000)
            elif mode == "floor_sum":
                n = random.randint(10, 500) if difficulty_hint < 10 else random.randint(100, 2000)
                p = random.randint(2, 20)  # 바닥함수 합에서는 p가 나누는 수
            else:  # trailing_zeros
                n = random.randint(50, 5000) if difficulty_hint < 10 else random.randint(500, 10000)
                p = 10  # 뒷자리 0의 개수 = v_5(n!) (v_2 >= v_5이므로)

            seed = {"n": n, "p": p, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n": 100, "p": 5, "mode": "trailing_zeros"}

    def execute(self, seed: dict[str, Any]) -> int:
        n, p, mode = seed["n"], seed["p"], seed["mode"]

        if mode == "legendre":
            return self._legendre(n, p) % 1000

        elif mode == "floor_sum":
            # Σ_{k=1}^{n} ⌊k/p⌋
            total = sum(k // p for k in range(1, n + 1))
            return total % 1000

        else:  # trailing_zeros
            # n!의 뒷자리 0의 개수 = min(v_2(n!), v_5(n!)) = v_5(n!)
            return self._legendre(n, 5) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, p, mode = seed["n"], seed["p"], seed["mode"]

        if mode == "legendre":
            terms = []
            pk = p
            while pk <= n:
                terms.append(f"⌊{n}/{pk}⌋ = {n // pk}")
                pk *= p
            val = self._legendre(n, p)
            return [
                f"1. 르장드르 공식을 적용합니다: v_{p}({n}!) = Σ⌊{n}/{p}^k⌋.",
                f"2. 각 항을 계산합니다: {' + '.join(terms)}.",
                f"3. 합계 = {val}, mod 1000 = {val % 1000}.",
            ]
        elif mode == "floor_sum":
            total = sum(k // p for k in range(1, n + 1))
            return [
                f"1. Σ_{{k=1}}^{{{n}}} ⌊k/{p}⌋를 구합니다.",
                f"2. 구간별 그룹핑: p의 배수 간격마다 ⌊k/p⌋ 값이 동일함을 이용합니다.",
                f"3. 합계 = {total}, mod 1000 = {total % 1000}.",
            ]
        else:
            val = self._legendre(n, 5)
            return [
                f"1. {n}!의 뒷자리 0의 개수 = v_5({n}!) (v_2 ≥ v_5이므로).",
                f"2. 르장드르 공식: v_5({n}!) = Σ⌊{n}/5^k⌋.",
                f"3. v_5({n}!) = {val}, mod 1000 = {val % 1000}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import factorial
            n, p, mode = seed["n"], seed["p"], seed["mode"]

            if mode == "legendre":
                # 독립 검증: 직접 n!을 계산하고 p로 나누기
                val = int(factorial(n))
                count = 0
                while val % p == 0:
                    val //= p
                    count += 1
                return count % 1000
            elif mode == "floor_sum":
                total = sum(k // p for k in range(1, n + 1))
                return total % 1000
            else:
                val = int(factorial(n))
                count = 0
                while val % 10 == 0:
                    val //= 10
                    count += 1
                return count % 1000
        except Exception:
            return None
