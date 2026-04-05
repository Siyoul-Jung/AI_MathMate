"""
AI_MathMate V2 -- comb_derangement (교란순열 / Derangements)
D(n) = n! * sum((-1)^k / k!, k=0..n) -- 어떤 원소도 제자리에 오지 않는 순열의 수.
기출 6회 (AIME).
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombDerangementModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_derangement",
        name="교란순열 (Derangements)",
        domain="integer",
        namespace="comb_derange",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=12, description="원소 수"),
            "mode": FieldSpec(dtype=str, domain="str", description="'full' | 'partial' | 'ratio'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=6,
        category="combinatorics",
        tags=["derangement", "inclusion_exclusion", "subfactorial", "permutation"],
        exam_types=["AIME"],
        bridge_output_keys=["derangement_count", "n"],
    )

    @staticmethod
    def _subfactorial(n: int) -> int:
        """D(n) = n! * sum((-1)^k / k!, k=0..n) = round(n! / e)"""
        if n == 0:
            return 1
        if n == 1:
            return 0
        # 재귀: D(n) = (n-1)(D(n-1) + D(n-2))
        d_prev2, d_prev1 = 1, 0  # D(0), D(1)
        for i in range(2, n + 1):
            d_curr = (i - 1) * (d_prev1 + d_prev2)
            d_prev2, d_prev1 = d_prev1, d_curr
        return d_prev1

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["full", "partial", "ratio"]
        for _ in range(100):
            mode = random.choice(modes)
            if difficulty_hint < 9:
                n = random.randint(3, 8)
            else:
                n = random.randint(6, 12)
            seed = {"n": n, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n": 5, "mode": "full"}

    def execute(self, seed: dict[str, Any]) -> int:
        n = seed["n"]
        mode = seed["mode"]

        if mode == "full":
            # D(n) mod 1000
            return self._subfactorial(n) % 1000

        elif mode == "partial":
            # 정확히 1개만 제자리에 오는 순열 수
            # = C(n,1) * D(n-1) = n * D(n-1)
            return (n * self._subfactorial(n - 1)) % 1000

        else:  # ratio
            # D(n) + D(n-1)을 구한다 (재귀 관계 활용 문제)
            # D(n) + D(n-1) = D(n) + D(n-1)
            # 참고: D(n) / n! -> 1/e 수렴, 하지만 정수답을 위해 합을 사용
            result = self._subfactorial(n) + self._subfactorial(n - 1)
            return result % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        n = seed["n"]
        return {
            "derangement_count": self._subfactorial(n),
            "n": n,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n = seed["n"]
        mode = seed["mode"]
        dn = self._subfactorial(n)

        if mode == "full":
            return [
                f"1. {n}개 원소의 교란순열 D({n})을 구합니다.",
                f"2. 포함-배제 원리: D({n}) = {n}! * sum((-1)^k/k!, k=0..{n}).",
                f"3. 또는 재귀: D({n}) = ({n}-1)(D({n-1}) + D({n-2}))를 사용합니다.",
                f"4. D({n}) = {dn}, mod 1000 = {dn % 1000}.",
            ]
        elif mode == "partial":
            dn1 = self._subfactorial(n - 1)
            return [
                f"1. {n}개 원소 중 정확히 1개만 제자리에 오는 순열 수를 구합니다.",
                f"2. 제자리에 올 원소 선택: C({n},1) = {n}가지.",
                f"3. 나머지 {n-1}개의 교란순열: D({n-1}) = {dn1}.",
                f"4. 답 = {n} x {dn1} = {n * dn1}, mod 1000 = {(n * dn1) % 1000}.",
            ]
        else:
            dn1 = self._subfactorial(n - 1)
            return [
                f"1. D({n}) + D({n-1})을 구합니다.",
                f"2. D({n}) = {dn}, D({n-1}) = {dn1}.",
                f"3. 합 = {dn + dn1}.",
                f"4. mod 1000 = {(dn + dn1) % 1000}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import subfactorial, Integer
            n = seed["n"]
            mode = seed["mode"]
            dn = int(subfactorial(Integer(n)))
            if mode == "full":
                return dn % 1000
            elif mode == "partial":
                dn1 = int(subfactorial(Integer(n - 1)))
                return (n * dn1) % 1000
            else:
                dn1 = int(subfactorial(Integer(n - 1)))
                return (dn + dn1) % 1000
        except Exception:
            return None
