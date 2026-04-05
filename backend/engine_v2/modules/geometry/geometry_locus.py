"""
AI_MathMate V2 — 궤적 (geometry_locus)
두 고정점에 대한 맨해튼 거리 합/차 조건을 만족하는 격자점 개수를 구합니다.
타원/쌍곡선의 정수 좌표 궤적 문제입니다.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryLocusModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_locus",
        name="궤적 (맨해튼 거리)",
        domain="integer",
        namespace="geom_locus",
        input_schema={
            "fx1": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="초점 F1 x좌표"),
            "fy1": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="초점 F1 y좌표"),
            "fx2": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="초점 F2 x좌표"),
            "fy2": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="초점 F2 y좌표"),
            "S": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=60, description="맨해튼 거리 합 상수"),
            "mode": FieldSpec(dtype=str, domain="str", description="'sum' (타원형) | 'diff' (쌍곡선형)"),
            "bound": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=50, description="탐색 범위"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="조건 만족 격자점 개수 mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=7,
        category="geometry",
        tags=["locus", "ellipse", "hyperbola", "lattice_points", "manhattan_distance"],
        exam_types=["AIME"],
        bridge_output_keys=["lattice_count", "sum_constant"],
    )

    def generate_seed(self, difficulty_hint: float = 9.0) -> dict[str, Any]:
        modes = ["sum", "diff"]
        for _ in range(100):
            mode = random.choice(modes)
            fx1 = random.randint(-5, 5)
            fy1 = random.randint(-5, 5)
            fx2 = random.randint(-5, 5)
            fy2 = random.randint(-5, 5)

            # 초점이 같으면 스킵
            if fx1 == fx2 and fy1 == fy2:
                continue

            foci_dist = abs(fx1 - fx2) + abs(fy1 - fy2)

            if mode == "sum":
                # S > 초점 간 맨해튼 거리 (삼각부등식)
                S = random.randint(foci_dist + 1, foci_dist + random.randint(4, 20))
            else:
                # 차이 모드: 0 < S < 초점 간 거리
                if foci_dist <= 1:
                    continue
                S = random.randint(1, foci_dist - 1)

            bound = max(20, S + max(abs(fx1), abs(fy1), abs(fx2), abs(fy2)) + 5)
            if bound > 50:
                bound = 50

            seed = {
                "fx1": fx1, "fy1": fy1, "fx2": fx2, "fy2": fy2,
                "S": S, "mode": mode, "bound": bound,
            }
            ans = self.execute(seed)
            if 0 <= ans <= 999 and ans > 0:
                return seed

        return {"fx1": 0, "fy1": 0, "fx2": 3, "fy2": 0, "S": 8, "mode": "sum", "bound": 20}

    def execute(self, seed: dict[str, Any]) -> int:
        fx1, fy1 = seed["fx1"], seed["fy1"]
        fx2, fy2 = seed["fx2"], seed["fy2"]
        S = seed["S"]
        mode = seed["mode"]
        bound = seed["bound"]

        count = 0
        for x in range(-bound, bound + 1):
            for y in range(-bound, bound + 1):
                d1 = abs(x - fx1) + abs(y - fy1)
                d2 = abs(x - fx2) + abs(y - fy2)
                if mode == "sum":
                    if d1 + d2 == S:
                        count += 1
                else:  # diff
                    if abs(d1 - d2) == S:
                        count += 1

        return count % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        count = self.execute(seed)
        return {
            "lattice_count": count,
            "sum_constant": seed["S"],
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        fx1, fy1 = seed["fx1"], seed["fy1"]
        fx2, fy2 = seed["fx2"], seed["fy2"]
        S = seed["S"]
        mode = seed["mode"]
        bound = seed["bound"]
        ans = self.execute(seed)

        if mode == "sum":
            cond_str = f"d(P, F1) + d(P, F2) = {S}"
            shape = "타원형"
        else:
            cond_str = f"|d(P, F1) - d(P, F2)| = {S}"
            shape = "쌍곡선형"

        return [
            f"1. 두 초점 F1=({fx1},{fy1}), F2=({fx2},{fy2})를 설정합니다.",
            f"2. 맨해튼 거리 조건 {cond_str}을 만족하는 정수 격자점을 찾습니다 ({shape} 궤적).",
            f"3. 탐색 범위 [-{bound}, {bound}]에서 모든 정수 좌표 (x, y)를 검사합니다.",
            f"4. 조건을 만족하는 격자점의 개수 {ans}를 구하고 1000으로 나눈 나머지를 취합니다.",
        ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            # 브루트포스 독립 재계산
            fx1, fy1 = seed["fx1"], seed["fy1"]
            fx2, fy2 = seed["fx2"], seed["fy2"]
            S = seed["S"]
            mode = seed["mode"]
            bound = seed["bound"]

            count = 0
            for x in range(-bound, bound + 1):
                for y in range(-bound, bound + 1):
                    d1 = abs(x - fx1) + abs(y - fy1)
                    d2 = abs(x - fx2) + abs(y - fy2)
                    if mode == "sum":
                        if d1 + d2 == S:
                            count += 1
                    else:
                        if abs(d1 - d2) == S:
                            count += 1
            return count % 1000
        except Exception:
            return None
