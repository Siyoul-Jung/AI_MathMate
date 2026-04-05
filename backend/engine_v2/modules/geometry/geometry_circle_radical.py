"""
AI_MathMate V2 — 근축 (geometry_circle_radical)
두 원의 근축(Radical Axis) 위 격자점에서의 거듭제곱(power) 값 합을 구합니다.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryCircleRadicalModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_circle_radical",
        name="근축 (Radical Axis)",
        domain="integer",
        namespace="geom_radical",
        input_schema={
            "h1": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="원1 중심 x"),
            "k1": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="원1 중심 y"),
            "r1": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=15, description="원1 반지름"),
            "h2": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="원2 중심 x"),
            "k2": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="원2 중심 y"),
            "r2": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=15, description="원2 반지름"),
            "x_lo": FieldSpec(dtype=int, domain="Z", min_val=-30, max_val=0, description="탐색 x 하한"),
            "x_hi": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=30, description="탐색 x 상한"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="power 절댓값 합 mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=8,
        category="geometry",
        tags=["radical_axis", "power_of_point", "circle", "lattice_points"],
        exam_types=["AIME"],
        bridge_output_keys=["power_sum", "radical_axis_coeff"],
    )

    @staticmethod
    def _radical_axis_coeffs(
        h1: int, k1: int, r1: int, h2: int, k2: int, r2: int
    ) -> tuple[int, int, int]:
        """
        근축 방정식: 2(h2-h1)x + 2(k2-k1)y = (h2^2 - h1^2) + (k2^2 - k1^2) - (r2^2 - r1^2)
        반환: (A, B, C) where Ax + By = C  (모두 정수)
        """
        A = 2 * (h2 - h1)
        B = 2 * (k2 - k1)
        C = (h2 ** 2 - h1 ** 2) + (k2 ** 2 - k1 ** 2) - (r2 ** 2 - r1 ** 2)
        return A, B, C

    def generate_seed(self, difficulty_hint: float = 9.0) -> dict[str, Any]:
        for _ in range(100):
            h1 = random.randint(-6, 6)
            k1 = random.randint(-6, 6)
            r1 = random.randint(2, 10)
            h2 = random.randint(-6, 6)
            k2 = random.randint(-6, 6)
            r2 = random.randint(2, 10)

            A, B, C = self._radical_axis_coeffs(h1, k1, r1, h2, k2, r2)

            # A == 0 이고 B == 0 이면 동심원 → 스킵
            if A == 0 and B == 0:
                continue

            x_lo = -20
            x_hi = 20

            seed = {
                "h1": h1, "k1": k1, "r1": r1,
                "h2": h2, "k2": k2, "r2": r2,
                "x_lo": x_lo, "x_hi": x_hi,
            }

            ans = self.execute(seed)
            if 0 <= ans <= 999 and ans > 0:
                return seed

        return {
            "h1": 0, "k1": 0, "r1": 5,
            "h2": 4, "k2": 0, "r2": 3,
            "x_lo": -20, "x_hi": 20,
        }

    def execute(self, seed: dict[str, Any]) -> int:
        h1, k1, r1 = seed["h1"], seed["k1"], seed["r1"]
        h2, k2, r2 = seed["h2"], seed["k2"], seed["r2"]
        x_lo, x_hi = seed["x_lo"], seed["x_hi"]

        A, B, C = self._radical_axis_coeffs(h1, k1, r1, h2, k2, r2)

        power_sum = 0
        # 근축: Ax + By = C
        # B != 0 이면 y = (C - Ax) / B — y가 정수인 x만 유효
        # B == 0 이면 x = C / A (상수), y 자유 → y 범위 내 모든 격자점

        if B != 0:
            for x in range(x_lo, x_hi + 1):
                num = C - A * x
                if num % B == 0:
                    y = num // B
                    power = (x - h1) ** 2 + (y - k1) ** 2 - r1 ** 2
                    power_sum += abs(power)
        elif A != 0:
            if C % A != 0:
                # 정수 x 해 없음
                return 0
            x_fixed = C // A
            if x_lo <= x_fixed <= x_hi:
                # y는 [-30, 30] 범위로 제한
                for y in range(-30, 31):
                    power = (x_fixed - h1) ** 2 + (y - k1) ** 2 - r1 ** 2
                    power_sum += abs(power)
        else:
            return 0

        return power_sum % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        h1, k1, r1 = seed["h1"], seed["k1"], seed["r1"]
        h2, k2, r2 = seed["h2"], seed["k2"], seed["r2"]
        A, B, C = self._radical_axis_coeffs(h1, k1, r1, h2, k2, r2)
        ans = self.execute(seed)
        return {
            "power_sum": ans,
            "radical_axis_coeff": [A, B, C],
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        h1, k1, r1 = seed["h1"], seed["k1"], seed["r1"]
        h2, k2, r2 = seed["h2"], seed["k2"], seed["r2"]
        x_lo, x_hi = seed["x_lo"], seed["x_hi"]
        A, B, C = self._radical_axis_coeffs(h1, k1, r1, h2, k2, r2)
        ans = self.execute(seed)

        return [
            f"1. 두 원 C1: (x-{h1})^2+(y-{k1})^2={r1}^2, C2: (x-{h2})^2+(y-{k2})^2={r2}^2의 근축을 구합니다.",
            f"2. 근축 방정식: {A}x + {B}y = {C}를 정리합니다 (두 원의 거듭제곱이 같은 점의 궤적).",
            f"3. x 범위 [{x_lo}, {x_hi}]에서 y가 정수인 격자점을 찾습니다.",
            f"4. 각 격자점에서의 power 절댓값 |(x-{h1})^2+(y-{k1})^2-{r1}^2|을 합산합니다.",
            f"5. 합 {ans}을 1000으로 나눈 나머지를 취합니다.",
        ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Integer
            h1, k1, r1 = Integer(seed["h1"]), Integer(seed["k1"]), Integer(seed["r1"])
            h2, k2, r2 = Integer(seed["h2"]), Integer(seed["k2"]), Integer(seed["r2"])
            x_lo, x_hi = seed["x_lo"], seed["x_hi"]

            A = 2 * (h2 - h1)
            B = 2 * (k2 - k1)
            C = (h2 ** 2 - h1 ** 2) + (k2 ** 2 - k1 ** 2) - (r2 ** 2 - r1 ** 2)

            power_sum = Integer(0)
            if B != 0:
                for x_val in range(x_lo, x_hi + 1):
                    x = Integer(x_val)
                    num = C - A * x
                    if num % B == 0:
                        y = num // B
                        power = (x - h1) ** 2 + (y - k1) ** 2 - r1 ** 2
                        power_sum += abs(power)
            elif A != 0:
                if C % A != 0:
                    return 0
                x = C // A
                if x_lo <= int(x) <= x_hi:
                    for y_val in range(-30, 31):
                        y = Integer(y_val)
                        power = (x - h1) ** 2 + (y - k1) ** 2 - r1 ** 2
                        power_sum += abs(power)
            else:
                return 0

            return int(power_sum % 1000)
        except Exception:
            return None
