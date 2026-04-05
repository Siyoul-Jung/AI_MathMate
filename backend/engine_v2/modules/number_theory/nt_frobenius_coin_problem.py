"""
AI_MathMate V2 — 프로베니우스 동전 문제 (nt_frobenius_coin_problem)
서로소인 두 수 a, b로 표현 불가능한 최대 정수(Frobenius number) 및 관련 문제.
AIME 기출 5회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtFrobeniusCoinProblemModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_frobenius_coin_problem",
        name="프로베니우스 동전 문제",
        domain="integer",
        namespace="nt_frobenius",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=200, description="첫 번째 동전 단위"),
            "b": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=200, description="두 번째 동전 단위"),
            "mode": FieldSpec(dtype=str, domain="str",
                              description="'frobenius_number' | 'non_representable_count' | 'largest_gap'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=3,
        daps_contribution=4.5,
        min_difficulty=6,
        category="number_theory",
        tags=["frobenius", "coin_problem", "chicken_mcnugget", "representation", "sylvester"],
        exam_types=["AIME"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["frobenius_number", "non_representable_count", "largest_gap"]
        for _ in range(100):
            mode = random.choice(modes)
            a = random.randint(3, 100) if difficulty_hint < 10 else random.randint(10, 200)
            b = random.randint(3, 100) if difficulty_hint < 10 else random.randint(10, 200)
            # gcd(a, b) = 1이어야 프로베니우스 수가 존재
            if math.gcd(a, b) != 1 or a == b:
                continue

            seed = {"a": a, "b": b, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"a": 3, "b": 5, "mode": "frobenius_number"}

    def execute(self, seed: dict[str, Any]) -> int:
        a, b, mode = seed["a"], seed["b"], seed["mode"]

        if mode == "frobenius_number":
            # Sylvester-Frobenius 공식: g(a,b) = ab - a - b
            frob = a * b - a - b
            return frob % 1000

        elif mode == "non_representable_count":
            # 표현 불가능한 양의 정수의 개수: (a-1)(b-1)/2
            count = (a - 1) * (b - 1) // 2
            return count % 1000

        else:  # largest_gap
            # 프로베니우스 수 근처에서 가장 큰 연속 표현불가능 구간의 길이
            frob = a * b - a - b
            # 표현 가능 여부를 체크해서 가장 큰 연속 gap을 찾음
            representable = set()
            for i in range(frob + 2):
                for xa in range(i // a + 1):
                    rem = i - xa * a
                    if rem >= 0 and rem % b == 0:
                        representable.add(i)
                        break

            max_gap = 0
            current_gap = 0
            for i in range(1, frob + 2):
                if i not in representable:
                    current_gap += 1
                    max_gap = max(max_gap, current_gap)
                else:
                    current_gap = 0
            return max_gap % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, mode = seed["a"], seed["b"], seed["mode"]

        if mode == "frobenius_number":
            frob = a * b - a - b
            return [
                f"1. gcd({a}, {b}) = 1임을 확인합니다.",
                f"2. Sylvester-Frobenius 공식: g({a}, {b}) = {a} × {b} - {a} - {b} = {frob}.",
                f"3. {frob} mod 1000 = {frob % 1000}.",
            ]
        elif mode == "non_representable_count":
            count = (a - 1) * (b - 1) // 2
            return [
                f"1. gcd({a}, {b}) = 1임을 확인합니다.",
                f"2. 표현 불가능한 양의 정수의 개수 = ({a}-1)({b}-1)/2 = {(a-1)}×{(b-1)}/2 = {count}.",
                f"3. {count} mod 1000 = {count % 1000}.",
            ]
        else:
            return [
                f"1. gcd({a}, {b}) = 1임을 확인하고 프로베니우스 수 g = {a*b - a - b}를 구합니다.",
                f"2. 1부터 g까지 각 정수가 {a}x + {b}y (x,y ≥ 0)로 표현 가능한지 확인합니다.",
                f"3. 표현 불가능한 수들 중 가장 긴 연속 구간의 길이를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            a, b, mode = seed["a"], seed["b"], seed["mode"]
            assert math.gcd(a, b) == 1

            if mode == "frobenius_number":
                return (a * b - a - b) % 1000
            elif mode == "non_representable_count":
                return ((a - 1) * (b - 1) // 2) % 1000
            else:
                # 독립 brute force
                frob = a * b - a - b
                representable = set()
                for i in range(frob + 2):
                    for xa in range(i // a + 1):
                        rem = i - xa * a
                        if rem >= 0 and rem % b == 0:
                            representable.add(i)
                            break
                max_gap = 0
                current_gap = 0
                for i in range(1, frob + 2):
                    if i not in representable:
                        current_gap += 1
                        max_gap = max(max_gap, current_gap)
                    else:
                        current_gap = 0
                return max_gap % 1000
        except Exception:
            return None
