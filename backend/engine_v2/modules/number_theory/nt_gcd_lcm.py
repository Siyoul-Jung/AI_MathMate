"""
AI_MathMate V2 — GCD/LCM (nt_gcd_lcm)
최대공약수, 최소공배수, 유클리드 알고리즘 응용. AIME 기출 24회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtGcdLcmModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_gcd_lcm",
        name="GCD/LCM",
        domain="integer",
        namespace="nt_gcdlcm",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=100000, description="첫 번째 정수"),
            "b": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=100000, description="두 번째 정수"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'gcd' | 'lcm' | 'gcd_lcm_sum' | 'pair_count'"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=500,
                           description="pair_count 모드: gcd=n인 쌍의 수"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=3.0,
        min_difficulty=2,
        category="number_theory",
        tags=["gcd", "lcm", "euclidean_algorithm", "coprime"],
        exam_types=["AIME", "AMC"],
    )

    @staticmethod
    def _euler_totient(n: int) -> int:
        """오일러 피 함수 φ(n)."""
        result = n
        p = 2
        temp = n
        while p * p <= temp:
            if temp % p == 0:
                while temp % p == 0:
                    temp //= p
                result -= result // p
            p += 1
        if temp > 1:
            result -= result // temp
        return result

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["gcd", "lcm", "gcd_lcm_sum", "pair_count"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "pair_count":
                n = random.randint(2, 200) if difficulty_hint < 10 else random.randint(50, 500)
                a, b = n, n  # placeholders
            else:
                a = random.randint(10, 5000) if difficulty_hint < 10 else random.randint(100, 100000)
                b = random.randint(10, 5000) if difficulty_hint < 10 else random.randint(100, 100000)
                n = 1  # unused

            seed = {"a": a, "b": b, "mode": mode, "n": n}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"a": 12, "b": 18, "mode": "gcd", "n": 1}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, mode = seed["a"], seed["b"], seed["mode"]

        if mode == "gcd":
            return math.gcd(a, b) % 1000

        elif mode == "lcm":
            return (a * b // math.gcd(a, b)) % 1000

        elif mode == "gcd_lcm_sum":
            g = math.gcd(a, b)
            l = a * b // g
            return (g + l) % 1000

        else:  # pair_count
            # 1 <= x, y <= n*n에서 gcd(x, y) = n인 순서쌍 (x, y)의 개수
            # gcd(x, y) = n ⟺ gcd(x/n, y/n) = 1, 1 <= x/n, y/n <= n
            n = seed["n"]
            # 1~n 범위에서 서로소 쌍의 수 = 2 * Σ_{k=1}^{n} φ(k) - 1
            # 순서쌍이므로 Σ_{i=1}^{n} Σ_{j=1}^{n} [gcd(i,j)==1]
            count = 0
            for i in range(1, n + 1):
                for j in range(1, n + 1):
                    if math.gcd(i, j) == 1:
                        count += 1
            return count % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, mode = seed["a"], seed["b"], seed["mode"]

        if mode == "gcd":
            g = math.gcd(a, b)
            return [
                f"1. 유클리드 호제법을 적용합니다: gcd({a}, {b}).",
                f"2. 반복 나눗셈으로 gcd = {g}를 구합니다.",
                f"3. {g} mod 1000 = {g % 1000}.",
            ]
        elif mode == "lcm":
            g = math.gcd(a, b)
            l = a * b // g
            return [
                f"1. gcd({a}, {b}) = {g}를 구합니다.",
                f"2. lcm({a}, {b}) = {a} × {b} / {g} = {l}.",
                f"3. {l} mod 1000 = {l % 1000}.",
            ]
        elif mode == "gcd_lcm_sum":
            g = math.gcd(a, b)
            l = a * b // g
            return [
                f"1. gcd({a}, {b}) = {g}, lcm({a}, {b}) = {l}를 구합니다.",
                f"2. gcd + lcm = {g} + {l} = {g + l}.",
                f"3. {g + l} mod 1000 = {(g + l) % 1000}.",
            ]
        else:
            n = seed["n"]
            return [
                f"1. gcd(x, y) = {n}인 순서쌍 (x, y)의 수를 구합니다 (1 ≤ x, y ≤ {n}²).",
                f"2. x = {n}i, y = {n}j로 치환하면 gcd(i, j) = 1이고 1 ≤ i, j ≤ {n}.",
                f"3. 1~{n} 범위의 서로소 순서쌍 수를 오일러 φ 함수로 계산합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import gcd as sym_gcd, lcm as sym_lcm, totient
            a, b, mode = seed["a"], seed["b"], seed["mode"]

            if mode == "gcd":
                return int(sym_gcd(a, b)) % 1000
            elif mode == "lcm":
                return int(sym_lcm(a, b)) % 1000
            elif mode == "gcd_lcm_sum":
                g = int(sym_gcd(a, b))
                l = int(sym_lcm(a, b))
                return (g + l) % 1000
            else:
                n = seed["n"]
                count = 0
                for i in range(1, n + 1):
                    for j in range(1, n + 1):
                        if int(sym_gcd(i, j)) == 1:
                            count += 1
                return count % 1000
        except Exception:
            return None
