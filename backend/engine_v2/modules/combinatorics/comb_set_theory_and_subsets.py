"""
AI_MathMate V2 -- comb_set_theory_and_subsets (집합론 / Set Theory & Subsets)
2^n 부분집합 중 조건을 만족하는 부분집합의 수를 구합니다.
기출 44회 (AIME).
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombSetTheoryAndSubsetsModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_set_theory_and_subsets",
        name="집합론 및 부분집합 (Set Theory & Subsets)",
        domain="integer",
        namespace="comb_sets",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=15, description="전체 집합 크기"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'non_empty' | 'even_size' | 'no_consecutive' | 'sum_divisible'"),
            "divisor": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=7, description="합의 나눗수 (sum_divisible 모드)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="조건 만족 부분집합 수 mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=5,
        category="combinatorics",
        tags=["set_theory", "subsets", "power_set", "counting", "inclusion_exclusion"],
        exam_types=["AIME"],
        bridge_output_keys=["subset_count", "n"],
        bridge_input_accepts=["n_elements"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["non_empty", "even_size", "no_consecutive", "sum_divisible"]
        for _ in range(100):
            mode = random.choice(modes)
            if difficulty_hint < 9:
                n = random.randint(3, 10)
            else:
                n = random.randint(6, 15)
            divisor = random.randint(2, 7) if mode == "sum_divisible" else 2

            seed = {"n": n, "mode": mode, "divisor": divisor}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n": 6, "mode": "non_empty", "divisor": 2}

    def execute(self, seed: dict[str, Any]) -> int:
        n = seed["n"]
        mode = seed["mode"]
        divisor = seed.get("divisor", 2)

        if mode == "non_empty":
            # 비어있지 않은 부분집합 수 = 2^n - 1
            return (pow(2, n) - 1) % 1000

        elif mode == "even_size":
            # 짝수 크기 부분집합 수 = 2^(n-1) (공집합 포함)
            return pow(2, n - 1) % 1000

        elif mode == "no_consecutive":
            # {1,...,n}의 부분집합 중 연속 정수를 포함하지 않는 것의 수
            # = F(n+2) (피보나치 수, 공집합 포함)
            # 재귀: a(n) = a(n-1) + a(n-2), a(0)=1 (공집합), a(1)=2 ({}, {1})
            if n == 0:
                return 1
            prev2, prev1 = 1, 2  # a(0), a(1)
            for _ in range(2, n + 1):
                curr = prev1 + prev2
                prev2, prev1 = prev1, curr
            return prev1 % 1000

        else:  # sum_divisible
            # {1,...,n}의 부분집합 중 원소 합이 divisor로 나누어지는 것의 수
            # DP: dp[j] = 원소 합 mod divisor == j인 부분집합 수
            dp = [0] * divisor
            dp[0] = 1  # 공집합
            for i in range(1, n + 1):
                new_dp = dp[:]
                for j in range(divisor):
                    new_dp[(j + i) % divisor] += dp[j]
                dp = new_dp
            return dp[0] % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        return {
            "subset_count": self.execute(seed),
            "n": seed["n"],
        }

    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float = 10.0) -> dict[str, Any]:
        n_elem = bridge.get("n_elements")
        if n_elem and 3 <= int(n_elem) <= 20:
            n = int(n_elem)
            mode = random.choice(["non_empty", "even_size", "no_consecutive"])
            seed = {"n": n, "mode": mode, "divisor": 1}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n = seed["n"]
        mode = seed["mode"]
        divisor = seed.get("divisor", 2)
        ans = self.execute(seed)

        if mode == "non_empty":
            return [
                f"1. 집합 {{1,...,{n}}}의 모든 부분집합 수 = 2^{n} = {2**n}.",
                f"2. 공집합을 제외합니다.",
                f"3. 비어있지 않은 부분집합 수 = {2**n} - 1 = {2**n - 1}.",
                f"4. mod 1000 = {ans}.",
            ]
        elif mode == "even_size":
            return [
                f"1. 집합 {{1,...,{n}}}에서 짝수 크기 부분집합 수를 구합니다.",
                f"2. sum(C({n},k), k=0,2,4,...) = 2^({n}-1).",
                f"3. 이는 (1+1)^{n} + (1-1)^{n} 를 2로 나눈 결과입니다.",
                f"4. 2^{n-1} mod 1000 = {ans}.",
            ]
        elif mode == "no_consecutive":
            return [
                f"1. {{1,...,{n}}}에서 연속 정수를 포함하지 않는 부분집합 수를 구합니다.",
                f"2. 재귀: a(k) = a(k-1) + a(k-2), a(0)=1, a(1)=2.",
                f"3. 이는 피보나치 수열의 변형입니다.",
                f"4. a({n}) mod 1000 = {ans}.",
            ]
        else:
            return [
                f"1. {{1,...,{n}}}의 부분집합 중 원소 합이 {divisor}의 배수인 것의 수를 구합니다.",
                f"2. DP: dp[j] = 원소 합 mod {divisor} == j인 부분집합 수.",
                f"3. 각 원소 i=1..{n}을 순서대로 추가하며 dp를 갱신합니다.",
                f"4. dp[0] mod 1000 = {ans}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            n = seed["n"]
            mode = seed["mode"]
            divisor = seed.get("divisor", 2)

            if mode == "non_empty":
                return (2 ** n - 1) % 1000
            elif mode == "even_size":
                return (2 ** (n - 1)) % 1000
            elif mode == "no_consecutive":
                # 독립 검증: 조합론 공식 sum C(n-k+1, k) for k=0..(n+1)//2
                total = 0
                for k in range((n + 2) // 2 + 1):
                    if n - k + 1 >= k:
                        total += math.comb(n - k + 1, k)
                return total % 1000
            else:
                # Brute force for small n
                if n <= 20:
                    count = 0
                    for mask in range(1 << n):
                        s = sum(i + 1 for i in range(n) if mask & (1 << i))
                        if s % divisor == 0:
                            count += 1
                    return count % 1000
                return None
        except Exception:
            return None
