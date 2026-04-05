"""
AI_MathMate V2 — 펠 방정식 (nt_diophantine_pell)
x² - Dy² = 1 (또는 = -1) 형태의 펠 방정식의 기본 해 및 k번째 해를 구합니다.
AIME 기출 3회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtDiophantinePellModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_diophantine_pell",
        name="펠 방정식",
        domain="integer",
        namespace="nt_pell",
        input_schema={
            "D": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=100, description="비완전제곱 양의 정수 D"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=6, description="k번째 해"),
            "mode": FieldSpec(dtype=str, domain="str", description="'x_value' | 'y_value' | 'sum_xy'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=5,
        daps_contribution=5.5,
        min_difficulty=8,
        category="number_theory",
        tags=["pell_equation", "continued_fraction", "quadratic_diophantine"],
        exam_types=["AIME"],
    )

    @staticmethod
    def _is_perfect_square(n: int) -> bool:
        if n < 0:
            return False
        s = int(math.isqrt(n))
        return s * s == n

    @staticmethod
    def _fundamental_solution(D: int) -> tuple[int, int]:
        """연분수 전개로 x² - Dy² = 1의 기본 해 (x1, y1)을 구합니다."""
        a0 = int(math.isqrt(D))
        if a0 * a0 == D:
            raise ValueError(f"D={D} is a perfect square")

        # 연분수 전개
        m, d, a = 0, 1, a0
        # 수렴분수의 분자/분모
        h_prev, h_curr = 1, a0
        k_prev, k_curr = 0, 1

        for _ in range(1000):
            m = d * a - m
            d = (D - m * m) // d
            a = (a0 + m) // d

            h_prev, h_curr = h_curr, a * h_curr + h_prev
            k_prev, k_curr = k_curr, a * k_curr + k_prev

            if h_curr * h_curr - D * k_curr * k_curr == 1:
                return h_curr, k_curr

        raise ValueError(f"Fundamental solution not found for D={D}")

    @staticmethod
    def _kth_solution(D: int, k: int) -> tuple[int, int]:
        """k번째 해를 기본 해의 거듭제곱으로 구합니다.
        (x_k + y_k√D) = (x1 + y1√D)^k"""
        x1, y1 = NtDiophantinePellModule._fundamental_solution(D)
        xk, yk = x1, y1
        for _ in range(k - 1):
            xk, yk = xk * x1 + D * yk * y1, xk * y1 + yk * x1
        return xk, yk

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        # D는 완전제곱이 아닌 수
        non_squares = [d for d in range(2, 101) if not self._is_perfect_square(d)]
        modes = ["x_value", "y_value", "sum_xy"]

        for _ in range(100):
            D = random.choice(non_squares)
            k = random.randint(1, 4) if difficulty_hint < 12 else random.randint(2, 6)
            mode = random.choice(modes)
            seed = {"D": D, "k": k, "mode": mode}
            try:
                ans = self.execute(seed)
                if 0 <= ans <= 999:
                    return seed
            except (ValueError, OverflowError):
                continue

        return {"D": 2, "k": 1, "mode": "x_value"}

    def execute(self, seed: dict[str, Any]) -> int:
        D, k, mode = seed["D"], seed["k"], seed["mode"]
        xk, yk = self._kth_solution(D, k)

        if mode == "x_value":
            return xk % 1000
        elif mode == "y_value":
            return yk % 1000
        else:  # sum_xy
            return (xk + yk) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        D, k, mode = seed["D"], seed["k"], seed["mode"]
        x1, y1 = self._fundamental_solution(D)
        xk, yk = self._kth_solution(D, k)

        steps = [
            f"1. 펠 방정식 x² - {D}y² = 1을 세웁니다.",
            f"2. √{D}의 연분수 전개로 기본 해 (x₁, y₁) = ({x1}, {y1})을 구합니다.",
            f"3. 검증: {x1}² - {D} × {y1}² = {x1**2} - {D * y1**2} = {x1**2 - D * y1**2}.",
        ]
        if k > 1:
            steps.append(f"4. (x₁ + y₁√{D})^{k}을 전개하여 {k}번째 해 ({xk}, {yk})를 구합니다.")
        if mode == "x_value":
            steps.append(f"{'5' if k > 1 else '4'}. x = {xk}을 1000으로 나눈 나머지를 구합니다.")
        elif mode == "y_value":
            steps.append(f"{'5' if k > 1 else '4'}. y = {yk}를 1000으로 나눈 나머지를 구합니다.")
        else:
            steps.append(f"{'5' if k > 1 else '4'}. x + y = {xk + yk}를 1000으로 나눈 나머지를 구합니다.")
        return steps

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            D, k, mode = seed["D"], seed["k"], seed["mode"]
            xk, yk = self._kth_solution(D, k)
            # 독립 검증: x² - Dy² = 1 확인
            assert xk * xk - D * yk * yk == 1, f"Pell verification failed: {xk}^2 - {D}*{yk}^2 != 1"

            if mode == "x_value":
                return xk % 1000
            elif mode == "y_value":
                return yk % 1000
            else:
                return (xk + yk) % 1000
        except Exception:
            return None
