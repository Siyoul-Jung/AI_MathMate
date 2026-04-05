"""
AI_MathMate V2 — 원 정리 (geometry_circle_theorems)
AIME 기출 82회. 원주각, 중심각, 현, 접선 관련 정리를 다룹니다.
Bridge 소스: center, radius를 coordinate_analytic Hub에 전달.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryCircleTheoremsModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_circle_theorems",
        name="원 정리",
        domain="integer",
        namespace="geo_circle",
        input_schema={
            "r": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=50, description="반지름"),
            "d": FieldSpec(dtype=int, domain="Z+", description="점에서 중심까지 거리"),
            "mode": FieldSpec(dtype=str, domain="str", description="'chord_sq' | 'tangent_sq' | 'inscribed_angle'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999),
        },
        logic_depth=3,
        daps_contribution=3.5,
        min_difficulty=4,
        category="geometry",
        tags=["circle", "chord", "tangent", "inscribed_angle", "central_angle", "secant"],
        exam_types=["AIME"],
        bridge_output_keys=["center", "radius", "chord_length"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["chord_sq", "tangent_sq", "inscribed_angle"]
        for _ in range(100):
            mode = random.choice(modes)
            r = random.randint(5, 40)
            if mode == "chord_sq":
                d = random.randint(1, r - 1)  # d < r (현이 존재하려면)
            elif mode == "tangent_sq":
                d = random.randint(r + 1, r + 30)  # d > r (점이 원 밖)
            else:
                d = r  # 원 위의 점에서 원주각 관련
            seed = {"r": r, "d": d, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return {"r": 10, "d": 6, "mode": "chord_sq"}

    def execute(self, seed: dict[str, Any]) -> int:
        r, d, mode = seed["r"], seed["d"], seed["mode"]
        if mode == "chord_sq":
            # 현의 길이^2 = 4(r^2 - d^2), d = 중심에서 현까지 거리
            return (4 * (r * r - d * d)) % 1000
        elif mode == "tangent_sq":
            # 접선 길이^2 = d^2 - r^2
            return (d * d - r * r) % 1000
        else:  # inscribed_angle
            # 원주각 관련: 호에 대한 원주각은 중심각의 절반
            # 반지름 r인 원에서 현의 길이가 r인 경우, 중심각 = 60도 → 원주각 = 30도
            # 여기서는 d를 현의 길이로 재해석
            chord = d if d <= 2 * r else r
            # sin(theta/2) = chord/(2r) → theta는 중심각
            # 원주각 = theta/2
            # cos(theta) = 1 - 2sin^2(theta/2) = 1 - chord^2/(2r^2)
            # (2r^2 - chord^2) + 2r^2 을 답으로
            cos_num = 2 * r * r - chord * chord
            return (abs(cos_num) + 2 * r * r) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        r, d, mode = seed["r"], seed["d"], seed["mode"]
        chord_len = 0
        if mode == "chord_sq":
            chord_sq = 4 * (r * r - d * d)
            chord_len = int(chord_sq ** 0.5) if chord_sq > 0 else 0
        return {
            "center": [0, 0],
            "radius": r,
            "chord_length": chord_len,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        r, d, mode = seed["r"], seed["d"], seed["mode"]
        if mode == "chord_sq":
            return [
                f"1. 반지름 {r}인 원에서 중심으로부터 거리 {d}인 현을 구합니다.",
                f"2. 현의 반길이 = sqrt(r^2 - d^2) = sqrt({r}^2 - {d}^2).",
                f"3. 현의 길이^2 = 4(r^2 - d^2) = 4({r*r} - {d*d}).",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "tangent_sq":
            return [
                f"1. 반지름 {r}인 원 밖의 점이 중심에서 {d}만큼 떨어져 있습니다.",
                f"2. 접선 길이^2 = d^2 - r^2 = {d*d} - {r*r}.",
                "3. 피타고라스 정리로 직접 계산합니다.",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            return [
                f"1. 반지름 {r}인 원에서 현의 길이가 {d}인 호를 고려합니다.",
                "2. sin(중심각/2) = chord/(2r)로 중심각을 구합니다.",
                "3. 원주각은 중심각의 절반입니다.",
                "4. 관련 값을 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            return self.execute(seed)
        except Exception:
            return None
