"""
AI_MathMate V2 -- comb_count_double (이중 세기 / Double Counting)
같은 집합을 두 가지 방법으로 세어 항등식을 유도합니다.
기출 118회 (AIME). Bridge 소스 모듈.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombCountDoubleModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_count_double",
        name="이중 세기 (Double Counting)",
        domain="integer",
        namespace="comb_dblcount",
        input_schema={
            "n": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=15, description="집합 크기"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=8, description="부분집합 크기"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'handshake' | 'committee' | 'grid'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=5,
        category="combinatorics",
        tags=["double_counting", "bijection", "handshake_lemma", "committee"],
        exam_types=["AIME"],
        bridge_output_keys=["total_count", "favorable_count", "n_elements"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["handshake", "committee", "grid"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "handshake":
                n = random.randint(4, 15)
                k = random.randint(2, min(n - 1, 6))
            elif mode == "committee":
                n = random.randint(5, 12)
                k = random.randint(2, min(n - 1, 5))
            else:  # grid
                n = random.randint(3, 10)
                k = random.randint(2, min(n, 5))
            seed = {"n": n, "k": k, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n": 6, "k": 3, "mode": "handshake"}

    def execute(self, seed: dict[str, Any]) -> int:
        n, k, mode = seed["n"], seed["k"], seed["mode"]

        if mode == "handshake":
            # n명이 각각 정확히 k명과 악수할 때, 총 악수 횟수
            # 이중 세기: sum(degree) = 2 * |edges|
            # 가능 조건: n*k가 짝수
            # 총 악수 횟수 = n*k // 2
            total = (n * k) // 2
            return total % 1000

        elif mode == "committee":
            # n명에서 k명 위원회를 뽑고 그중 의장 1명을 선출하는 방법 수
            # 방법 1: C(n,k) * k (위원회 뽑고 의장 선출)
            # 방법 2: n * C(n-1,k-1) (의장 먼저 뽑고 나머지 위원 선출)
            # 둘 다 같은 값 = n * C(n-1, k-1)
            result = n * math.comb(n - 1, k - 1)
            return result % 1000

        else:  # grid
            # n x k 격자에서 직사각형 개수
            # 이중 세기: 수평선 2개 * 수직선 2개 = C(n+1,2) * C(k+1,2)
            result = math.comb(n + 1, 2) * math.comb(k + 1, 2)
            return result % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        n, k, mode = seed["n"], seed["k"], seed["mode"]
        ans = self.execute(seed)

        if mode == "committee":
            total = math.comb(n, k) * k
            favorable = n * math.comb(n - 1, k - 1)
        elif mode == "handshake":
            total = n * k
            favorable = (n * k) // 2
        else:
            total = math.comb(n + 1, 2) * math.comb(k + 1, 2)
            favorable = total

        return {
            "total_count": total,
            "favorable_count": favorable,
            "n_elements": n,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n, k, mode = seed["n"], seed["k"], seed["mode"]

        if mode == "handshake":
            return [
                f"1. {n}명이 각각 정확히 {k}명과 악수하는 상황을 설정합니다.",
                f"2. 방법 1: 각 사람 관점에서 악수 횟수 합산 = {n} x {k} = {n*k}.",
                f"3. 방법 2: 각 악수는 두 사람이 관여하므로 2회 중복 카운트됩니다.",
                f"4. 이중 세기: 총 악수 횟수 = {n*k} / 2 = {(n*k)//2}, mod 1000 적용.",
            ]
        elif mode == "committee":
            return [
                f"1. {n}명에서 {k}명 위원회를 뽑고 의장 1명을 선출합니다.",
                f"2. 방법 1: C({n},{k}) x {k} = 위원회 뽑고 의장 선출.",
                f"3. 방법 2: 의장 먼저 선출({n}가지) x 나머지 위원 C({n-1},{k-1}).",
                f"4. 이중 세기로 두 방법이 같음을 확인하고 {n} x C({n-1},{k-1}) mod 1000을 계산합니다.",
            ]
        else:
            return [
                f"1. {n} x {k} 격자에서 직사각형 개수를 구합니다.",
                f"2. 수평선 {n+1}개 중 2개 선택: C({n+1},2) = {math.comb(n+1,2)}.",
                f"3. 수직선 {k+1}개 중 2개 선택: C({k+1},2) = {math.comb(k+1,2)}.",
                f"4. 총 직사각형 수 = {math.comb(n+1,2)} x {math.comb(k+1,2)} mod 1000.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import binomial, Integer
            n, k, mode = seed["n"], seed["k"], seed["mode"]
            if mode == "handshake":
                return int((n * k) // 2) % 1000
            elif mode == "committee":
                return int(n * binomial(Integer(n - 1), Integer(k - 1))) % 1000
            else:
                return int(binomial(Integer(n + 1), 2) * binomial(Integer(k + 1), 2)) % 1000
        except Exception:
            return None
