"""
AI_MathMate V2 — 중국인 나머지 정리 (nt_chinese_remainder_theorem)
서로소인 모듈러 연립합동식의 최소 양수 해를 구합니다. AIME 기출 12회.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class NtChineseRemainderTheoremModule(AtomicModule):
    META = ModuleMeta(
        module_id="nt_chinese_remainder_theorem",
        name="중국인 나머지 정리",
        domain="integer",
        namespace="nt_crt",
        input_schema={
            "remainders": FieldSpec(dtype=list, domain="Z+", description="나머지 리스트 [a1, a2, ...]"),
            "moduli": FieldSpec(dtype=list, domain="Z+", min_val=2, max_val=100, description="서로소인 법 리스트 [m1, m2, ...]"),
            "mode": FieldSpec(dtype=str, domain="str", description="'min_solution' | 'kth_solution' | 'count_range'"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=10, description="k번째 해 (kth_solution 모드)"),
            "upper": FieldSpec(dtype=int, domain="Z+", min_val=100, max_val=10000, description="범위 상한 (count_range 모드)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=5,
        category="number_theory",
        tags=["CRT", "congruence", "modular_system", "coprime"],
        exam_types=["AIME"],
    )

    @staticmethod
    def _ext_gcd(a: int, b: int) -> tuple[int, int, int]:
        """확장 유클리드: ax + by = gcd(a,b) → (g, x, y)"""
        if b == 0:
            return a, 1, 0
        g, x1, y1 = NtChineseRemainderTheoremModule._ext_gcd(b, a % b)
        return g, y1, x1 - (a // b) * y1

    @staticmethod
    def _crt_two(a1: int, m1: int, a2: int, m2: int) -> tuple[int, int]:
        """두 합동식 x ≡ a1 (mod m1), x ≡ a2 (mod m2) 의 해를 (solution, lcm) 으로 반환."""
        g, p, _ = NtChineseRemainderTheoremModule._ext_gcd(m1, m2)
        if (a2 - a1) % g != 0:
            raise ValueError("해가 존재하지 않음")
        lcm = m1 // g * m2
        sol = (a1 + m1 * ((a2 - a1) // g * p % (m2 // g))) % lcm
        return sol, lcm

    @classmethod
    def _crt(cls, remainders: list[int], moduli: list[int]) -> tuple[int, int]:
        """연립합동식의 최소 비음수 해와 주기를 반환."""
        cur_a, cur_m = remainders[0] % moduli[0], moduli[0]
        for i in range(1, len(remainders)):
            cur_a, cur_m = cls._crt_two(cur_a, cur_m, remainders[i] % moduli[i], moduli[i])
        return cur_a, cur_m

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["min_solution", "kth_solution", "count_range"]
        # 서로소인 모듈러 후보
        coprime_sets = [
            [3, 5, 7], [3, 7, 11], [4, 9, 11], [5, 7, 9],
            [3, 5, 11], [7, 11, 13], [4, 7, 9], [5, 9, 13],
            [3, 11, 13], [5, 7, 11], [8, 9, 11], [7, 9, 11],
        ]

        for _ in range(100):
            mode = random.choice(modes)
            moduli = list(random.choice(coprime_sets))
            # 모든 쌍이 서로소인지 확인
            ok = all(math.gcd(moduli[i], moduli[j]) == 1
                     for i in range(len(moduli)) for j in range(i + 1, len(moduli)))
            if not ok:
                continue

            remainders = [random.randint(0, m - 1) for m in moduli]
            k = random.randint(1, 5)
            prod = 1
            for m in moduli:
                prod *= m
            upper = random.randint(prod * 2, prod * 10)

            seed = {
                "remainders": remainders, "moduli": moduli,
                "mode": mode, "k": k, "upper": upper,
            }
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"remainders": [2, 3, 2], "moduli": [3, 5, 7], "mode": "min_solution", "k": 1, "upper": 1000}

    def execute(self, seed: dict[str, Any]) -> int:
        remainders = seed["remainders"]
        moduli = seed["moduli"]
        mode = seed["mode"]

        sol, period = self._crt(remainders, moduli)
        if sol == 0:
            sol = period  # 최소 양수 해

        if mode == "min_solution":
            return sol % 1000

        elif mode == "kth_solution":
            k = seed["k"]
            kth = sol + (k - 1) * period
            return kth % 1000

        else:  # count_range
            upper = seed["upper"]
            if sol > upper:
                return 0
            count = (upper - sol) // period + 1
            return count % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        remainders = seed["remainders"]
        moduli = seed["moduli"]
        mode = seed["mode"]
        congs = [f"x ≡ {r} (mod {m})" for r, m in zip(remainders, moduli)]
        sol, period = self._crt(remainders, moduli)
        if sol == 0:
            sol = period

        steps = [
            f"1. 연립합동식을 세웁니다: {', '.join(congs)}.",
            f"2. 모듈러 {moduli}가 쌍별 서로소임을 확인합니다 (CRT 적용 가능).",
            f"3. 확장 유클리드 알고리즘으로 단계적으로 합쳐서 최소 양수 해 x = {sol}, 주기 = {period}를 구합니다.",
        ]
        if mode == "kth_solution":
            k = seed["k"]
            steps.append(f"4. {k}번째 해: {sol} + {k - 1} × {period} = {sol + (k - 1) * period}, mod 1000을 취합니다.")
        elif mode == "count_range":
            upper = seed["upper"]
            steps.append(f"4. 1~{upper} 범위에서 해의 개수를 셉니다: ⌊({upper} - {sol}) / {period}⌋ + 1.")
        else:
            steps.append(f"4. 최소 양수 해 {sol}을 1000으로 나눈 나머지를 구합니다.")
        return steps

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy.ntheory.modular import crt
            remainders = seed["remainders"]
            moduli = seed["moduli"]
            mode = seed["mode"]

            result = crt(moduli, remainders)
            if result is None:
                return None
            sol, period = result
            sol = int(sol)
            period = int(period)
            if sol == 0:
                sol = period

            if mode == "min_solution":
                return sol % 1000
            elif mode == "kth_solution":
                k = seed["k"]
                return (sol + (k - 1) * period) % 1000
            else:
                upper = seed["upper"]
                if sol > upper:
                    return 0
                count = (upper - sol) // period + 1
                return count % 1000
        except Exception:
            return None
