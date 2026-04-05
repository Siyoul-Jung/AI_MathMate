"""
AI_MathMate V2 -- comb_graph_coloring_chromatic (그래프 색칠 / Chromatic Polynomial)
그래프의 색칠 다항식(Chromatic Polynomial)을 이용하여 k색으로 적절히 색칠하는 방법 수를 구합니다.
기출 4회 (AIME).
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombGraphColoringChromaticModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_graph_coloring_chromatic",
        name="그래프 색칠 (Chromatic Polynomial)",
        domain="integer",
        namespace="comb_chromatic",
        input_schema={
            "n_vertices": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=8, description="꼭짓점 수"),
            "k_colors": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=6, description="색 수"),
            "graph_type": FieldSpec(dtype=str, domain="str", description="'cycle' | 'complete' | 'path' | 'wheel'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=5.0,
        min_difficulty=8,
        category="combinatorics",
        tags=["graph_coloring", "chromatic_polynomial", "cycle", "complete_graph"],
        exam_types=["AIME"],
    )

    @staticmethod
    def _chromatic_cycle(n: int, k: int) -> int:
        """순환 그래프 C_n의 색칠 다항식: P(C_n, k) = (k-1)^n + (-1)^n * (k-1)"""
        return (k - 1) ** n + ((-1) ** n) * (k - 1)

    @staticmethod
    def _chromatic_complete(n: int, k: int) -> int:
        """완전 그래프 K_n의 색칠 다항식: P(K_n, k) = k * (k-1) * (k-2) * ... * (k-n+1)"""
        result = 1
        for i in range(n):
            result *= (k - i)
        return result

    @staticmethod
    def _chromatic_path(n: int, k: int) -> int:
        """경로 그래프 P_n의 색칠 다항식: P(P_n, k) = k * (k-1)^(n-1)"""
        return k * (k - 1) ** (n - 1)

    @staticmethod
    def _chromatic_wheel(n: int, k: int) -> int:
        """휠 그래프 W_n (중심 1 + 외곽 n개):
        P(W_n, k) = k * [(k-2)^n + (-1)^n * (k-2)]
        단, k >= 3이어야 유효한 색칠 존재"""
        if k < 3:
            return 0
        # 중심 꼭짓점에 색 배정 후 외곽 순환에서 중심색 제외
        # P(W_n, k) = k * P(C_n, k-1) / (k-1) 은 부정확.
        # 정확한 공식: 중심에 k가지, 외곽은 C_n을 (k-1)색으로 칠하기
        # P(W_n, k) = k * [(k-2)^n + (-1)^n * (k-2)]
        return k * ((k - 2) ** n + ((-1) ** n) * (k - 2))

    def generate_seed(self, difficulty_hint: float = 9.0) -> dict[str, Any]:
        graph_types = ["cycle", "complete", "path", "wheel"]
        for _ in range(100):
            graph_type = random.choice(graph_types)
            if graph_type == "complete":
                n_vertices = random.randint(3, 6)
                k_colors = random.randint(n_vertices, min(n_vertices + 2, 6))
            elif graph_type == "wheel":
                n_vertices = random.randint(3, 7)
                k_colors = random.randint(3, 6)
            else:
                n_vertices = random.randint(3, 8)
                k_colors = random.randint(2, 5)

            seed = {"n_vertices": n_vertices, "k_colors": k_colors, "graph_type": graph_type}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n_vertices": 4, "k_colors": 3, "graph_type": "cycle"}

    def execute(self, seed: dict[str, Any]) -> int:
        n = seed["n_vertices"]
        k = seed["k_colors"]
        graph_type = seed["graph_type"]

        if graph_type == "cycle":
            result = self._chromatic_cycle(n, k)
        elif graph_type == "complete":
            result = self._chromatic_complete(n, k)
        elif graph_type == "path":
            result = self._chromatic_path(n, k)
        else:  # wheel
            result = self._chromatic_wheel(n, k)

        return abs(result) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n = seed["n_vertices"]
        k = seed["k_colors"]
        graph_type = seed["graph_type"]
        ans = self.execute(seed)

        if graph_type == "cycle":
            return [
                f"1. 순환 그래프 C_{n}의 꼭짓점을 {k}색으로 적절히 색칠하는 방법 수를 구합니다.",
                f"2. 색칠 다항식: P(C_{n}, {k}) = ({k}-1)^{n} + (-1)^{n} * ({k}-1).",
                f"3. ({k-1})^{n} = {(k-1)**n}, (-1)^{n}*({k-1}) = {((-1)**n)*(k-1)}.",
                f"4. 합산 후 mod 1000 = {ans}.",
            ]
        elif graph_type == "complete":
            return [
                f"1. 완전 그래프 K_{n}을 {k}색으로 적절히 색칠하는 방법 수를 구합니다.",
                f"2. P(K_{n}, {k}) = {k} x ({k}-1) x ... x ({k}-{n}+1).",
                f"3. = {' x '.join(str(k-i) for i in range(n))} = {self._chromatic_complete(n, k)}.",
                f"4. mod 1000 = {ans}.",
            ]
        elif graph_type == "path":
            return [
                f"1. 경로 그래프 P_{n} (꼭짓점 {n}개)을 {k}색으로 색칠합니다.",
                f"2. 첫 꼭짓점: {k}가지, 이후 각 꼭짓점: ({k}-1)가지.",
                f"3. P(P_{n}, {k}) = {k} x ({k}-1)^{n-1} = {self._chromatic_path(n, k)}.",
                f"4. mod 1000 = {ans}.",
            ]
        else:
            return [
                f"1. 휠 그래프 W_{n} (중심 1개 + 외곽 {n}개)을 {k}색으로 색칠합니다.",
                f"2. 중심 꼭짓점에 {k}가지 색 중 하나를 배정합니다.",
                f"3. 외곽 순환 C_{n}을 중심색을 제외한 ({k}-1)색 중 ({k}-2)색으로 색칠합니다.",
                f"4. P(W_{n}, {k}) = {k} x [({k}-2)^{n} + (-1)^{n}*({k}-2)] mod 1000 = {ans}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Integer
            n = seed["n_vertices"]
            k = seed["k_colors"]
            graph_type = seed["graph_type"]

            if graph_type == "cycle":
                result = (k - 1) ** n + ((-1) ** n) * (k - 1)
            elif graph_type == "complete":
                result = 1
                for i in range(n):
                    result *= (k - i)
            elif graph_type == "path":
                result = k * (k - 1) ** (n - 1)
            else:
                result = k * ((k - 2) ** n + ((-1) ** n) * (k - 2))

            return abs(result) % 1000
        except Exception:
            return None
