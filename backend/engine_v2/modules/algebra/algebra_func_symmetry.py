"""
AI_MathMate V2 — 함수 대칭성 (algebra_func_symmetry)
짝함수/홀함수 판별, f(a-x)=f(a+x) 대칭축, f(x)+f(-x)=g(x) 조건 등
대칭성을 이용한 합/차 계산 문제를 다룹니다.
기출 빈도: 12회
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraFuncSymmetryModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_func_symmetry",
        name="함수 대칭성 (짝/홀 함수)",
        domain="integer",
        namespace="alg_sym",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'even_odd_sum' | 'axis_symmetry' | 'periodic_sum'"),
            "coeffs": FieldSpec(dtype=list, domain="Z", description="다항식 계수 리스트 [a_n, ..., a_0]"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=50, description="합산 범위 또는 대칭축 파라미터"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=6,
        category="algebra",
        tags=["even_function", "odd_function", "symmetry", "axis_of_symmetry", "polynomial"],
        exam_types=["AIME"],
        bridge_output_keys=["symmetry_sum", "axis"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["even_odd_sum", "axis_symmetry", "periodic_sum"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "even_odd_sum":
                # f(x) = ax^3 + bx^2 + cx + d (짝수부 + 홀수부 분리)
                # f(x)+f(-x) = 2(bx^2+d), 합산: sum_{x=1}^{n} [f(x)+f(-x)]
                a = random.randint(-5, 5)
                b = random.randint(1, 8)
                c = random.randint(-5, 5)
                d = random.randint(0, 10)
                n = random.randint(3, 15)
                seed = {"mode": mode, "coeffs": [a, b, c, d], "n": n}

            elif mode == "axis_symmetry":
                # f(x) = a(x-h)^2 + k, 대칭축 x=h
                # sum_{x=h-n}^{h+n} f(x) = (2n+1)*k + 2a*sum_{i=1}^{n} i^2
                a_coeff = random.randint(1, 5)
                h = random.randint(1, 10)
                k = random.randint(0, 15)
                n = random.randint(2, 10)
                seed = {"mode": mode, "coeffs": [a_coeff, h, k], "n": n}

            else:  # periodic_sum
                # f(x) + f(x+p) = S (상수), sum_{x=1}^{2mp} f(x) = m*p*S
                # 구체적: f(x) = ax^2 mod M, p = M, f(x)+f(p-x) = S 조건
                # 간소화: f(x) = x mod p, f(x)+f(p-x) = p
                # sum_{x=1}^{2n*p} f(x) via 쌍 묶기
                p = random.randint(3, 12)
                n_pairs = random.randint(2, 8)
                seed = {"mode": mode, "coeffs": [p], "n": n_pairs}

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"mode": "even_odd_sum", "coeffs": [1, 2, 1, 3], "n": 5}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        coeffs = seed["coeffs"]
        n = seed["n"]

        if mode == "even_odd_sum":
            # f(x) = ax^3 + bx^2 + cx + d
            # f(x)+f(-x) = 2bx^2 + 2d (홀수 항 소거)
            a, b, c, d = coeffs
            # sum_{x=1}^{n} [f(x)+f(-x)] = sum_{x=1}^{n} (2b*x^2 + 2d)
            total = sum(2 * b * x * x + 2 * d for x in range(1, n + 1))
            return abs(total) % 1000

        elif mode == "axis_symmetry":
            # f(x) = a_coeff*(x-h)^2 + k
            # sum_{x=h-n}^{h+n} f(x) = (2n+1)*k + 2*a_coeff * sum_{i=1}^{n} i^2
            a_coeff, h, k = coeffs
            sum_sq = n * (n + 1) * (2 * n + 1) // 6
            total = (2 * n + 1) * k + 2 * a_coeff * sum_sq
            return abs(total) % 1000

        else:  # periodic_sum
            # f(x) = ((x-1) mod p) + 1 이면 f(x)+f(p+1-x) = p+2 (1-indexed 쌍)
            # 간소화: f(x) = x mod p, 그러면 한 주기 [0..p-1] 합 = p(p-1)/2
            # n_pairs 주기만큼 합산: n_pairs * p * (p-1) / 2
            p = coeffs[0]
            n_pairs = n
            # 2*n_pairs*p 개 항의 합 = n_pairs 주기 * 2 * (한 주기 합)
            # 한 주기 [1..p] 에서 x mod p: 1,2,...,p-1,0 → 합 = p(p-1)/2
            one_cycle = p * (p - 1) // 2
            total = 2 * n_pairs * one_cycle
            return total % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        mode = seed["mode"]
        ans = self.execute(seed)
        axis = 0
        if mode == "axis_symmetry":
            axis = seed["coeffs"][1]  # h
        return {
            "symmetry_sum": ans,
            "axis": axis,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        coeffs = seed["coeffs"]
        n = seed["n"]

        if mode == "even_odd_sum":
            a, b, c, d = coeffs
            return [
                f"1. f(x) = {a}x^3 + {b}x^2 + {c}x + {d}에서 f(x)+f(-x)를 계산합니다.",
                f"2. 홀수 차항(x^3, x)은 소거되어 f(x)+f(-x) = {2*b}x^2 + {2*d}입니다.",
                f"3. x=1부터 {n}까지 합산: Σ({2*b}x^2 + {2*d})을 구합니다.",
                f"4. {2*b} * Σx^2 + {2*d} * {n}을 계산하고 mod 1000을 취합니다.",
            ]
        elif mode == "axis_symmetry":
            a_coeff, h, k = coeffs
            return [
                f"1. f(x) = {a_coeff}(x-{h})^2 + {k}는 x={h}에 대해 대칭입니다.",
                f"2. x={h-n}부터 {h+n}까지 합산 시 대칭 쌍을 묶습니다.",
                f"3. 합 = (2*{n}+1)*{k} + 2*{a_coeff}*(1^2+2^2+...+{n}^2)로 정리합니다.",
                f"4. Σi^2 = {n}*{n+1}*{2*n+1}/6을 대입하여 최종 답을 구합니다.",
            ]
        else:
            p = coeffs[0]
            return [
                f"1. f(x) = x mod {p}에서 f(x)+f({p}-x) 쌍의 합이 일정함을 관찰합니다.",
                f"2. 한 주기 [0,{p}-1]의 합 = {p}*({p}-1)/2 = {p*(p-1)//2}입니다.",
                f"3. {n}쌍의 두 주기(2*{n}*{p}개 항)를 합산합니다.",
                f"4. 총합 = 2*{n}*{p*(p-1)//2} = {2*n*p*(p-1)//2}이고, mod 1000을 취합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            mode = seed["mode"]
            coeffs = seed["coeffs"]
            n = seed["n"]

            if mode == "even_odd_sum":
                a, b, c, d = coeffs
                f = lambda x: a * x**3 + b * x**2 + c * x + d
                total = sum(f(x) + f(-x) for x in range(1, n + 1))
                return abs(total) % 1000

            elif mode == "axis_symmetry":
                a_coeff, h, k = coeffs
                f = lambda x: a_coeff * (x - h) ** 2 + k
                total = sum(f(x) for x in range(h - n, h + n + 1))
                return abs(total) % 1000

            else:
                p = coeffs[0]
                n_pairs = n
                f = lambda x: x % p
                total = sum(f(x) for x in range(2 * n_pairs * p))
                return total % 1000

        except Exception:
            return None
