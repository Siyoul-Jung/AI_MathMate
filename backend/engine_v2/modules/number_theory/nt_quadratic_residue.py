"""
AI_MathMate V2 — 이차 잉여 (nt_quadratic_residue)
르장드르 기호, 이차 잉여/비잉여 판별, 이차 잉여의 개수. AIME 기출 6회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtQuadraticResidueModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_quadratic_residue",
        name="이차 잉여",
        domain="integer",
        namespace="nt_qr",
        input_schema={
            "p": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=997, description="홀수 소수 p"),
            "a": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=996, description="이차 잉여 판별 대상"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'legendre' | 'qr_count' | 'sum_qr' | 'smallest_qnr'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=5.0,
        min_difficulty=7,
        category="number_theory",
        tags=["quadratic_residue", "legendre_symbol", "euler_criterion", "quadratic_reciprocity"],
        exam_types=["AIME"],
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
    def _legendre(a: int, p: int) -> int:
        """르장드르 기호 (a/p): 오일러 판정법."""
        a = a % p
        if a == 0:
            return 0
        result = pow(a, (p - 1) // 2, p)
        return result if result <= 1 else -1  # p-1 ≡ -1 (mod p)

    @staticmethod
    def _quadratic_residues(p: int) -> list[int]:
        """mod p의 이차 잉여 집합 (0 제외)."""
        qr = set()
        for x in range(1, p):
            qr.add(pow(x, 2, p))
        return sorted(qr)

    def generate_seed(self, difficulty_hint: float = 9.0) -> dict[str, Any]:
        primes = [p for p in range(3, 998) if self._is_prime(p) and p % 2 == 1]
        modes = ["legendre", "qr_count", "sum_qr", "smallest_qnr"]

        for _ in range(100):
            mode = random.choice(modes)
            if mode == "legendre":
                p = random.choice(primes)
                a = random.randint(1, p - 1)
            elif mode == "qr_count":
                p = random.choice([q for q in primes if q < 500])
                a = 1  # unused
            elif mode == "sum_qr":
                p = random.choice([q for q in primes if q < 200])
                a = 1
            else:  # smallest_qnr
                p = random.choice(primes)
                a = 1

            seed = {"p": p, "a": a, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"p": 7, "a": 3, "mode": "legendre"}

    def execute(self, seed: dict[str, Any]) -> int:
        p, a, mode = seed["p"], seed["a"], seed["mode"]

        if mode == "legendre":
            # 르장드르 기호 값: 1 (이차 잉여), 0, -1 → 정답은 양수 변환
            leg = self._legendre(a, p)
            # -1 → 999 (p-1 mod 1000), 0 → 0, 1 → 1
            if leg == -1:
                return (p - 1) % 1000  # p-1 ≡ -1 (mod p)이므로 p-1을 답으로
            return leg % 1000

        elif mode == "qr_count":
            # mod p의 이차 잉여 개수 = (p-1)/2
            qr = self._quadratic_residues(p)
            return len(qr) % 1000

        elif mode == "sum_qr":
            # mod p의 이차 잉여 합
            qr = self._quadratic_residues(p)
            return sum(qr) % 1000

        else:  # smallest_qnr
            # 최소 이차 비잉여
            for candidate in range(2, p):
                if self._legendre(candidate, p) == -1:
                    return candidate % 1000
            return 0

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        p, a, mode = seed["p"], seed["a"], seed["mode"]

        if mode == "legendre":
            leg = self._legendre(a, p)
            return [
                f"1. 르장드르 기호 ({a}/{p})를 오일러 판정법으로 구합니다.",
                f"2. {a}^(({p}-1)/2) mod {p} = {a}^{(p-1)//2} mod {p}를 계산합니다.",
                f"3. 결과: {'이차 잉여' if leg == 1 else '이차 비잉여' if leg == -1 else '0'}.",
                f"4. 정답: {self.execute(seed)}.",
            ]
        elif mode == "qr_count":
            count = (p - 1) // 2
            return [
                f"1. mod {p}의 이차 잉여 개수를 구합니다.",
                f"2. 홀수 소수 p에 대해 이차 잉여의 개수 = (p-1)/2 = {count}.",
                f"3. {count} mod 1000 = {count % 1000}.",
            ]
        elif mode == "sum_qr":
            qr = self._quadratic_residues(p)
            total = sum(qr)
            return [
                f"1. mod {p}의 모든 이차 잉여를 구합니다: {qr[:5]}... (총 {len(qr)}개).",
                f"2. 이차 잉여의 합을 계산합니다.",
                f"3. 합 = {total}, mod 1000 = {total % 1000}.",
            ]
        else:
            for candidate in range(2, p):
                if self._legendre(candidate, p) == -1:
                    return [
                        f"1. mod {p}의 최소 이차 비잉여를 찾습니다.",
                        f"2. 2부터 순서대로 오일러 판정법을 적용합니다.",
                        f"3. ({candidate}/{p}) = -1이므로, 최소 이차 비잉여 = {candidate}.",
                    ]
            return [f"1. mod {p}의 이차 비잉여를 찾습니다.", f"2. 탐색을 수행합니다."]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy.ntheory.residues import is_quad_residue
            from sympy import jacobi_symbol
            p, a, mode = seed["p"], seed["a"], seed["mode"]

            if mode == "legendre":
                leg = jacobi_symbol(a, p)
                if leg == -1:
                    return (p - 1) % 1000
                return leg % 1000
            elif mode == "qr_count":
                count = sum(1 for x in range(1, p) if is_quad_residue(x, p))
                return count % 1000
            elif mode == "sum_qr":
                total = sum(x for x in range(1, p) if is_quad_residue(x, p))
                return total % 1000
            else:
                for candidate in range(2, p):
                    if not is_quad_residue(candidate, p):
                        return candidate % 1000
                return 0
        except Exception:
            return None
