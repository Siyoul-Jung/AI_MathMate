"""
AI_MathMate V2 -- comb_path_counting (격자 경로 세기 / Lattice Path Counting)
(0,0)에서 (m,n)까지 오른쪽/위쪽으로만 이동하는 격자 경로 수.
장애물 또는 대각선 제약이 있는 변형 포함.
기출 20회 (AIME).
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombPathCountingModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_path_counting",
        name="격자 경로 세기 (Lattice Path Counting)",
        domain="integer",
        namespace="comb_path",
        input_schema={
            "m": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=15, description="격자 가로 크기"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=15, description="격자 세로 크기"),
            "mode": FieldSpec(dtype=str, domain="str", description="'basic' | 'reflect' | 'obstacle'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=5,
        category="combinatorics",
        tags=["lattice_path", "binomial", "reflection_principle", "catalan"],
        exam_types=["AIME"],
        bridge_output_keys=["path_count", "grid_size"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["basic", "reflect", "obstacle"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "basic":
                m = random.randint(2, 15)
                n = random.randint(2, 15)
            elif mode == "reflect":
                # 반사 원리: m == n일 때 대각선 아래 경로 (카탈란 수)
                val = random.randint(2, 12)
                m, n = val, val
            else:  # obstacle
                m = random.randint(3, 10)
                n = random.randint(3, 10)

            seed = {"m": m, "n": n, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"m": 4, "n": 4, "mode": "basic"}

    def execute(self, seed: dict[str, Any]) -> int:
        m, n, mode = seed["m"], seed["n"], seed["mode"]

        if mode == "basic":
            # C(m+n, m) 격자 경로 수
            return math.comb(m + n, m) % 1000

        elif mode == "reflect":
            # 대각선 y=x를 넘지 않는 경로 수 (반사 원리)
            # = C(2n, n) - C(2n, n+1) = C(2n, n) / (n+1) = 카탈란 수 C_n
            catalan = math.comb(2 * n, n) // (n + 1)
            return catalan % 1000

        else:  # obstacle
            # 중간 점 (m//2, n//2)을 통과할 수 없는 경로 수
            # 전체 - 장애물 통과 경로
            mid_r, mid_c = m // 2, n // 2
            total = math.comb(m + n, m)
            # 장애물 통과: (0,0)->(mid_r,mid_c) * (mid_r,mid_c)->(m,n)
            through = math.comb(mid_r + mid_c, mid_r) * math.comb((m - mid_r) + (n - mid_c), m - mid_r)
            result = total - through
            return abs(result) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        m, n = seed["m"], seed["n"]
        return {
            "path_count": math.comb(m + n, m),
            "grid_size": m + n,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        m, n, mode = seed["m"], seed["n"], seed["mode"]

        if mode == "basic":
            return [
                f"1. (0,0)에서 ({m},{n})까지 오른쪽/위쪽 이동만 허용하는 격자 경로 수를 구합니다.",
                f"2. 총 이동 횟수 = {m}+{n} = {m+n}, 그 중 오른쪽 {m}번.",
                f"3. C({m+n}, {m}) = {math.comb(m+n, m)}을 계산합니다.",
                f"4. mod 1000 = {math.comb(m+n, m) % 1000}.",
            ]
        elif mode == "reflect":
            catalan = math.comb(2 * n, n) // (n + 1)
            return [
                f"1. (0,0)에서 ({n},{n})까지 대각선 y=x를 넘지 않는 경로 수를 구합니다.",
                f"2. 반사 원리(Reflection Principle)를 적용합니다.",
                f"3. C({2*n},{n}) - C({2*n},{n+1}) = C({2*n},{n})/({n}+1) = {catalan} (카탈란 수).",
                f"4. mod 1000 = {catalan % 1000}.",
            ]
        else:
            mid_r, mid_c = m // 2, n // 2
            total = math.comb(m + n, m)
            through = math.comb(mid_r + mid_c, mid_r) * math.comb((m - mid_r) + (n - mid_c), m - mid_r)
            return [
                f"1. (0,0)에서 ({m},{n})까지의 경로 중 ({mid_r},{mid_c})를 통과하지 않는 수를 구합니다.",
                f"2. 전체 경로 수 = C({m+n},{m}) = {total}.",
                f"3. 장애물 통과 경로 = C({mid_r+mid_c},{mid_r}) x C({(m-mid_r)+(n-mid_c)},{m-mid_r}) = {through}.",
                f"4. 답 = {total} - {through} = {total - through}, mod 1000 = {abs(total - through) % 1000}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import binomial, Integer
            m, n, mode = seed["m"], seed["n"], seed["mode"]
            if mode == "basic":
                return int(binomial(Integer(m + n), Integer(m))) % 1000
            elif mode == "reflect":
                cat = int(binomial(2 * n, n)) // (n + 1)
                return cat % 1000
            else:
                mid_r, mid_c = m // 2, n // 2
                total = int(binomial(m + n, m))
                through = int(binomial(mid_r + mid_c, mid_r)) * int(binomial((m - mid_r) + (n - mid_c), m - mid_r))
                return abs(total - through) % 1000
        except Exception:
            return None
