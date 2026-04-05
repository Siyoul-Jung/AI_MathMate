"""
AI_MathMate V2 -- comb_prob_transition_matrix (전이 행렬 / Transition Matrix)
유한 상태 마르코프 체인의 전이 행렬을 n번 거듭제곱하여 n단계 후의 확률을 구합니다.
기출 2회 (AIME).
"""
from __future__ import annotations
import random
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombProbTransitionMatrixModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_prob_transition_matrix",
        name="전이 행렬 (Transition Matrix Power)",
        domain="integer",
        namespace="comb_trans_matrix",
        input_schema={
            "n_steps": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=20, description="전이 단계 수"),
            "mode": FieldSpec(dtype=str, domain="str", description="'two_state' | 'three_state'"),
            "p_num": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=5, description="전이 확률 분자"),
            "p_den": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=6, description="전이 확률 분모"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="p+q 기약분수"),
        },
        logic_depth=5,
        daps_contribution=5.0,
        min_difficulty=9,
        category="combinatorics",
        tags=["transition_matrix", "matrix_power", "markov_chain", "probability"],
        exam_types=["AIME"],
        bridge_output_keys=["n_steps", "transition_result"],
        bridge_input_accepts=["n_states"],
    )

    @staticmethod
    def _mat_mul_frac(A: list[list[Fraction]], B: list[list[Fraction]]) -> list[list[Fraction]]:
        """Fraction 행렬 곱셈"""
        n = len(A)
        m = len(B[0])
        k = len(B)
        result = [[Fraction(0)] * m for _ in range(n)]
        for i in range(n):
            for j in range(m):
                for l in range(k):
                    result[i][j] += A[i][l] * B[l][j]
        return result

    @staticmethod
    def _mat_pow_frac(M: list[list[Fraction]], exp: int) -> list[list[Fraction]]:
        """Fraction 행렬 거듭제곱 (빠른 거듭제곱)"""
        n = len(M)
        # 단위 행렬
        result = [[Fraction(1) if i == j else Fraction(0) for j in range(n)] for i in range(n)]
        base = [row[:] for row in M]
        while exp > 0:
            if exp % 2 == 1:
                result = CombProbTransitionMatrixModule._mat_mul_frac(result, base)
            base = CombProbTransitionMatrixModule._mat_mul_frac(base, base)
            exp //= 2
        return result

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["two_state", "three_state"]
        for _ in range(100):
            mode = random.choice(modes)
            p_den = random.randint(2, 6)
            p_num = random.randint(1, p_den - 1)
            if difficulty_hint < 10:
                n_steps = random.randint(2, 10)
            else:
                n_steps = random.randint(5, 20)

            seed = {"n_steps": n_steps, "mode": mode, "p_num": p_num, "p_den": p_den}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n_steps": 4, "mode": "two_state", "p_num": 1, "p_den": 3}

    def execute(self, seed: dict[str, Any]) -> int:
        n_steps = seed["n_steps"]
        mode = seed["mode"]
        p = Fraction(seed["p_num"], seed["p_den"])
        q = Fraction(1) - p

        if mode == "two_state":
            # 2상태 마르코프: 상태 A, B
            # A->A: p, A->B: 1-p, B->A: 1-p, B->B: p
            M = [
                [p, Fraction(1) - p],
                [Fraction(1) - p, p],
            ]
            result = self._mat_pow_frac(M, n_steps)
            # 상태 A에서 시작, n단계 후 상태 A에 있을 확률
            prob = result[0][0]

        else:  # three_state
            # 3상태 순환: A->B: p, A->A: 1-p, B->C: p, B->B: 1-p, C->A: p, C->C: 1-p
            M = [
                [q, p, Fraction(0)],
                [Fraction(0), q, p],
                [p, Fraction(0), q],
            ]
            result = self._mat_pow_frac(M, n_steps)
            # 상태 A에서 시작, n단계 후 상태 A에 있을 확률
            prob = result[0][0]

        return int(prob.numerator + prob.denominator)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n_steps = seed["n_steps"]
        mode = seed["mode"]
        p = Fraction(seed["p_num"], seed["p_den"])

        if mode == "two_state":
            return [
                f"1. 2상태 마르코프 체인: 전이 확률 p = {p}으로 설정합니다.",
                f"2. 전이 행렬 T = [[{p}, {1-p}], [{1-p}, {p}]]를 구성합니다.",
                f"3. T^{n_steps}를 행렬 거듭제곱으로 계산합니다.",
                f"4. 상태 A에서 시작하여 {n_steps}단계 후 A에 있을 확률을 기약분수로 구하고 p+q를 답합니다.",
            ]
        else:
            return [
                f"1. 3상태 순환 마르코프 체인: 전이 확률 p = {p}으로 설정합니다.",
                f"2. 3x3 전이 행렬 T를 구성합니다 (A->B, B->C, C->A 순환).",
                f"3. T^{n_steps}를 빠른 거듭제곱으로 계산합니다.",
                f"4. (0,0) 성분에서 기약분수를 추출하고 p+q를 답합니다.",
                f"5. 행렬 거듭제곱의 닫힌 형태를 고유값 분해로 검증합니다.",
            ]

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        """n_steps와 transition_result(execute 결과)를 하류 모듈에 전달."""
        ans = self.execute(seed)
        return {
            "n_steps": seed["n_steps"],
            "transition_result": ans,
        }

    def generate_seed_with_bridge(
        self, bridge: dict[str, Any], difficulty_hint: float = 10.0
    ) -> dict[str, Any]:
        """상위 모듈의 n_states를 받아 mode를 결정 (n_states<=3 → two_state, 그 외 three_state)."""
        n_states = bridge.get("n_states")
        if n_states is not None:
            n_states = int(n_states)
            mode = "two_state" if n_states <= 3 else "three_state"
        else:
            mode = random.choice(["two_state", "three_state"])

        for _ in range(100):
            p_den = random.randint(2, 6)
            p_num = random.randint(1, p_den - 1)
            if difficulty_hint < 10:
                n_steps = random.randint(2, 10)
            else:
                n_steps = random.randint(5, 20)

            seed = {"n_steps": n_steps, "mode": mode, "p_num": p_num, "p_den": p_den}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n_steps": 4, "mode": mode, "p_num": 1, "p_den": 3}

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Matrix, Rational
            n_steps = seed["n_steps"]
            mode = seed["mode"]
            p = Rational(seed["p_num"], seed["p_den"])
            q = 1 - p

            if mode == "two_state":
                M = Matrix([[p, 1 - p], [1 - p, p]])
            else:
                M = Matrix([
                    [q, p, 0],
                    [0, q, p],
                    [p, 0, q],
                ])

            result = M ** n_steps
            prob = result[0, 0]
            return int(prob.p + prob.q)
        except Exception:
            return None
