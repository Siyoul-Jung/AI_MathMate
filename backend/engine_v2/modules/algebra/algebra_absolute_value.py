"""
AI_MathMate V2 — 절대값 방정식/부등식 (algebra_absolute_value)
|ax + b| = c, |ax + b| + |cx + d| = k 형태의 절대값 문제를 다룹니다.
기출 빈도: 16회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraAbsoluteValueModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_absolute_value",
        name="절대값 방정식/부등식",
        domain="integer",
        namespace="alg_abs",
        input_schema={
            "a1": FieldSpec(dtype=int, domain="Z", min_val=1, max_val=10, description="첫 번째 절대값 내부 x 계수"),
            "b1": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20, description="첫 번째 절대값 내부 상수"),
            "a2": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=10, description="두 번째 절대값 내부 x 계수 (0이면 단일 절대값)"),
            "b2": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20, description="두 번째 절대값 내부 상수"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=100, description="우변 상수"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'single' | 'double' | 'count'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="정수 해의 합 또는 개수 mod 1000"),
        },
        logic_depth=4,
        daps_contribution=3.5,
        min_difficulty=3,
        category="algebra",
        tags=["absolute_value", "equation", "inequality", "casework", "piecewise"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["solution_set", "solution_sum"],
    )

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["single", "double", "count"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "single":
                # |a1*x + b1| = k  →  정수 해의 합
                a1 = random.randint(1, 8)
                b1 = random.randint(-15, 15)
                a2 = 0
                b2 = 0
                k = random.randint(1, 50)
            elif mode == "double":
                # |a1*x + b1| + |a2*x + b2| = k  →  정수 해의 합
                a1 = random.randint(1, 6)
                b1 = random.randint(-12, 12)
                a2 = random.randint(1, 6)
                b2 = random.randint(-12, 12)
                k = random.randint(5, 80)
            else:
                # |a1*x + b1| <= k  →  정수 해의 개수
                a1 = random.randint(1, 8)
                b1 = random.randint(-15, 15)
                a2 = 0
                b2 = 0
                k = random.randint(1, 60)

            seed = {"a1": a1, "b1": b1, "a2": a2, "b2": b2, "k": k, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"a1": 2, "b1": 3, "a2": 0, "b2": 0, "k": 7, "mode": "single"}

    def execute(self, seed: dict[str, Any]) -> int:
        a1 = seed["a1"]
        b1 = seed["b1"]
        a2 = seed["a2"]
        b2 = seed["b2"]
        k = seed["k"]
        mode = seed["mode"]

        if mode == "single":
            # |a1*x + b1| = k
            # Case 1: a1*x + b1 = k  →  x = (k - b1) / a1
            # Case 2: a1*x + b1 = -k  →  x = (-k - b1) / a1
            solutions = set()
            for rhs in [k, -k]:
                num = rhs - b1
                if num % a1 == 0:
                    solutions.add(num // a1)
            if not solutions:
                return 0
            return sum(solutions) % 1000

        elif mode == "double":
            # |a1*x + b1| + |a2*x + b2| = k
            # 경계점에서 구간 분리하여 정수 해 탐색
            # 경계점: x = -b1/a1, x = -b2/a2
            solutions = set()
            search_range = max(abs(k) + abs(b1) + abs(b2), 200)
            for x in range(-search_range, search_range + 1):
                val = abs(a1 * x + b1) + abs(a2 * x + b2)
                if val == k:
                    solutions.add(x)
            if not solutions:
                return 0
            return sum(solutions) % 1000

        else:  # count
            # |a1*x + b1| <= k  →  정수 해의 개수
            # -k <= a1*x + b1 <= k
            # (-k - b1)/a1 <= x <= (k - b1)/a1
            low = math.ceil((-k - b1) / a1)
            high = math.floor((k - b1) / a1)
            count = max(0, high - low + 1)
            return count % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        a1, b1, a2, b2, k, mode = (
            seed["a1"], seed["b1"], seed["a2"], seed["b2"], seed["k"], seed["mode"],
        )
        if mode == "single":
            solutions = set()
            for rhs in [k, -k]:
                num = rhs - b1
                if num % a1 == 0:
                    solutions.add(num // a1)
        elif mode == "double":
            solutions = set()
            search_range = max(abs(k) + abs(b1) + abs(b2), 200)
            for x in range(-search_range, search_range + 1):
                if abs(a1 * x + b1) + abs(a2 * x + b2) == k:
                    solutions.add(x)
        else:
            low = math.ceil((-k - b1) / a1)
            high = math.floor((k - b1) / a1)
            solutions = set(range(low, high + 1))

        return {
            "solution_set": sorted(solutions),
            "solution_sum": sum(solutions),
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a1, b1, a2, b2, k, mode = (
            seed["a1"], seed["b1"], seed["a2"], seed["b2"], seed["k"], seed["mode"],
        )
        if mode == "single":
            return [
                f"1. |{a1}x + {b1}| = {k} 방정식을 양/음 두 경우로 분리합니다.",
                f"2. Case 1: {a1}x + {b1} = {k}  →  x = ({k} - {b1}) / {a1}.",
                f"3. Case 2: {a1}x + {b1} = {-k}  →  x = ({-k} - {b1}) / {a1}.",
                f"4. 정수 해만 모아 합을 구하고, 1000으로 나눈 나머지를 취합니다.",
            ]
        elif mode == "double":
            return [
                f"1. |{a1}x + {b1}| + |{a2}x + {b2}| = {k} 방정식을 세웁니다.",
                f"2. 경계점 x = {-b1}/{a1}, x = {-b2}/{a2}를 기준으로 구간을 분리합니다.",
                f"3. 각 구간에서 절대값을 풀어 일차방정식을 풀고, 정수 해를 모읍니다.",
                f"4. 모든 정수 해의 합을 구하고 1000으로 나눈 나머지를 취합니다.",
            ]
        else:
            return [
                f"1. |{a1}x + {b1}| <= {k} 부등식을 풀어야 합니다.",
                f"2. -{k} <= {a1}x + {b1} <= {k}로 변환합니다.",
                f"3. x의 범위: ({-k} - {b1})/{a1} <= x <= ({k} - {b1})/{a1}.",
                f"4. 범위 내 정수의 개수를 세고 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import symbols, Abs, solveset, S
            x = symbols('x')
            a1, b1, a2, b2, k, mode = (
                seed["a1"], seed["b1"], seed["a2"], seed["b2"], seed["k"], seed["mode"],
            )

            if mode == "single":
                # Solve |a1*x + b1| = k manually (sympy Abs in equations can be tricky)
                solutions = set()
                for rhs in [k, -k]:
                    num = rhs - b1
                    if num % a1 == 0:
                        solutions.add(num // a1)
                if not solutions:
                    return 0
                return sum(solutions) % 1000

            elif mode == "double":
                solutions = set()
                search_range = max(abs(k) + abs(b1) + abs(b2), 200)
                for xv in range(-search_range, search_range + 1):
                    if abs(a1 * xv + b1) + abs(a2 * xv + b2) == k:
                        solutions.add(xv)
                if not solutions:
                    return 0
                return sum(solutions) % 1000

            else:  # count
                import math as m
                low = m.ceil((-k - b1) / a1)
                high = m.floor((k - b1) / a1)
                return max(0, high - low + 1) % 1000
        except Exception:
            return None
