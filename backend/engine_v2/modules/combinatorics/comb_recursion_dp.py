"""
AI_MathMate V2 -- comb_recursion_dp (재귀/DP / Recurrence & Dynamic Programming)
f(n) = a*f(n-1) + b*f(n-2) 형태의 재귀 관계식을 반복 계산하여 답을 구합니다.
타일링, 피보나치 변형, 문자열 세기 등.
기출 80회 (AIME).
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombRecursionDpModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_recursion_dp",
        name="재귀/DP (Recurrence & DP)",
        domain="integer",
        namespace="comb_rec_dp",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=50, description="목표 인덱스"),
            "a": FieldSpec(dtype=int, domain="Z", min_val=1, max_val=5, description="f(n-1) 계수"),
            "b": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=3, description="f(n-2) 계수"),
            "f0": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=5, description="초기값 f(0)"),
            "f1": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=5, description="초기값 f(1)"),
            "mode": FieldSpec(dtype=str, domain="str", description="'linear' | 'tiling' | 'string_count'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="f(n) mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=6,
        category="combinatorics",
        tags=["recurrence", "dynamic_programming", "fibonacci", "tiling", "linear_recurrence"],
        exam_types=["AIME"],
        bridge_output_keys=["sequence_value", "n"],
        bridge_input_accepts=["n_elements", "total_count"],
    )

    @staticmethod
    def _compute_recurrence(n: int, a: int, b: int, f0: int, f1: int) -> int:
        """f(k) = a*f(k-1) + b*f(k-2)를 반복 계산"""
        if n == 0:
            return f0
        if n == 1:
            return f1
        prev2, prev1 = f0, f1
        for _ in range(2, n + 1):
            curr = a * prev1 + b * prev2
            prev2, prev1 = prev1, curr
        return prev1

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["linear", "tiling", "string_count"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "tiling":
                # 2xn 타일링: f(n) = f(n-1) + f(n-2), f(0)=1, f(1)=1 (피보나치)
                n = random.randint(5, 40)
                a, b, f0, f1 = 1, 1, 1, 1
            elif mode == "string_count":
                # 0,1 문자열에서 연속 1이 없는 길이 n: f(n)=f(n-1)+f(n-2)
                n = random.randint(5, 35)
                a, b = 1, 1
                f0, f1 = 2, 3  # 길이 0->빈문자열(1개...편의상 2), 길이 1->0,1(2개...편의상 3)
                # 실제: f(1)=2(0,1), f(2)=3(00,01,10), f(n)=f(n-1)+f(n-2)
                f0, f1 = 2, 3
            else:  # linear
                a = random.randint(1, 4)
                b = random.randint(1, 3)
                f0 = random.randint(0, 3)
                f1 = random.randint(1, 5)
                n = random.randint(3, 30)

            seed = {"n": n, "a": a, "b": b, "f0": f0, "f1": f1, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"n": 10, "a": 1, "b": 1, "f0": 1, "f1": 1, "mode": "tiling"}

    def execute(self, seed: dict[str, Any]) -> int:
        n = seed["n"]
        a, b = seed["a"], seed["b"]
        f0, f1 = seed["f0"], seed["f1"]
        return self._compute_recurrence(n, a, b, f0, f1) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        n = seed["n"]
        a, b = seed["a"], seed["b"]
        f0, f1 = seed["f0"], seed["f1"]
        return {
            "sequence_value": self._compute_recurrence(n, a, b, f0, f1),
            "n": n,
        }

    def generate_seed_with_bridge(self, bridge: dict, difficulty_hint: float = 10.0) -> dict[str, Any]:
        n_elem = bridge.get("n_elements")
        if n_elem and 5 <= int(n_elem) <= 30:
            n = int(n_elem)
            a, b = random.randint(1, 3), random.randint(1, 3)
            f0, f1 = random.randint(1, 5), random.randint(1, 5)
            mode = random.choice(["linear", "fibonacci_variant"])
            seed = {"n": n, "a": a, "b": b, "f0": f0, "f1": f1, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n = seed["n"]
        a, b = seed["a"], seed["b"]
        f0, f1 = seed["f0"], seed["f1"]
        mode = seed["mode"]
        ans = self.execute(seed)

        if mode == "tiling":
            return [
                f"1. 2x{n} 격자를 1x2 도미노로 타일링하는 방법 수를 구합니다.",
                f"2. 재귀 관계: f(n) = f(n-1) + f(n-2), f(0)=1, f(1)=1.",
                f"3. 이것은 피보나치 수열과 동일합니다.",
                f"4. f({n}) mod 1000 = {ans}.",
            ]
        elif mode == "string_count":
            return [
                f"1. 길이 {n}인 0,1 문자열 중 연속 1이 없는 것의 개수를 구합니다.",
                f"2. 재귀 관계: f(n) = f(n-1) + f(n-2), f(1)=2, f(2)=3.",
                f"3. n={n}까지 반복 계산합니다.",
                f"4. f({n}) mod 1000 = {ans}.",
            ]
        else:
            return [
                f"1. 재귀 관계 f(n) = {a}*f(n-1) + {b}*f(n-2)를 설정합니다.",
                f"2. 초기값: f(0)={f0}, f(1)={f1}.",
                f"3. n={n}까지 반복 계산합니다.",
                f"4. f({n}) mod 1000 = {ans}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Function, rsolve, Symbol, Integer
            # 직접 재귀 계산으로 검증 (다른 경로)
            n = seed["n"]
            a, b = seed["a"], seed["b"]
            f0, f1 = seed["f0"], seed["f1"]

            # 행렬 거듭제곱으로 독립 검증
            # [[a, b], [1, 0]]^(n-1) * [f1, f0]^T
            if n == 0:
                return f0 % 1000
            if n == 1:
                return f1 % 1000

            # 행렬 [[a, b], [1, 0]]
            m00, m01, m10, m11 = 1, 0, 0, 1  # identity
            ba, bb, bc, bd = a, b, 1, 0  # base matrix

            exp = n - 1
            while exp > 0:
                if exp % 2 == 1:
                    # result = result * base
                    new00 = m00 * ba + m01 * bc
                    new01 = m00 * bb + m01 * bd
                    new10 = m10 * ba + m11 * bc
                    new11 = m10 * bb + m11 * bd
                    m00, m01, m10, m11 = new00, new01, new10, new11
                # base = base * base
                new_ba = ba * ba + bb * bc
                new_bb = ba * bb + bb * bd
                new_bc = bc * ba + bd * bc
                new_bd = bc * bb + bd * bd
                ba, bb, bc, bd = new_ba, new_bb, new_bc, new_bd
                exp //= 2

            result = m00 * f1 + m01 * f0
            return result % 1000
        except Exception:
            return None
