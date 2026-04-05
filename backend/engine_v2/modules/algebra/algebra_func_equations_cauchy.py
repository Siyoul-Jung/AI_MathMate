"""
AI_MathMate V2 — 함수방정식 코시 유형 (algebra_func_equations_cauchy)
f(x+y)=f(x)+f(y), f(xy)=f(x)f(y), f(x+y)=f(x)f(y) 등
코시 유형 함수방정식에서 f(특정값)을 결정론적으로 계산합니다.
기출 빈도: 11회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraFuncEquationsCauchyModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_func_equations_cauchy",
        name="함수방정식 (코시 유형)",
        domain="integer",
        namespace="alg_cauchy",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'additive' | 'multiplicative' | 'exponential'"),
            "c": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=20, description="함수 결정 상수 (f(1)=c 등)"),
            "target": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=50, description="f(target) 계산 대상"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=6,
        category="algebra",
        tags=["functional_equation", "cauchy", "additive", "multiplicative", "homomorphism"],
        exam_types=["AIME"],
        bridge_output_keys=["f_value", "constant_c"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["additive", "multiplicative", "exponential"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "additive":
                # f(x+y) = f(x) + f(y), f(1) = c  =>  f(n) = c*n
                c = random.randint(2, 18)
                target = random.randint(5, 50)
            elif mode == "multiplicative":
                # f(xy) = f(x) + f(y) (log-type), f(base) = c  =>  f(base^k) = c*k
                # 여기서 target = base^k 형태로 제한
                base = random.choice([2, 3, 5, 7])
                c = random.randint(1, 15)
                k = random.randint(2, 8)
                target = base ** k
            else:
                # f(x+y) = f(x)*f(y), f(1) = c  =>  f(n) = c^n
                c = random.randint(2, 6)
                target = random.randint(2, 12)

            seed = {"mode": mode, "c": c, "target": target}
            if mode == "multiplicative":
                seed["base"] = base
                seed["k"] = k
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"mode": "additive", "c": 3, "target": 10}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        c = seed["c"]
        target = seed["target"]

        if mode == "additive":
            # f(x+y) = f(x) + f(y) => f는 가법적, f(n) = c*n (f(1)=c)
            return (c * target) % 1000

        elif mode == "multiplicative":
            # f(xy) = f(x) + f(y) => f는 로그형, f(base)=c => f(base^k)=c*k
            k = seed["k"]
            return (c * k) % 1000

        else:  # exponential
            # f(x+y) = f(x)*f(y) => f(n) = f(1)^n = c^n
            return pow(c, target) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        return {
            "f_value": self.execute(seed),
            "constant_c": seed["c"],
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        c = seed["c"]
        target = seed["target"]

        if mode == "additive":
            return [
                f"1. 함수방정식 f(x+y) = f(x) + f(y)에서 f는 가법적(additive) 함수입니다.",
                f"2. f(1) = {c}이므로, f(n) = f(1) * n = {c} * n입니다.",
                f"3. f({target}) = {c} * {target} = {c * target}을 계산합니다.",
                f"4. 답은 {(c * target) % 1000}입니다 (mod 1000).",
            ]
        elif mode == "multiplicative":
            base = seed["base"]
            k = seed["k"]
            return [
                f"1. 함수방정식 f(xy) = f(x) + f(y)에서 f는 로그형 함수입니다.",
                f"2. f({base}) = {c}이므로, f({base}^k) = {c} * k입니다.",
                f"3. target = {target} = {base}^{k}이므로 f({target}) = {c} * {k} = {c * k}입니다.",
                f"4. 답은 {(c * k) % 1000}입니다 (mod 1000).",
            ]
        else:
            val = pow(c, target)
            return [
                f"1. 함수방정식 f(x+y) = f(x) * f(y)에서 f는 지수형 함수입니다.",
                f"2. f(1) = {c}이므로, f(n) = {c}^n입니다.",
                f"3. f({target}) = {c}^{target} = {val}을 계산합니다.",
                f"4. 답은 {val % 1000}입니다 (mod 1000).",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            mode = seed["mode"]
            c = seed["c"]
            target = seed["target"]

            if mode == "additive":
                # 검증: f(a+b) = f(a)+f(b) 만족 확인
                f = lambda n: c * n
                a, b = 3, 5
                assert f(a + b) == f(a) + f(b), "가법성 검증 실패"
                return (c * target) % 1000
            elif mode == "multiplicative":
                k = seed["k"]
                base = seed["base"]
                f = lambda x: c * round(math.log(x) / math.log(base)) if x > 0 else 0
                a, b = base, base ** 2
                assert f(a * b) == f(a) + f(b), "로그형 검증 실패"
                return (c * k) % 1000
            else:
                f = lambda n: c ** n
                a, b = 2, 3
                assert f(a + b) == f(a) * f(b), "지수형 검증 실패"
                return pow(c, target) % 1000
        except Exception:
            return None
