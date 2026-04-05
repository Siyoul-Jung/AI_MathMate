"""
AI_MathMate V2 — 속도/거리/시간 및 일(Work) 문제 (algebra_kinematics)
두 객체의 속도·거리·시간 관계, 만남/추월 문제, 공동 작업 문제를 다룹니다.
기출 빈도: 48회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraKinematicsModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_kinematics",
        name="속도/거리/시간 및 일 문제",
        domain="integer",
        namespace="alg_kine",
        input_schema={
            "v1": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=100, description="객체 1 속도"),
            "v2": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=100, description="객체 2 속도"),
            "d": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=500, description="거리"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'meet' | 'chase' | 'work'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="분자+분모 합 (mod 1000)"),
        },
        logic_depth=4,
        daps_contribution=3.5,
        min_difficulty=3,
        category="algebra",
        tags=["speed", "distance", "time", "rate", "work_problem", "kinematics"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["meeting_time_num", "meeting_time_den"],
    )

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        modes = ["meet", "chase", "work"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "meet":
                # 두 객체가 마주보고 출발, 만나는 시간 = d / (v1 + v2)
                v1 = random.randint(3, 60)
                v2 = random.randint(3, 60)
                d = random.randint(20, 400)
            elif mode == "chase":
                # 추월 문제: 같은 방향, 만나는 시간 = d / |v1 - v2|
                v1 = random.randint(10, 80)
                v2 = random.randint(3, v1 - 1)  # v1 > v2 보장
                d = random.randint(10, 300)
            else:
                # 공동 작업: A가 v1시간, B가 v2시간에 완료 → 함께 하면 d단위 작업 시간
                # 시간 = d / (d/v1 + d/v2) = v1*v2/(v1+v2) 로 단순화, d는 작업량
                v1 = random.randint(2, 50)
                v2 = random.randint(2, 50)
                d = random.randint(1, 20)

            seed = {"v1": v1, "v2": v2, "d": d, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"v1": 10, "v2": 15, "d": 100, "mode": "meet"}

    def execute(self, seed: dict[str, Any]) -> int:
        v1, v2, d, mode = seed["v1"], seed["v2"], seed["d"], seed["mode"]

        if mode == "meet":
            # 만나는 시간 = d / (v1 + v2) → 기약분수의 분자+분모
            g = math.gcd(d, v1 + v2)
            num = d // g
            den = (v1 + v2) // g
            return (num + den) % 1000

        elif mode == "chase":
            # 추월 시간 = d / (v1 - v2) → 기약분수의 분자+분모
            diff = v1 - v2
            if diff <= 0:
                return 0
            g = math.gcd(d, diff)
            num = d // g
            den = diff // g
            return (num + den) % 1000

        else:  # work
            # 공동 작업 시간 for d units: rate = 1/v1 + 1/v2 = (v1+v2)/(v1*v2)
            # 시간 = d / rate = d * v1 * v2 / (v1 + v2) → 기약분수의 분자+분모
            numerator = d * v1 * v2
            denominator = v1 + v2
            g = math.gcd(numerator, denominator)
            num = numerator // g
            den = denominator // g
            return (num + den) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        v1, v2, d, mode = seed["v1"], seed["v2"], seed["d"], seed["mode"]
        if mode == "meet":
            g = math.gcd(d, v1 + v2)
            return {"meeting_time_num": d // g, "meeting_time_den": (v1 + v2) // g}
        elif mode == "chase":
            diff = max(v1 - v2, 1)
            g = math.gcd(d, diff)
            return {"meeting_time_num": d // g, "meeting_time_den": diff // g}
        else:
            numerator = d * v1 * v2
            denominator = v1 + v2
            g = math.gcd(numerator, denominator)
            return {"meeting_time_num": numerator // g, "meeting_time_den": denominator // g}

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        v1, v2, d, mode = seed["v1"], seed["v2"], seed["d"], seed["mode"]

        if mode == "meet":
            s = v1 + v2
            g = math.gcd(d, s)
            return [
                f"1. 두 객체가 마주보고 출발합니다. 속도는 각각 {v1}, {v2}입니다.",
                f"2. 상대 속도는 {v1} + {v2} = {s}입니다.",
                f"3. 만나는 시간 = {d}/{s}을 기약분수로 변환합니다 (GCD={g}).",
                f"4. 기약분수 {d // g}/{s // g}의 분자+분모 합을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "chase":
            diff = v1 - v2
            g = math.gcd(d, diff)
            return [
                f"1. 두 객체가 같은 방향으로 출발합니다. 속도 {v1}이(가) {v2}보다 빠릅니다.",
                f"2. 상대 속도는 {v1} - {v2} = {diff}입니다.",
                f"3. 추월 시간 = {d}/{diff}을 기약분수로 변환합니다 (GCD={g}).",
                f"4. 기약분수 {d // g}/{diff // g}의 분자+분모 합을 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            num = d * v1 * v2
            den = v1 + v2
            g = math.gcd(num, den)
            return [
                f"1. A는 {v1}시간, B는 {v2}시간에 단위 작업을 완료합니다.",
                f"2. 합산 작업률 = 1/{v1} + 1/{v2} = {v1 + v2}/({v1}*{v2})입니다.",
                f"3. {d}단위 작업의 공동 소요 시간 = {num}/{den}을 기약분수로 변환합니다.",
                f"4. 기약분수 {num // g}/{den // g}의 분자+분모 합을 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Rational
            v1, v2, d, mode = seed["v1"], seed["v2"], seed["d"], seed["mode"]

            if mode == "meet":
                t = Rational(d, v1 + v2)
            elif mode == "chase":
                diff = v1 - v2
                if diff <= 0:
                    return 0
                t = Rational(d, diff)
            else:
                t = Rational(d * v1 * v2, v1 + v2)

            return (int(t.p) + int(t.q)) % 1000
        except Exception:
            return None
