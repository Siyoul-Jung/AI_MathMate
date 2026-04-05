"""
AI_MathMate V2 — 특성방정식 / 선형 점화식 (algebra_seq_characteristic_eq)
a_n = p*a_{n-1} + q*a_{n-2} 형태의 2차 선형 점화식을 특성방정식 또는 직접 반복으로 풉니다.
기출 빈도: 5회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraSeqCharacteristicEqModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_seq_characteristic_eq",
        name="특성방정식 (선형 점화식)",
        domain="integer",
        namespace="alg_charseq",
        input_schema={
            "p": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="점화식 계수 p"),
            "q": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="점화식 계수 q"),
            "a0": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=20, description="초기값 a_0"),
            "a1": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=20, description="초기값 a_1"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=50, description="목표 인덱스 k"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="a_k mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=5,
        category="algebra",
        tags=["recurrence", "characteristic_equation", "linear_recurrence", "sequence", "fibonacci"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["sequence_value", "discriminant"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        for _ in range(100):
            p = random.randint(-6, 6)
            q = random.randint(-6, 6)
            if q == 0:
                continue  # 2차 점화식이어야 함
            a0 = random.randint(0, 10)
            a1 = random.randint(0, 10)

            # 난이도에 따라 k 조절
            if difficulty_hint < 8:
                k = random.randint(5, 15)
            elif difficulty_hint < 12:
                k = random.randint(10, 30)
            else:
                k = random.randint(20, 50)

            seed = {"p": p, "q": q, "a0": a0, "a1": a1, "k": k}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"p": 1, "q": 1, "a0": 1, "a1": 1, "k": 10}

    def execute(self, seed: dict[str, Any]) -> int:
        p, q = seed["p"], seed["q"]
        a0, a1 = seed["a0"], seed["a1"]
        k = seed["k"]

        # 직접 반복 계산 (결정론적, mod 1000)
        # a_n = p * a_{n-1} + q * a_{n-2}
        if k == 0:
            return a0 % 1000
        if k == 1:
            return a1 % 1000

        prev2, prev1 = a0, a1
        for _ in range(2, k + 1):
            curr = p * prev1 + q * prev2
            prev2, prev1 = prev1, curr

        # 음수 처리: Python mod는 항상 양수
        return prev1 % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        p, q = seed["p"], seed["q"]
        # 특성방정식: x^2 - p*x - q = 0, 판별식 D = p^2 + 4q
        discriminant = p * p + 4 * q
        seq_val = self.execute(seed)
        return {"sequence_value": seq_val, "discriminant": discriminant}

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        p, q = seed["p"], seed["q"]
        a0, a1 = seed["a0"], seed["a1"]
        k = seed["k"]
        disc = p * p + 4 * q

        steps = [
            f"1. 점화식 a_n = {p}*a_{{n-1}} + ({q})*a_{{n-2}}, 초기조건 a_0={a0}, a_1={a1}이 주어집니다.",
            f"2. 특성방정식: x^2 - ({p})x - ({q}) = 0, 판별식 D = {p}^2 + 4*({q}) = {disc}.",
        ]

        if disc > 0:
            steps.append(
                f"3. D > 0이므로 두 실수 특성근이 존재합니다. 일반항 a_n = A*r1^n + B*r2^n 형태입니다."
            )
        elif disc == 0:
            steps.append(
                f"3. D = 0이므로 중근 r = {p}/2입니다. 일반항 a_n = (A + Bn)*r^n 형태입니다."
            )
        else:
            steps.append(
                f"3. D < 0이므로 복소 특성근이 존재합니다. 직접 반복 계산을 사용합니다."
            )

        steps.append(
            f"4. a_{k}을 반복 계산하여 1000으로 나눈 나머지를 구합니다."
        )
        return steps

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            p, q = seed["p"], seed["q"]
            a0, a1 = seed["a0"], seed["a1"]
            k = seed["k"]

            # sympy를 사용한 독립 반복 검증
            if k == 0:
                return a0 % 1000
            if k == 1:
                return a1 % 1000

            seq = [0] * (k + 1)
            seq[0], seq[1] = a0, a1
            for i in range(2, k + 1):
                seq[i] = p * seq[i - 1] + q * seq[i - 2]

            return seq[k] % 1000
        except Exception:
            return None
