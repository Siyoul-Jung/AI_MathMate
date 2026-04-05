"""
AI_MathMate V2 — 포함-배제 원리 (comb_inclusion_exclusion)
AIME 기출 3회 UNMAPPED으로 발견된 핵심 기법.
집합의 합집합 크기를 구하는 포함-배제 공식 및 교란순열 응용을 다룹니다.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombInclusionExclusionModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_inclusion_exclusion",
        name="포함-배제 원리 (Inclusion-Exclusion)",
        domain="integer",
        namespace="comb_ie",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=999, description="전체 원소 수"),
            "mode": FieldSpec(dtype=str, domain="str", description="'two_sets' | 'three_sets' | 'derangement_ie'"),
            "a": FieldSpec(dtype=int, domain="Z+", description="첫 번째 조건 (배수 기준)"),
            "b": FieldSpec(dtype=int, domain="Z+", description="두 번째 조건"),
            "c": FieldSpec(dtype=int, domain="Z+", description="세 번째 조건 (three_sets용)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=3,
        category="combinatorics",
        tags=["inclusion_exclusion", "counting", "sets", "overcounting", "derangement"],
        exam_types=["AIME"],
        bridge_output_keys=["set_count", "total"],
        bridge_input_accepts=["n_elements", "subset_count", "n_sides"],
    )

    SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23]

    def generate_seed(self, difficulty_hint: float = 7.0) -> dict[str, Any]:
        modes = ["two_sets", "three_sets", "derangement_ie"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "two_sets":
                n = random.randint(100, 999)
                a, b = random.sample(self.SMALL_PRIMES[:6], 2)
                c = 1
            elif mode == "three_sets":
                n = random.randint(200, 999)
                a, b, c = random.sample(self.SMALL_PRIMES[:7], 3)
            else:  # derangement_ie
                n = random.randint(4, 10) if difficulty_hint < 10 else random.randint(7, 10)
                a, b, c = 1, 1, 1

            seed = {"n": n, "mode": mode, "a": a, "b": b, "c": c}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n": 100, "mode": "two_sets", "a": 3, "b": 5, "c": 1}

    def execute(self, seed: dict[str, Any]) -> int:
        n, mode = seed["n"], seed["mode"]
        a, b, c = seed["a"], seed["b"], seed["c"]

        if mode == "two_sets":
            # |A ∪ B| = |A| + |B| - |A ∩ B|
            lcm_ab = a * b // math.gcd(a, b)
            count = n // a + n // b - n // lcm_ab
            return count % 1000

        elif mode == "three_sets":
            # |A ∪ B ∪ C| = |A|+|B|+|C| - |A∩B|-|A∩C|-|B∩C| + |A∩B∩C|
            lcm_ab = a * b // math.gcd(a, b)
            lcm_ac = a * c // math.gcd(a, c)
            lcm_bc = b * c // math.gcd(b, c)
            lcm_abc = lcm_ab * c // math.gcd(lcm_ab, c)
            count = (n // a + n // b + n // c
                     - n // lcm_ab - n // lcm_ac - n // lcm_bc
                     + n // lcm_abc)
            return count % 1000

        else:  # derangement_ie
            # D(n) = n! * Σ_{k=0}^{n} (-1)^k / k!
            dn = 0
            for k in range(n + 1):
                dn += ((-1) ** k) * math.factorial(n) // math.factorial(k)
            return dn % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        ans = self.execute(seed)
        return {
            "set_count": ans,
            "total": seed["n"],
        }

    def generate_seed_with_bridge(
        self, bridge: dict[str, Any], difficulty_hint: float = 7.0
    ) -> dict[str, Any]:
        """상위 모듈의 n_elements/subset_count/n_sides를 n으로 활용."""
        n_candidate = bridge.get("n_elements") or bridge.get("subset_count") or bridge.get("n_sides")
        if n_candidate is not None:
            n_candidate = int(n_candidate)
            # derangement_ie 모드: 작은 n (4-10)
            if 4 <= n_candidate <= 10:
                seed = {"n": n_candidate, "mode": "derangement_ie", "a": 1, "b": 1, "c": 1}
                ans = self.execute(seed)
                if 0 <= ans <= 999:
                    return seed
            # two_sets/three_sets: n을 전체 원소 수로 사용 (10-999)
            if 10 <= n_candidate <= 999:
                for _ in range(50):
                    mode = random.choice(["two_sets", "three_sets"])
                    if mode == "two_sets":
                        a, b = random.sample(self.SMALL_PRIMES[:6], 2)
                        c = 1
                    else:
                        a, b, c = random.sample(self.SMALL_PRIMES[:7], 3)
                    seed = {"n": n_candidate, "mode": mode, "a": a, "b": b, "c": c}
                    ans = self.execute(seed)
                    if 0 <= ans <= 999:
                        return seed
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, mode = seed["n"], seed["mode"]
        a, b, c = seed["a"], seed["b"], seed["c"]

        if mode == "two_sets":
            return [
                f"1. 1부터 {n}까지에서 {a}의 배수 집합 A, {b}의 배수 집합 B를 정의합니다.",
                f"2. |A| = floor({n}/{a}), |B| = floor({n}/{b})를 각각 구합니다.",
                f"3. |A ∩ B| = floor({n}/lcm({a},{b}))를 구하여 중복 카운트를 제거합니다.",
                f"4. 포함-배제 공식 |A ∪ B| = |A| + |B| - |A ∩ B|로 최종 답을 구합니다.",
            ]
        elif mode == "three_sets":
            return [
                f"1. 1부터 {n}까지에서 {a}, {b}, {c}의 배수 집합 A, B, C를 정의합니다.",
                f"2. 각 집합의 크기 |A|, |B|, |C|를 구합니다.",
                f"3. 쌍별 교집합 |A∩B|, |A∩C|, |B∩C|와 삼중 교집합 |A∩B∩C|를 LCM으로 구합니다.",
                f"4. 3집합 포함-배제 공식으로 |A ∪ B ∪ C|를 계산합니다.",
            ]
        else:
            return [
                f"1. {n}개 원소의 완전순열(교란순열, derangement) D({n})을 구합니다.",
                f"2. 포함-배제 원리를 적용: D(n) = n! × Σ((-1)^k / k!, k=0..n).",
                f"3. 각 항을 계산하여 합산합니��.",
                f"4. D({n}) mod 1000을 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        """완전 열거 또는 sympy exact arithmetic으로 독립 검증."""
        try:
            n, mode = seed["n"], seed["mode"]
            a, b, c = seed["a"], seed["b"], seed["c"]

            if mode == "two_sets":
                # 완전 열거 (n <= 999이므로 안전)
                count = sum(1 for i in range(1, n + 1) if i % a == 0 or i % b == 0)
                return count % 1000

            elif mode == "three_sets":
                count = sum(1 for i in range(1, n + 1)
                            if i % a == 0 or i % b == 0 or i % c == 0)
                return count % 1000

            else:  # derangement_ie
                # 완전 열거 (n <= 10이므로 안전)
                from itertools import permutations
                count = sum(1 for p in permutations(range(n)) if all(p[i] != i for i in range(n)))
                return count % 1000
        except Exception:
            return None
