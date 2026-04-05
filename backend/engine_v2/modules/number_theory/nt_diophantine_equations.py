"""
AI_MathMate V2 — 디오판토스 방정식 (nt_diophantine_equations)
ax + by = c 형태의 선형 디오판토스 방정식: 해의 존재, 최소 양수 해, 양수 해의 개수.
AIME 기출 110회. Bridge 타겟 모듈.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtDiophantineEquationsModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_diophantine_equations",
        name="디오판토스 방정식",
        domain="integer",
        namespace="nt_diophantine",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=200, description="계수 a"),
            "b": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=200, description="계수 b"),
            "c": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=50000, description="우변 상수 c"),
            "mode": FieldSpec(dtype=str, domain="str", description="'positive_count' | 'min_positive_x' | 'sum_all_x'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=5,
        category="number_theory",
        tags=["diophantine", "linear_equation", "gcd", "integer_solutions"],
        exam_types=["AIME"],
        bridge_input_accepts=["polynomial_value", "factored_sum"],
    )

    @staticmethod
    def _ext_gcd(a: int, b: int) -> tuple[int, int, int]:
        if b == 0:
            return a, 1, 0
        g, x1, y1 = NtDiophantineEquationsModule._ext_gcd(b, a % b)
        return g, y1, x1 - (a // b) * y1

    @staticmethod
    def _solve(a: int, b: int, c: int) -> tuple[int, int, int, int] | None:
        """ax + by = c 의 일반해: x = x0 + (b/g)*t, y = y0 - (a/g)*t.
        Returns (x0, y0, step_x, step_y) or None if no solution."""
        g, px, py = NtDiophantineEquationsModule._ext_gcd(a, b)
        if c % g != 0:
            return None
        scale = c // g
        x0 = px * scale
        y0 = py * scale
        step_x = b // g   # x 증가분
        step_y = a // g   # y 감소분
        return x0, y0, step_x, step_y

    @staticmethod
    def _positive_solutions(a: int, b: int, c: int) -> list[tuple[int, int]]:
        """ax + by = c 의 양수 해 (x > 0, y > 0) 전부를 반환."""
        result = NtDiophantineEquationsModule._solve(a, b, c)
        if result is None:
            return []
        x0, y0, step_x, step_y = result
        solutions = []
        # x > 0 조건: x0 + step_x * t > 0
        # y > 0 조건: y0 - step_y * t > 0
        if step_x > 0:
            t_min = math.ceil((1 - x0) / step_x) if x0 < 1 else (
                -((x0 - 1) // step_x)
            )
            t_max = (y0 - 1) // step_y if step_y > 0 else 10**9
        else:
            return []

        # x > 0 조건에서 t의 하한
        if x0 >= 1:
            t_min = -((x0 - 1) // step_x)
        else:
            t_min = math.ceil((1 - x0) / step_x)

        # y > 0 조건에서 t의 상한
        if step_y > 0:
            t_max = (y0 - 1) // step_y
        else:
            t_max = 10**6  # y always positive if step_y <= 0

        for t in range(t_min, t_max + 1):
            x = x0 + step_x * t
            y = y0 - step_y * t
            if x > 0 and y > 0:
                solutions.append((x, y))
            if len(solutions) > 2000:
                break
        return solutions

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["positive_count", "min_positive_x", "sum_all_x"]
        for _ in range(100):
            mode = random.choice(modes)
            a = random.randint(3, 80) if difficulty_hint < 10 else random.randint(10, 200)
            b = random.randint(3, 80) if difficulty_hint < 10 else random.randint(10, 200)
            g = math.gcd(a, b)
            # c는 gcd(a,b)의 배수여야 해가 존재
            multiplier = random.randint(5, 200)
            c = g * multiplier

            seed = {"a": a, "b": b, "c": c, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999 and ans > 0:
                return seed

        return {"a": 7, "b": 11, "c": 300, "mode": "positive_count"}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]

        if mode == "positive_count":
            sols = self._positive_solutions(a, b, c)
            return len(sols) % 1000

        elif mode == "min_positive_x":
            sols = self._positive_solutions(a, b, c)
            if not sols:
                return 0
            return min(x for x, y in sols) % 1000

        else:  # sum_all_x
            sols = self._positive_solutions(a, b, c)
            total = sum(x for x, y in sols)
            return total % 1000

    def generate_seed_with_bridge(self, bridge: dict[str, Any], difficulty_hint: float = 8.0) -> dict[str, Any]:
        """Bridge 입력 (polynomial_value, factored_sum)으로부터 c 값을 도출."""
        c_candidate = bridge.get("polynomial_value") or bridge.get("factored_sum") or 300
        c_candidate = abs(int(c_candidate))
        if c_candidate < 10:
            c_candidate = c_candidate * 50 + 100

        for _ in range(100):
            a = random.randint(3, 80)
            b = random.randint(3, 80)
            g = math.gcd(a, b)
            # c를 gcd의 배수로 맞춤
            c = (c_candidate // g) * g
            if c < g:
                c = g * 10
            mode = random.choice(["positive_count", "min_positive_x", "sum_all_x"])
            seed = {"a": a, "b": b, "c": c, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999 and ans > 0:
                return seed

        return {"a": 7, "b": 11, "c": 300, "mode": "positive_count"}

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, c, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
        g = math.gcd(a, b)
        steps = [
            f"1. 디오판토스 방정식 {a}x + {b}y = {c}를 세웁니다.",
            f"2. gcd({a}, {b}) = {g}이고, {c}가 {g}의 배수인지 확인합니다 ({c} / {g} = {c // g}).",
            f"3. 확장 유클리드로 특수해 (x₀, y₀)를 구합니다.",
        ]
        if mode == "positive_count":
            sols = self._positive_solutions(a, b, c)
            steps.append(f"4. x > 0, y > 0 조건을 만족하는 해의 개수: {len(sols)}개, mod 1000을 취합니다.")
        elif mode == "min_positive_x":
            steps.append(f"4. 일반해에서 x > 0인 최소값을 구하고 1000으로 나눈 나머지를 취합니다.")
        else:
            sols = self._positive_solutions(a, b, c)
            steps.append(f"4. 모든 양수 해의 x값의 합: {sum(x for x, y in sols)}, mod 1000을 취합니다.")
        return steps

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import symbols, diophantine
            from sympy import Eq
            a_val, b_val, c_val, mode = seed["a"], seed["b"], seed["c"], seed["mode"]
            x, y = symbols('x y', integer=True)

            # sympy diophantine returns parametric solutions; use our own independent impl
            g = math.gcd(a_val, b_val)
            if c_val % g != 0:
                return 0

            # Independent brute approach for verification (bounded)
            if mode == "positive_count":
                count = 0
                max_x = c_val // a_val + 1
                for xv in range(1, max_x + 1):
                    rem = c_val - a_val * xv
                    if rem > 0 and rem % b_val == 0:
                        count += 1
                return count % 1000
            elif mode == "min_positive_x":
                max_x = c_val // a_val + 1
                for xv in range(1, max_x + 1):
                    rem = c_val - a_val * xv
                    if rem > 0 and rem % b_val == 0:
                        return xv % 1000
                return 0
            else:  # sum_all_x
                total = 0
                max_x = c_val // a_val + 1
                for xv in range(1, max_x + 1):
                    rem = c_val - a_val * xv
                    if rem > 0 and rem % b_val == 0:
                        total += xv
                return total % 1000
        except Exception:
            return None
