"""
AI_MathMate V2 — 모듈러 산술 (nt_modular_arithmetic)
거듭제곱 모듈러, 페르마 소정리, 모듈러 역원 등. AIME 기출 103회.
Bridge 타겟 모듈: prime_factors, divisor_count, lcm_value 입력.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtModularArithmeticModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_modular_arithmetic",
        name="모듈러 산술",
        domain="integer",
        namespace="nt_modarith",
        input_schema={
            "base": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=10000, description="밑"),
            "exp": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=1000000, description="지수"),
            "mod": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=10000, description="법"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'power_mod' | 'inverse' | 'sum_powers' | 'fermat_order'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=4,
        category="number_theory",
        tags=["modular_arithmetic", "power_mod", "fermat", "modular_inverse", "euler_theorem"],
        exam_types=["AIME", "AMC"],
        bridge_input_accepts=["prime_factors", "divisor_count", "lcm_value"],
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
    def _euler_totient(n: int) -> int:
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

    @staticmethod
    def _mul_order(base: int, mod: int) -> int:
        """base의 mod에 대한 곱셈 위수 ord_mod(base)."""
        if math.gcd(base, mod) != 1:
            return 0
        order = 1
        current = base % mod
        while current != 1:
            current = (current * base) % mod
            order += 1
            if order > mod:
                return 0
        return order

    def generate_seed(self, difficulty_hint: float = 7.0) -> dict[str, Any]:
        modes = ["power_mod", "inverse", "sum_powers", "fermat_order"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "power_mod":
                base = random.randint(2, 500) if difficulty_hint < 10 else random.randint(100, 10000)
                exp = random.randint(10, 10000) if difficulty_hint < 10 else random.randint(1000, 1000000)
                mod = random.randint(100, 1000) if difficulty_hint < 10 else random.randint(500, 10000)
            elif mode == "inverse":
                mod = random.choice([p for p in range(100, 1000) if NtModularArithmeticModule._is_prime(p)])
                base = random.randint(2, mod - 1)
                exp = 1  # unused
            elif mode == "sum_powers":
                base = random.randint(2, 50)
                exp = random.randint(5, 200)  # 합산할 항 수
                mod = random.randint(100, 1000)
            else:  # fermat_order
                mod = random.choice([p for p in range(10, 500) if NtModularArithmeticModule._is_prime(p)])
                base = random.randint(2, mod - 1)
                exp = mod  # unused

            seed = {"base": base, "exp": exp, "mod": mod, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"base": 2, "exp": 100, "mod": 1000, "mode": "power_mod"}

    def execute(self, seed: dict[str, Any]) -> int:
        base, exp, mod, mode = seed["base"], seed["exp"], seed["mod"], seed["mode"]

        if mode == "power_mod":
            return pow(base, exp, mod) % 1000

        elif mode == "inverse":
            # 모듈러 역원: base^(-1) mod mod
            if math.gcd(base, mod) != 1:
                return 0
            return pow(base, -1, mod) % 1000

        elif mode == "sum_powers":
            # Σ_{k=0}^{exp} base^k mod mod
            total = 0
            for k in range(exp + 1):
                total = (total + pow(base, k, mod)) % mod
            return total % 1000

        else:  # fermat_order
            # 곱셈 위수 ord_mod(base)
            return self._mul_order(base, mod) % 1000

    def generate_seed_with_bridge(self, bridge: dict[str, Any], difficulty_hint: float = 8.0) -> dict[str, Any]:
        """Bridge 입력으로부터 mod 또는 base를 도출."""
        # prime_factors에서 소수를 추출하여 mod로 사용
        prime_factors = bridge.get("prime_factors", {})
        divisor_count = bridge.get("divisor_count")
        lcm_value = bridge.get("lcm_value")

        # mod 후보 설정
        if isinstance(prime_factors, dict) and prime_factors:
            primes = list(prime_factors.keys())
            mod_candidate = max(primes) if primes else 997
        elif lcm_value and isinstance(lcm_value, int):
            mod_candidate = lcm_value % 9973 + 100
        else:
            mod_candidate = 997

        if mod_candidate < 10:
            mod_candidate = 997

        for _ in range(100):
            mode = random.choice(["power_mod", "sum_powers", "fermat_order"])
            base = random.randint(2, 500)
            exp = random.randint(10, 10000)
            mod = mod_candidate if mod_candidate < 10000 else mod_candidate % 9973 + 100

            if mode == "fermat_order" and (not self._is_prime(mod) or math.gcd(base, mod) != 1):
                continue

            seed = {"base": base, "exp": exp, "mod": mod, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"base": 2, "exp": 100, "mod": 997, "mode": "power_mod"}

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        base, exp, mod, mode = seed["base"], seed["exp"], seed["mod"], seed["mode"]

        if mode == "power_mod":
            phi = self._euler_totient(mod)
            reduced = exp % phi if math.gcd(base, mod) == 1 else exp
            return [
                f"1. {base}^{exp} mod {mod}를 구합니다.",
                f"2. 오일러 정리: φ({mod}) = {phi}, gcd({base}, {mod})를 확인합니다.",
                f"3. 지수를 축소합니다: {exp} mod {phi} = {reduced}.",
                f"4. {base}^{reduced} mod {mod} = {pow(base, reduced, mod)}.",
            ]
        elif mode == "inverse":
            inv = pow(base, -1, mod) if math.gcd(base, mod) == 1 else 0
            return [
                f"1. {base}의 모듈러 역원을 mod {mod}에서 구합니다.",
                f"2. 확장 유클리드 또는 페르마 소정리를 적용합니다.",
                f"3. {base}^(-1) ≡ {inv} (mod {mod}).",
            ]
        elif mode == "sum_powers":
            return [
                f"1. Σ_{{k=0}}^{{{exp}}} {base}^k mod {mod}를 구합니다.",
                f"2. 등비급수 합 공식 또는 반복 모듈러 계산을 적용합니다.",
                f"3. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            order = self._mul_order(base, mod)
            return [
                f"1. ord_{mod}({base})를 구합니다.",
                f"2. {base}^k ≡ 1 (mod {mod})를 만족하는 최소 양의 정수 k를 찾습니다.",
                f"3. 위수 = {order}, mod 1000 = {order % 1000}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import mod_inverse, totient
            from sympy.ntheory.residues import n_order
            base, exp, mod, mode = seed["base"], seed["exp"], seed["mod"], seed["mode"]

            if mode == "power_mod":
                return pow(base, exp, mod) % 1000
            elif mode == "inverse":
                if math.gcd(base, mod) != 1:
                    return 0
                return int(mod_inverse(base, mod)) % 1000
            elif mode == "sum_powers":
                total = 0
                for k in range(exp + 1):
                    total = (total + pow(base, k, mod)) % mod
                return total % 1000
            else:
                if math.gcd(base, mod) != 1:
                    return 0
                return int(n_order(base, mod)) % 1000
        except Exception:
            return None
