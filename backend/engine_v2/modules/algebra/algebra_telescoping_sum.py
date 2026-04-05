"""
AI_MathMate V2 — 텔레스코핑 합 (algebra_telescoping_sum)
Sigma 1/(k(k+d)) 부분분수 또는 Sigma (f(k)-f(k+1)) 형태의 텔레스코핑 급수를 다룹니다.
기출 빈도: 10회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraTelescopingSumModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_telescoping_sum",
        name="텔레스코핑 합",
        domain="integer",
        namespace="alg_tele",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str",
                              description="유형: 'partial_fraction' | 'difference'"),
            "start": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=5,
                               description="합산 시작 인덱스"),
            "end": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=500,
                             description="합산 끝 인덱스"),
            "d": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=5,
                           description="부분분수 간격 d: 1/(k(k+d))"),
            "c": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=10,
                           description="분자 상수 c (difference 모드에서 f(k)=c*k)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999,
                                description="분자+분모 합 (기약분수) mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=5,
        category="algebra",
        tags=["telescoping", "partial_fraction", "series", "summation"],
        exam_types=["AIME"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["partial_fraction", "difference"]
        for _ in range(100):
            mode = random.choice(modes)
            start = random.randint(1, 3)

            if mode == "partial_fraction":
                d = random.randint(1, 4)
                end = random.randint(20, 400) if difficulty_hint >= 9 else random.randint(10, 100)
                c = 1  # 미사용이지만 스키마 일관성
            else:
                d = 1  # 미사용
                c = random.randint(1, 8)
                end = random.randint(15, 300) if difficulty_hint >= 9 else random.randint(10, 80)

            seed = {"mode": mode, "start": start, "end": end, "d": d, "c": c}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"mode": "partial_fraction", "start": 1, "end": 50, "d": 1, "c": 1}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        start = seed["start"]
        end = seed["end"]

        if mode == "partial_fraction":
            # Sum_{k=start}^{end} 1/(k*(k+d))
            # = (1/d) * Sum (1/k - 1/(k+d))  — 텔레스코핑
            # = (1/d) * (H(start, start+d-1) - H(end+1, end+d))
            # 여기서 H(a,b) = 1/a + 1/(a+1) + ... + 1/b
            d = seed["d"]
            # 직접 기약분수 계산: 분자/분모
            # 텔레스코핑 결과 = (1/d) * sum_{j=0}^{d-1} (1/(start+j) - 1/(end+1+j))
            from fractions import Fraction
            total = Fraction(0)
            for j in range(d):
                total += Fraction(1, start + j) - Fraction(1, end + 1 + j)
            total /= d
            # 기약분수의 분자 + 분모
            p = abs(total.numerator)
            q = total.denominator
            return (p + q) % 1000

        else:  # difference
            # Sum_{k=start}^{end} (f(k) - f(k+1)) where f(k) = c / k
            # = f(start) - f(end+1) = c/start - c/(end+1)
            c = seed["c"]
            from fractions import Fraction
            result = Fraction(c, start) - Fraction(c, end + 1)
            p = abs(result.numerator)
            q = result.denominator
            return (p + q) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        start = seed["start"]
        end = seed["end"]

        if mode == "partial_fraction":
            d = seed["d"]
            return [
                f"1. 합 Sum_{{k={start}}}^{{{end}}} 1/(k(k+{d}))을 부분분수로 분해합니다: (1/{d})(1/k - 1/(k+{d})).",
                f"2. 텔레스코핑 원리로 중간항이 소거됩니다.",
                f"3. 남는 항을 정리하여 기약분수 p/q를 구합니다.",
                f"4. (p + q) mod 1000을 계산합니다.",
            ]
        else:
            c = seed["c"]
            return [
                f"1. f(k) = {c}/k로 놓으면 합은 Sum (f(k) - f(k+1))입니다.",
                f"2. 텔레스코핑으로 f({start}) - f({end + 1}) = {c}/{start} - {c}/{end + 1}만 남습니다.",
                f"3. 기약분수로 정리하여 분자 p, 분모 q를 구합니다.",
                f"4. (p + q) mod 1000을 계산합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Rational, gcd
            mode = seed["mode"]
            start = seed["start"]
            end = seed["end"]

            if mode == "partial_fraction":
                d = seed["d"]
                total = Rational(0)
                for j in range(d):
                    total += Rational(1, start + j) - Rational(1, end + 1 + j)
                total /= d
                p = abs(total.p)
                q = total.q
                return (p + q) % 1000
            else:
                c = seed["c"]
                result = Rational(c, start) - Rational(c, end + 1)
                p = abs(result.p)
                q = result.q
                return (p + q) % 1000
        except Exception:
            return None
