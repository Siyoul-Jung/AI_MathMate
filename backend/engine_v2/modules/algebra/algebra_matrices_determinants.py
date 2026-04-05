"""
AI_MathMate V2 — 행렬/행렬식 (algebra_matrices_determinants)
2x2, 3x3 정수 행렬의 행렬식, 역행렬 원소, 행렬 거듭제곱의 원소를 다룹니다.
기출 빈도: 7회
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraMatricesDeterminantsModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_matrices_determinants",
        name="행렬/행렬식",
        domain="integer",
        namespace="alg_matrix",
        input_schema={
            "matrix": FieldSpec(dtype=list, domain="Z", description="2x2 또는 3x3 정수 행렬 (row-major)"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'det2' | 'det3' | 'inv_element'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="행렬식 또는 역행렬 원소 합 (mod 1000)"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=5,
        category="algebra",
        tags=["matrix", "determinant", "inverse_matrix", "linear_algebra"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["determinant"],
    )

    # ── 내부 유틸 ──

    @staticmethod
    def _det2(m: list[list[int]]) -> int:
        """2x2 행렬식"""
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    @staticmethod
    def _det3(m: list[list[int]]) -> int:
        """3x3 행렬식 (사루스 전개)"""
        a = m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
        b = m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
        c = m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
        return a - b + c

    @staticmethod
    def _adjugate2(m: list[list[int]]) -> list[list[int]]:
        """2x2 수반행렬 (adjugate)"""
        return [[m[1][1], -m[0][1]], [-m[1][0], m[0][0]]]

    @staticmethod
    def _cofactor3(m: list[list[int]]) -> list[list[int]]:
        """3x3 여인수 행렬"""
        cof = [[0, 0, 0] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                # 소행렬
                minor = []
                for r in range(3):
                    if r == i:
                        continue
                    row = []
                    for c_idx in range(3):
                        if c_idx == j:
                            continue
                        row.append(m[r][c_idx])
                    minor.append(row)
                sign = (-1) ** (i + j)
                cof[i][j] = sign * (minor[0][0] * minor[1][1] - minor[0][1] * minor[1][0])
        return cof

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["det2", "det3", "inv_element"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "det2":
                m = [[random.randint(-15, 15) for _ in range(2)] for _ in range(2)]
                seed = {"matrix": m, "mode": mode}

            elif mode == "det3":
                m = [[random.randint(-9, 9) for _ in range(3)] for _ in range(3)]
                seed = {"matrix": m, "mode": mode}

            else:  # inv_element
                # 2x2 역행렬의 원소 절대값 합 → det != 0 필요
                m = [[random.randint(-12, 12) for _ in range(2)] for _ in range(2)]
                det_val = self._det2(m)
                if det_val == 0:
                    continue
                seed = {"matrix": m, "mode": mode}

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"matrix": [[3, 1], [2, 4]], "mode": "det2"}

    def execute(self, seed: dict[str, Any]) -> int:
        m = seed["matrix"]
        mode = seed["mode"]

        if mode == "det2":
            return abs(self._det2(m)) % 1000

        elif mode == "det3":
            return abs(self._det3(m)) % 1000

        else:  # inv_element
            # det*inverse = adjugate → 역행렬 분자(수반행렬) 원소 절대값 합 + |det|
            det_val = self._det2(m)
            if det_val == 0:
                return 0
            adj = self._adjugate2(m)
            elem_sum = sum(abs(adj[i][j]) for i in range(2) for j in range(2))
            return (elem_sum + abs(det_val)) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        m = seed["matrix"]
        mode = seed["mode"]
        if mode == "det3":
            return {"determinant": self._det3(m)}
        else:
            return {"determinant": self._det2(m)}

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        m = seed["matrix"]
        mode = seed["mode"]

        if mode == "det2":
            return [
                f"1. 2x2 행렬 [[{m[0][0]}, {m[0][1]}], [{m[1][0]}, {m[1][1]}]]의 행렬식을 구합니다.",
                f"2. det = ({m[0][0]})({m[1][1]}) - ({m[0][1]})({m[1][0]}) = {self._det2(m)}.",
                f"3. 절대값을 취하고 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "det3":
            det_val = self._det3(m)
            return [
                f"1. 3x3 행렬의 행렬식을 여인수 전개(cofactor expansion)로 계산합니다.",
                f"2. 1행을 기준으로 전개: a11*M11 - a12*M12 + a13*M13.",
                f"3. 각 소행렬식(minor)을 2x2 행렬식으로 계산합니다.",
                f"4. det = {det_val}, 절대값의 1000 나머지 = {abs(det_val) % 1000}.",
            ]
        else:
            det_val = self._det2(m)
            adj = self._adjugate2(m)
            return [
                f"1. 2x2 행렬의 역행렬을 구합니다. det = {det_val}.",
                f"2. 수반행렬(adjugate) = [[{adj[0][0]}, {adj[0][1]}], [{adj[1][0]}, {adj[1][1]}]].",
                f"3. 수반행렬 원소 절대값 합 + |det|를 계산합니다.",
                f"4. 합계를 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Matrix
            m = seed["matrix"]
            mode = seed["mode"]
            M = Matrix(m)

            if mode == "det2" or mode == "det3":
                return abs(int(M.det())) % 1000
            else:
                det_val = int(M.det())
                if det_val == 0:
                    return 0
                adj = M.adjugate()
                elem_sum = sum(abs(int(adj[i, j])) for i in range(M.rows) for j in range(M.cols))
                return (elem_sum + abs(det_val)) % 1000
        except Exception:
            return None
