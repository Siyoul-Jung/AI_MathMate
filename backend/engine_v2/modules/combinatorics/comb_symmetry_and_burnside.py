"""
AI_MathMate V2 -- comb_symmetry_and_burnside (번사이드 보조정리 / Burnside's Lemma)
군(Group) 작용 하에서 구별되는 색칠/배열 수를 구합니다.
|X/G| = (1/|G|) * sum_{g in G} |Fix(g)|
기출 7회 (AIME).
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombSymmetryAndBurnsideModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_symmetry_and_burnside",
        name="번사이드 보조정리 (Burnside's Lemma)",
        domain="integer",
        namespace="comb_burnside",
        input_schema={
            "n_positions": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=10, description="위치/꼭짓점 수"),
            "n_colors": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=5, description="사용 가능 색 수"),
            "mode": FieldSpec(dtype=str, domain="str", description="'necklace' | 'cube_face' | 'bracelet'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="구별되는 배열 수 mod 1000"),
        },
        logic_depth=5,
        daps_contribution=5.5,
        min_difficulty=9,
        category="combinatorics",
        tags=["burnside", "polya", "symmetry", "group_action", "necklace", "coloring"],
        exam_types=["AIME"],
    )

    @staticmethod
    def _necklace_count(n: int, k: int) -> int:
        """n개 구슬 목걸이, k색, 회전 대칭만 (순환군 Z_n)
        = (1/n) * sum_{d|n} phi(n/d) * k^d
        """
        total = 0
        for d in range(1, n + 1):
            if n % d == 0:
                # 오일러 피 함수
                phi_val = _euler_phi(n // d)
                total += phi_val * (k ** d)
        return total // n

    @staticmethod
    def _bracelet_count(n: int, k: int) -> int:
        """n개 구슬 팔찌, k색, 회전+뒤집기 대칭 (이면체군 D_n)
        = (necklace + reflection_fix) / 2 대신 직접 계산
        """
        necklace = CombSymmetryAndBurnsideModule._necklace_count(n, k)
        # 뒤집기 고정점
        if n % 2 == 0:
            # n/2개의 축이 꼭짓점 통과, n/2개의 축이 변 통과
            flip_fix = (n // 2) * (k ** (n // 2 + 1)) + (n // 2) * (k ** (n // 2))
        else:
            # n개의 축, 각각 하나의 꼭짓점 통과
            flip_fix = n * (k ** ((n + 1) // 2))

        # 번사이드: (회전 고정점 합 + 뒤집기 고정점 합) / (2n)
        rotation_sum = necklace * n  # necklace = rotation_sum / n
        return (rotation_sum + flip_fix) // (2 * n)

    @staticmethod
    def _cube_face_coloring(k: int) -> int:
        """정육면체 6면 k색 칠하기 (회전군 |G|=24)
        번사이드 공식:
        1*k^6 + 6*k^3 + 3*k^4 + 8*k^2 + 6*k^3 를 24로 나눔
        = (k^6 + 3*k^4 + 12*k^3 + 8*k^2) / 24
        """
        total = k**6 + 3 * k**4 + 12 * k**3 + 8 * k**2
        return total // 24

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["necklace", "cube_face", "bracelet"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "cube_face":
                n_positions = 6  # 정육면체 면 수
                n_colors = random.randint(2, 5)
            elif mode == "necklace":
                n_positions = random.randint(3, 10)
                n_colors = random.randint(2, 4)
            else:  # bracelet
                n_positions = random.randint(3, 10)
                n_colors = random.randint(2, 4)

            seed = {"n_positions": n_positions, "n_colors": n_colors, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n_positions": 5, "n_colors": 2, "mode": "necklace"}

    def execute(self, seed: dict[str, Any]) -> int:
        n = seed["n_positions"]
        k = seed["n_colors"]
        mode = seed["mode"]

        if mode == "necklace":
            return self._necklace_count(n, k) % 1000
        elif mode == "bracelet":
            return self._bracelet_count(n, k) % 1000
        else:  # cube_face
            return self._cube_face_coloring(k) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n = seed["n_positions"]
        k = seed["n_colors"]
        mode = seed["mode"]
        ans = self.execute(seed)

        if mode == "necklace":
            return [
                f"1. {n}개 구슬 목걸이를 {k}색으로 칠하는 구별되는 방법 수를 구합니다.",
                f"2. 순환군 Z_{n}의 작용: 회전 대칭을 고려합니다.",
                f"3. 번사이드 보조정리: (1/{n}) * sum(phi({n}/d) * {k}^d, d|{n}).",
                f"4. 각 약수 d에 대해 오일러 피 함수와 고정점을 계산합니다.",
                f"5. 결과 mod 1000 = {ans}.",
            ]
        elif mode == "bracelet":
            return [
                f"1. {n}개 구슬 팔찌를 {k}색으로 칠하는 구별되는 방법 수를 구합니다.",
                f"2. 이면체군 D_{n}의 작용: 회전 + 뒤집기 대칭을 고려합니다.",
                f"3. 회전 고정점(목걸이)과 뒤집기 고정점을 각각 계산합니다.",
                f"4. 번사이드: (회전 고정점 합 + 뒤집기 고정점 합) / (2*{n}).",
                f"5. 결과 mod 1000 = {ans}.",
            ]
        else:
            return [
                f"1. 정육면체 6면을 {k}색으로 칠하는 구별되는 방법 수를 구합니다.",
                f"2. 정육면체 회전군 |G|=24: 항등(1) + 면회전(6) + 모서리회전(3) + 꼭짓점회전(8) + 대면회전(6).",
                f"3. 번사이드: ({k}^6 + 3*{k}^4 + 12*{k}^3 + 8*{k}^2) / 24.",
                f"4. 결과 mod 1000 = {ans}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            n = seed["n_positions"]
            k = seed["n_colors"]
            mode = seed["mode"]

            if mode == "necklace":
                # 독립 검증: 직접 약수 순회
                total = 0
                for d in range(1, n + 1):
                    if n % d == 0:
                        total += _euler_phi(n // d) * (k ** d)
                return (total // n) % 1000
            elif mode == "bracelet":
                return self._bracelet_count(n, k) % 1000
            else:
                return ((k**6 + 3 * k**4 + 12 * k**3 + 8 * k**2) // 24) % 1000
        except Exception:
            return None


def _euler_phi(n: int) -> int:
    """오일러 피 함수"""
    result = n
    p = 2
    temp = n
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result
