"""
AI_MathMate V2 — 로그/지수 (algebra_logarithms_exponents)
로그 성질(밑 변환, 체인), 지수 방정식, 순환 로그 곱 등을 다룹니다.
기출 빈도: 61회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraLogarithmsExponentsModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_logarithms_exponents",
        name="로그/지수",
        domain="integer",
        namespace="alg_logexp",
        input_schema={
            "a": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=100, description="밑 또는 기수 a"),
            "b": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=100, description="밑 또는 기수 b"),
            "c": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=100, description="밑 또는 기수 c"),
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'cyclic_log' | 'power_tower' | 'log_sum'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=5,
        category="algebra",
        tags=["logarithm", "exponent", "change_of_base", "power_tower", "log_chain"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["log_value_num", "log_value_den"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["cyclic_log", "power_tower", "log_sum"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "cyclic_log":
                # log_a(b) * log_b(c) * log_c(a) = 1 (항상)
                # 변형: log_a(b) * log_b(c^k) 의 값 → k * log_a(c) 를 정수로 만듦
                # a = p^m, c = p^n 형태로 선택하여 정수 결과 보장
                p = random.choice([2, 3, 5, 7])
                m = random.randint(1, 4)
                n = random.randint(1, 4)
                k = random.randint(1, 5)
                a = p ** m   # a = p^m
                c = p ** n   # c = p^n
                b = random.choice([p ** i for i in range(1, 6) if p ** i != a and p ** i <= 200])
                if b is None or b == a:
                    continue
                seed = {"a": a, "b": b, "c": c, "k": k, "p": p, "m": m, "n": n, "mode": mode}

            elif mode == "power_tower":
                # a^(b^c) mod 1000 — 모듈러 지수 문제
                a = random.randint(2, 15)
                b = random.randint(2, 8)
                c = random.randint(2, 5)
                seed = {"a": a, "b": b, "c": c, "k": 0, "p": 0, "m": 0, "n": 0, "mode": mode}

            else:  # log_sum
                # floor(log_2(1)) + floor(log_2(2)) + ... + floor(log_2(n))
                # = sum of floor(log2(k)) for k=1..n
                n = random.randint(10, 500)
                seed = {"a": 2, "b": n, "c": 0, "k": 0, "p": 0, "m": 0, "n": 0, "mode": mode}

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"a": 2, "b": 8, "c": 4, "k": 2, "p": 2, "m": 1, "n": 2, "mode": "cyclic_log"}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]

        if mode == "cyclic_log":
            # log_a(b) * log_b(c^k) = k * log_a(c) = k * n / m (정수)
            k = seed["k"]
            m = seed["m"]
            n = seed["n"]
            # result = k * n / m — 기약분수의 분자+분모 합
            numerator = k * n
            denominator = m
            g = math.gcd(numerator, denominator)
            num = numerator // g
            den = denominator // g
            return (num + den) % 1000

        elif mode == "power_tower":
            # a^(b^c) mod 1000
            a, b, c = seed["a"], seed["b"], seed["c"]
            exponent = pow(b, c)
            result = pow(a, exponent, 1000)
            return result

        else:  # log_sum
            # sum of floor(log2(k)) for k = 1..b
            n = seed["b"]
            total = 0
            for k in range(1, n + 1):
                if k >= 1:
                    total += int(math.log2(k))
            return total % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        mode = seed["mode"]
        if mode == "cyclic_log":
            k, m, n = seed["k"], seed["m"], seed["n"]
            numerator = k * n
            denominator = m
            g = math.gcd(numerator, denominator)
            return {"log_value_num": numerator // g, "log_value_den": denominator // g}
        elif mode == "power_tower":
            ans = self.execute(seed)
            return {"log_value_num": ans, "log_value_den": 1}
        else:
            ans = self.execute(seed)
            return {"log_value_num": ans, "log_value_den": 1}

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]

        if mode == "cyclic_log":
            a, b, k, p, m, n = seed["a"], seed["b"], seed["k"], seed["p"], seed["m"], seed["n"]
            c = seed["c"]
            return [
                f"1. log_{a}({b}) * log_{b}({c}^{k})를 밑 변환 공식으로 정리합니다.",
                f"2. 밑 변환: log_{a}({b}) = log_{p}({b})/log_{p}({a}), log_{b}({c}^{k}) = {k}*log_{p}({c})/log_{p}({b}).",
                f"3. 곱을 정리하면 {k} * log_{p}({c}) / log_{p}({a}) = {k}*{n}/{m}입니다.",
                f"4. 기약분수로 변환 후 분자+분모 합을 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "power_tower":
            a, b, c = seed["a"], seed["b"], seed["c"]
            return [
                f"1. {a}^({b}^{c})를 계산해야 합니다.",
                f"2. 먼저 지수 {b}^{c} = {b**c}를 구합니다.",
                f"3. {a}^{b**c} mod 1000을 모듈러 지수법으로 계산합니다.",
                f"4. 오일러 정리와 반복 제곱법을 활용하여 최종값을 구합니다.",
            ]
        else:
            n = seed["b"]
            return [
                f"1. floor(log_2(k))의 합을 k=1부터 k={n}까지 구합니다.",
                f"2. floor(log_2(k)) = j인 k의 범위는 2^j <= k < 2^(j+1)입니다.",
                f"3. 각 j에 대해 기여하는 항의 수를 계산하여 합산합니다.",
                f"4. 합계를 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Rational, Integer, log, floor as sym_floor
            mode = seed["mode"]

            if mode == "cyclic_log":
                k, m, n = seed["k"], seed["m"], seed["n"]
                val = Rational(k * n, m)
                return (int(val.p) + int(val.q)) % 1000
            elif mode == "power_tower":
                a, b, c = seed["a"], seed["b"], seed["c"]
                exponent = int(Integer(b) ** Integer(c))
                result = pow(a, exponent, 1000)
                return result
            else:
                n = seed["b"]
                total = sum(int(math.log2(k)) for k in range(1, n + 1))
                return total % 1000
        except Exception:
            return None
