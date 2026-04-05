"""
AI_MathMate V2 -- comb_catalan (카탈란 수)
C(n) = C(2n, n) / (n+1) 카탈란 수의 다양한 해석을 활용합니다.
- 올바른 괄호 배열 수
- 대각선을 넘지 않는 격자 경로 수
- 이진 트리의 구조 수
기출 2회 (AIME).
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombCatalanModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_catalan",
        name="카탈란 수 (Catalan Numbers)",
        domain="integer",
        namespace="comb_catalan",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=12, description="카탈란 수의 인덱스"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'catalan' | 'ballot' | 'triangulation'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=7,
        category="combinatorics",
        tags=["catalan", "parenthesization", "binary_tree", "triangulation", "ballot"],
        exam_types=["AIME"],
        bridge_output_keys=["catalan_value", "n"],
    )

    def _catalan(self, n: int) -> int:
        """n번째 카탈란 수 C(n) = C(2n,n)/(n+1)"""
        return math.comb(2 * n, n) // (n + 1)

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["catalan", "ballot", "triangulation"]
        for _ in range(100):
            mode = random.choice(modes)
            if difficulty_hint < 9:
                n = random.randint(2, 8)
            else:
                n = random.randint(5, 12)
            seed = {"n": n, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n": 5, "mode": "catalan"}

    def execute(self, seed: dict[str, Any]) -> int:
        n = seed["n"]
        mode = seed["mode"]

        if mode == "catalan":
            # 직접 카탈란 수 mod 1000
            return self._catalan(n) % 1000

        elif mode == "ballot":
            # 투표 문제: 후보 A가 n표, 후보 B가 n표일 때
            # A가 항상 앞서거나 같은 경우의 수 = C(n)
            # 답: C(n) mod 1000
            return self._catalan(n) % 1000

        else:  # triangulation
            # 볼록 (n+2)-각형을 삼각형으로 분할하는 방법 수 = C(n)
            return self._catalan(n) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        n = seed["n"]
        return {
            "catalan_value": self._catalan(n),
            "n": n,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n = seed["n"]
        mode = seed["mode"]
        c_val = self._catalan(n)

        if mode == "catalan":
            return [
                f"1. n={n}번째 카탈란 수 C({n}) = C(2*{n}, {n}) / ({n}+1)을 구합니다.",
                f"2. C({2*n}, {n}) = {math.comb(2*n, n)}을 계산합니다.",
                f"3. {math.comb(2*n, n)} / {n+1} = {c_val}을 구합니다.",
                f"4. {c_val} mod 1000 = {c_val % 1000}이 최종 답입니다.",
            ]
        elif mode == "ballot":
            return [
                f"1. A와 B가 각각 {n}표씩 받은 투표에서, 개표 과정 중 A가 항상 앞서거나 같은 순서의 수를 구합니다.",
                f"2. 이것은 n={n}번째 카탈란 수 C({n})와 같습니다.",
                f"3. C({n}) = C({2*n},{n})/({n}+1) = {c_val}을 계산합니다.",
                f"4. {c_val} mod 1000 = {c_val % 1000}이 최종 답입니다.",
            ]
        else:
            return [
                f"1. 볼록 {n+2}각형을 대각선으로 삼각형 분할하는 방법 수를 구합니다.",
                f"2. 이것은 n={n}번째 카탈란 수 C({n})와 같습니다.",
                f"3. C({n}) = C({2*n},{n})/({n}+1) = {c_val}을 계산합니다.",
                f"4. {c_val} mod 1000 = {c_val % 1000}이 최종 답입니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import catalan, Integer
            n = seed["n"]
            sympy_val = int(catalan(Integer(n)))
            return sympy_val % 1000
        except Exception:
            return None
