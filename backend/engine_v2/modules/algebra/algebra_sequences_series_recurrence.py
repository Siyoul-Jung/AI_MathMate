"""
AI_MathMate V2 — 수열/급수/점화식 (algebra_sequences_series_recurrence)
등차·등비 수열의 합, 선형 점화식 a_{n+1} = p*a_n + q 를 다룹니다.
기출 빈도: 143회 (최빈출)
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraSequencesSeriesRecurrenceModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_sequences_series_recurrence",
        name="수열/급수/점화식",
        domain="integer",
        namespace="alg_seq",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'arithmetic' | 'geometric' | 'recurrence'"),
            "a1": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=50, description="초항"),
            "d_or_r": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="공차(등차) 또는 공비(등비)"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=5, max_val=80, description="항 번호 또는 부분합 개수"),
            "p": FieldSpec(dtype=int, domain="Z", min_val=1, max_val=5, description="점화식 계수 p (recurrence 모드)"),
            "q": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="점화식 상수 q (recurrence 모드)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답 (mod 1000)"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=3,
        category="algebra",
        tags=["arithmetic_sequence", "geometric_sequence", "recurrence", "partial_sum", "series"],
        exam_types=["AIME", "AMC"],
    )

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["arithmetic", "geometric", "recurrence"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "arithmetic":
                a1 = random.randint(1, 50)
                d = random.randint(1, 20) * random.choice([-1, 1])
                n = random.randint(10, 80) if difficulty_hint >= 9 else random.randint(5, 40)
                seed = {"mode": mode, "a1": a1, "d_or_r": d, "n": n, "p": 1, "q": 0}

            elif mode == "geometric":
                a1 = random.randint(1, 10)
                r = random.randint(2, 4)
                # n 을 작게 잡아야 0~999 범위 맞추기 쉬움
                n = random.randint(3, 8) if difficulty_hint < 10 else random.randint(5, 10)
                seed = {"mode": mode, "a1": a1, "d_or_r": r, "n": n, "p": 1, "q": 0}

            else:  # recurrence
                a1 = random.randint(1, 10)
                p = random.randint(2, 5)
                q = random.randint(-10, 10)
                n = random.randint(5, 15)
                seed = {"mode": mode, "a1": a1, "d_or_r": 0, "n": n, "p": p, "q": q}

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"mode": "arithmetic", "a1": 3, "d_or_r": 5, "n": 10, "p": 1, "q": 0}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        a1 = seed["a1"]
        n = seed["n"]

        if mode == "arithmetic":
            d = seed["d_or_r"]
            # 부분합 S_n = n/2 * (2*a1 + (n-1)*d)
            s_n = n * (2 * a1 + (n - 1) * d) // 2
            return abs(s_n) % 1000

        elif mode == "geometric":
            r = seed["d_or_r"]
            if r == 1:
                s_n = a1 * n
            else:
                # S_n = a1 * (r^n - 1) / (r - 1)
                s_n = a1 * (r ** n - 1) // (r - 1)
            return abs(s_n) % 1000

        else:  # recurrence: a_{k+1} = p*a_k + q, 구하는 것 = a_n mod 1000
            p = seed["p"]
            q = seed["q"]
            a_k = a1
            for _ in range(n - 1):
                a_k = p * a_k + q
            return abs(a_k) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        a1 = seed["a1"]
        n = seed["n"]

        if mode == "arithmetic":
            d = seed["d_or_r"]
            return [
                f"1. 초항 a_1 = {a1}, 공차 d = {d}인 등차수열을 정의합니다.",
                f"2. 일반항: a_n = {a1} + (n-1)*{d}를 확인합니다.",
                f"3. 부분합 공식 S_{n} = {n}/2 * (2*{a1} + ({n}-1)*{d})를 적용합니다.",
                f"4. 계산 결과의 절댓값을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "geometric":
            r = seed["d_or_r"]
            return [
                f"1. 초항 a_1 = {a1}, 공비 r = {r}인 등비수열을 정의합니다.",
                f"2. 부분합 공식 S_{n} = {a1} * ({r}^{n} - 1) / ({r} - 1)을 적용합니다.",
                f"3. {r}^{n}을 계산하고 분수를 정리합니다.",
                f"4. 결과의 절댓값을 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            p, q = seed["p"], seed["q"]
            return [
                f"1. 점화식 a_{{k+1}} = {p}*a_k + {q}, 초항 a_1 = {a1}을 정의합니다.",
                f"2. a_2 = {p}*{a1} + {q} = {p * a1 + q}부터 순차적으로 계산합니다.",
                f"3. n = {n}까지 반복하여 a_{n}을 구합니다.",
                f"4. 결과의 절댓값을 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            mode = seed["mode"]
            a1 = seed["a1"]
            n = seed["n"]

            if mode == "arithmetic":
                d = seed["d_or_r"]
                from sympy import Rational
                s_n = Rational(n, 1) * (2 * a1 + (n - 1) * d) / 2
                return abs(int(s_n)) % 1000

            elif mode == "geometric":
                r = seed["d_or_r"]
                if r == 1:
                    s_n = a1 * n
                else:
                    from sympy import Rational
                    s_n = Rational(a1, 1) * (r ** n - 1) / (r - 1)
                    s_n = int(s_n)
                return abs(s_n) % 1000

            else:
                p, q = seed["p"], seed["q"]
                a_k = a1
                for _ in range(n - 1):
                    a_k = p * a_k + q
                return abs(a_k) % 1000
        except Exception:
            return None
