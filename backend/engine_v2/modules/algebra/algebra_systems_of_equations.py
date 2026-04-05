"""
AI_MathMate V2 — 연립방정식 (algebra_systems_of_equations)
2~3변수 정수해 연립방정식을 생성하고, 해의 합 또는 곱을 구합니다.
기출 빈도: 86회
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraSystemsOfEquationsModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_systems_of_equations",
        name="연립방정식",
        domain="integer",
        namespace="alg_sys_eq",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str", description="변수 개수: '2var' | '3var'"),
            "result_type": FieldSpec(dtype=str, domain="str", description="결과 유형: 'sum' | 'product'"),
            "x": FieldSpec(dtype=int, domain="Z", min_val=-30, max_val=30, description="해 x"),
            "y": FieldSpec(dtype=int, domain="Z", min_val=-30, max_val=30, description="해 y"),
            "z": FieldSpec(dtype=int, domain="Z", min_val=-30, max_val=30, description="해 z (3var 모드)"),
            "a11": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="계수 행렬 (1,1)"),
            "a12": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="계수 행렬 (1,2)"),
            "a21": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="계수 행렬 (2,1)"),
            "a22": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=10, description="계수 행렬 (2,2)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="해의 합 또는 곱 (mod 1000)"),
        },
        logic_depth=4,
        daps_contribution=3.5,
        min_difficulty=2,
        category="algebra",
        tags=["linear_system", "substitution", "elimination", "cramer", "integer_solution"],
        exam_types=["AIME", "AMC"],
    )

    def generate_seed(self, difficulty_hint: float = 6.0) -> dict[str, Any]:
        for _ in range(100):
            mode = "3var" if difficulty_hint >= 10 and random.random() < 0.5 else "2var"
            result_type = random.choice(["sum", "product"])

            if mode == "2var":
                seed = self._gen_2var(result_type)
            else:
                seed = self._gen_3var(result_type)

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        # Fallback: x=3, y=5, trivial system
        return {
            "mode": "2var", "result_type": "sum",
            "x": 3, "y": 5, "z": 0,
            "a11": 1, "a12": 1, "a21": 1, "a22": -1,
        }

    def _gen_2var(self, result_type: str) -> dict[str, Any]:
        """정수해 (x, y)를 먼저 고르고, 비특이 계수 행렬을 만든다."""
        x = random.randint(-20, 20)
        y = random.randint(-20, 20)
        while True:
            a11 = random.randint(-8, 8)
            a12 = random.randint(-8, 8)
            a21 = random.randint(-8, 8)
            a22 = random.randint(-8, 8)
            det = a11 * a22 - a12 * a21
            if det != 0 and any(v != 0 for v in [a11, a12]) and any(v != 0 for v in [a21, a22]):
                break
        return {
            "mode": "2var", "result_type": result_type,
            "x": x, "y": y, "z": 0,
            "a11": a11, "a12": a12, "a21": a21, "a22": a22,
        }

    def _gen_3var(self, result_type: str) -> dict[str, Any]:
        """3변수 시스템 — 해를 먼저 정하고 계수를 샘플링. seed에 3x3 계수 저장."""
        x = random.randint(-15, 15)
        y = random.randint(-15, 15)
        z = random.randint(-15, 15)
        # 간결한 seed를 위해 대각 우세 행렬을 생성
        while True:
            coeffs = [[random.randint(-5, 5) for _ in range(3)] for _ in range(3)]
            # 행렬식 != 0 체크 (3x3 사루스)
            d = (coeffs[0][0] * (coeffs[1][1] * coeffs[2][2] - coeffs[1][2] * coeffs[2][1])
                 - coeffs[0][1] * (coeffs[1][0] * coeffs[2][2] - coeffs[1][2] * coeffs[2][0])
                 + coeffs[0][2] * (coeffs[1][0] * coeffs[2][1] - coeffs[1][1] * coeffs[2][0]))
            if d != 0:
                break
        # seed 내 계수를 flat 으로 저장 (a11~a33)
        return {
            "mode": "3var", "result_type": result_type,
            "x": x, "y": y, "z": z,
            # 2var 호환 필드 (사용 안 함이지만 스키마 일관성)
            "a11": coeffs[0][0], "a12": coeffs[0][1], "a21": coeffs[1][0], "a22": coeffs[1][1],
            # 3var 확장 계수
            "a13": coeffs[0][2],
            "a23": coeffs[1][2],
            "a31": coeffs[2][0], "a32": coeffs[2][1], "a33": coeffs[2][2],
        }

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        result_type = seed["result_type"]
        x, y, z = seed["x"], seed["y"], seed.get("z", 0)

        if mode == "2var":
            val = (x + y) if result_type == "sum" else (x * y)
        else:
            val = (x + y + z) if result_type == "sum" else (x * y * z)

        return abs(val) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        x, y, z = seed["x"], seed["y"], seed.get("z", 0)
        result_type = seed["result_type"]

        if mode == "2var":
            a11, a12 = seed["a11"], seed["a12"]
            a21, a22 = seed["a21"], seed["a22"]
            b1 = a11 * x + a12 * y
            b2 = a21 * x + a22 * y
            val = (x + y) if result_type == "sum" else (x * y)
            return [
                f"1. 연립방정식: {a11}x + {a12}y = {b1}, {a21}x + {a22}y = {b2}를 세웁니다.",
                f"2. 소거법 또는 크라메르 공식으로 x, y를 구합니다.",
                f"3. x = {x}, y = {y}을(를) 얻습니다.",
                f"4. 해의 {'합' if result_type == 'sum' else '곱'} = {val}, |{val}| mod 1000 = {abs(val) % 1000}.",
            ]
        else:
            val = (x + y + z) if result_type == "sum" else (x * y * z)
            return [
                "1. 3변수 연립방정식 3개를 세웁니다.",
                "2. 가우스 소거법으로 변수를 하나씩 제거합니다.",
                f"3. x = {x}, y = {y}, z = {z}을(를) 얻습니다.",
                f"4. 해의 {'합' if result_type == 'sum' else '곱'} = {val}, |{val}| mod 1000 = {abs(val) % 1000}.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Matrix, symbols, Eq, solve
            mode = seed["mode"]
            result_type = seed["result_type"]
            sx, sy, sz = symbols('x y z')

            if mode == "2var":
                a11, a12 = seed["a11"], seed["a12"]
                a21, a22 = seed["a21"], seed["a22"]
                x_val, y_val = seed["x"], seed["y"]
                b1 = a11 * x_val + a12 * y_val
                b2 = a21 * x_val + a22 * y_val

                sol = solve([Eq(a11 * sx + a12 * sy, b1),
                             Eq(a21 * sx + a22 * sy, b2)], [sx, sy])
                if not sol:
                    return None
                xr, yr = int(sol[sx]), int(sol[sy])
                val = (xr + yr) if result_type == "sum" else (xr * yr)
                return abs(val) % 1000
            else:
                coeffs = [
                    [seed["a11"], seed["a12"], seed.get("a13", 0)],
                    [seed["a21"], seed["a22"], seed.get("a23", 0)],
                    [seed.get("a31", 1), seed.get("a32", 0), seed.get("a33", 1)],
                ]
                x_val, y_val, z_val = seed["x"], seed["y"], seed["z"]
                rhs = [sum(coeffs[i][j] * [x_val, y_val, z_val][j] for j in range(3)) for i in range(3)]
                eqs = [Eq(coeffs[i][0] * sx + coeffs[i][1] * sy + coeffs[i][2] * sz, rhs[i]) for i in range(3)]
                sol = solve(eqs, [sx, sy, sz])
                if not sol:
                    return None
                xr, yr, zr = int(sol[sx]), int(sol[sy]), int(sol[sz])
                val = (xr + yr + zr) if result_type == "sum" else (xr * yr * zr)
                return abs(val) % 1000
        except Exception:
            return None
