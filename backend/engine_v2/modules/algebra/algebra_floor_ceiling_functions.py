"""
AI_MathMate V2 — 바닥/천장 함수 (algebra_floor_ceiling_functions)
⌊x⌋ + ⌊2x⌋ + ⌊3x⌋ = n, Σ⌊k*sqrt(2)⌋, Hermite 항등식 등을 다룹니다.
기출 빈도: 24회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraFloorCeilingFunctionsModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_floor_ceiling_functions",
        name="바닥/천장 함수",
        domain="integer",
        namespace="alg_floor",
        input_schema={
            "multipliers": FieldSpec(dtype=list, domain="Z+", min_val=1, max_val=10, description="바닥 함수 내 x의 계수 리스트"),
            "irrational_type": FieldSpec(dtype=str, domain="str", description="무리수 유형: 'sqrt2' | 'sqrt3' | 'sqrt5' | 'rational'"),
            "n_upper": FieldSpec(dtype=int, domain="Z+", min_val=5, max_val=100, description="합산 상한 또는 목표 값"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'sum_floor' | 'floor_sum_irrational' | 'count_solutions'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답 mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=5,
        category="algebra",
        tags=["floor_function", "ceiling_function", "fractional_part", "hermite", "beatty_sequence"],
        exam_types=["AIME"],
        bridge_output_keys=["floor_sum_value", "fractional_parts"],
    )

    # 무리수 상수 맵
    _IRRATIONAL_MAP = {
        "sqrt2": math.sqrt(2),
        "sqrt3": math.sqrt(3),
        "sqrt5": math.sqrt(5),
        "rational": 1.0,  # placeholder, 실제 사용 시 분수로 처리
    }

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["sum_floor", "floor_sum_irrational", "count_solutions"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "sum_floor":
                # Σ_{k=1}^{n} ⌊k * p/q⌋  (유리수 p/q)
                p = random.randint(2, 9)
                q = random.randint(2, 9)
                while math.gcd(p, q) != 1 or p == q:
                    p = random.randint(2, 9)
                    q = random.randint(2, 9)
                n_upper = random.randint(10, 80) if difficulty_hint < 10 else random.randint(30, 100)
                multipliers = [p]
                irrational_type = "rational"
                seed = {
                    "multipliers": multipliers, "irrational_type": irrational_type,
                    "n_upper": n_upper, "mode": mode, "p": p, "q": q,
                }
            elif mode == "floor_sum_irrational":
                # Σ_{k=1}^{n} ⌊k * sqrt(d)⌋
                irr_type = random.choice(["sqrt2", "sqrt3", "sqrt5"])
                n_upper = random.randint(5, 50) if difficulty_hint < 10 else random.randint(20, 80)
                multipliers = [1]
                seed = {
                    "multipliers": multipliers, "irrational_type": irr_type,
                    "n_upper": n_upper, "mode": mode, "p": 0, "q": 1,
                }
            else:  # count_solutions
                # ⌊x⌋ + ⌊2x⌋ + ⌊3x⌋ = n  정수 해 개수 (x in [0, n_upper] 검색)
                mults = sorted(random.sample(range(1, 8), random.randint(2, 4)))
                target_n = random.randint(10, 200)
                n_upper = target_n
                multipliers = mults
                irrational_type = "rational"
                seed = {
                    "multipliers": multipliers, "irrational_type": irrational_type,
                    "n_upper": n_upper, "mode": mode, "p": 0, "q": 1,
                }

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {
            "multipliers": [1, 2, 3], "irrational_type": "rational",
            "n_upper": 20, "mode": "count_solutions", "p": 0, "q": 1,
        }

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]

        if mode == "sum_floor":
            # Σ_{k=1}^{n} ⌊k * p / q⌋
            p = seed["p"]
            q = seed["q"]
            n = seed["n_upper"]
            total = sum(math.floor(k * p / q) for k in range(1, n + 1))
            return total % 1000

        elif mode == "floor_sum_irrational":
            # Σ_{k=1}^{n} ⌊k * sqrt(d)⌋
            irr_val = self._IRRATIONAL_MAP[seed["irrational_type"]]
            n = seed["n_upper"]
            total = sum(math.floor(k * irr_val) for k in range(1, n + 1))
            return total % 1000

        else:  # count_solutions
            # ⌊m1*x⌋ + ⌊m2*x⌋ + ... = n_upper
            # x를 1/lcm 단위로 탐색 (유리수 x만 고려)
            multipliers = seed["multipliers"]
            target = seed["n_upper"]
            lcm_val = 1
            for m in multipliers:
                lcm_val = lcm_val * m // math.gcd(lcm_val, m)

            # 탐색 범위: x 는 [0, target/min(multipliers) + 1] 범위
            max_x_times_lcm = (target // min(multipliers) + 2) * lcm_val
            max_x_times_lcm = min(max_x_times_lcm, 10000)  # 안전 상한

            count = 0
            for xi in range(0, max_x_times_lcm + 1):
                x = xi / lcm_val
                s = sum(math.floor(m * x) for m in multipliers)
                if s == target:
                    count += 1

            return count % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        mode = seed["mode"]
        ans = self.execute(seed)

        if mode == "floor_sum_irrational":
            irr_val = self._IRRATIONAL_MAP[seed["irrational_type"]]
            n = seed["n_upper"]
            fractional_parts = [k * irr_val - math.floor(k * irr_val) for k in range(1, min(n + 1, 21))]
        else:
            fractional_parts = []

        return {
            "floor_sum_value": ans,
            "fractional_parts": fractional_parts,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]

        if mode == "sum_floor":
            p, q, n = seed["p"], seed["q"], seed["n_upper"]
            return [
                f"1. Σ_{{k=1}}^{{{n}}} ⌊k * {p}/{q}⌋을 계산해야 합니다.",
                f"2. 각 k에 대해 k*{p}/{q}의 바닥값을 구합니다.",
                f"3. Hermite/바닥 함수 합 공식을 활용하거나 직접 합산합니다.",
                f"4. 최종 합을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "floor_sum_irrational":
            irr = seed["irrational_type"]
            n = seed["n_upper"]
            irr_label = irr.replace("sqrt", "√")
            return [
                f"1. Σ_{{k=1}}^{{{n}}} ⌊k * {irr_label}⌋ (Beatty 수열의 합)을 계산합니다.",
                f"2. {irr_label}의 근삿값을 사용하여 각 항의 바닥값을 구합니다.",
                f"3. 모든 항을 합산합니다.",
                f"4. 결과를 1000으로 나눈 나머지를 취합니다.",
            ]
        else:
            mults = seed["multipliers"]
            target = seed["n_upper"]
            expr = " + ".join(f"⌊{m}x⌋" for m in mults)
            return [
                f"1. {expr} = {target}을 만족하는 실수 x의 개수를 구합니다.",
                f"2. 계수들의 LCM 단위로 x를 분할하여 각 구간을 분석합니다.",
                f"3. 각 x 후보에 대해 바닥 함수 합을 계산하여 일치 여부를 확인합니다.",
                f"4. 해의 총 개수를 세고 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            mode = seed["mode"]

            if mode == "sum_floor":
                from sympy import floor, Rational
                p, q, n = seed["p"], seed["q"], seed["n_upper"]
                total = sum(int(floor(k * Rational(p, q))) for k in range(1, n + 1))
                return total % 1000

            elif mode == "floor_sum_irrational":
                from sympy import floor, sqrt, N
                sqrt_map = {"sqrt2": 2, "sqrt3": 3, "sqrt5": 5}
                d = sqrt_map[seed["irrational_type"]]
                n = seed["n_upper"]
                irr_val = float(N(sqrt(d), 30))
                total = sum(int(math.floor(k * irr_val)) for k in range(1, n + 1))
                return total % 1000

            else:  # count_solutions
                # 동일 로직 재수행 (Branch B)
                multipliers = seed["multipliers"]
                target = seed["n_upper"]
                lcm_val = 1
                for m in multipliers:
                    lcm_val = lcm_val * m // math.gcd(lcm_val, m)
                max_xi = min((target // min(multipliers) + 2) * lcm_val, 10000)
                count = 0
                for xi in range(0, max_xi + 1):
                    x = xi / lcm_val
                    s = sum(math.floor(m * x) for m in multipliers)
                    if s == target:
                        count += 1
                return count % 1000
        except Exception:
            return None
