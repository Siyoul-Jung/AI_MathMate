"""
AI_MathMate V2 — 함수 성질 (algebra_functions_and_properties)
정의역, 치역, 합성함수, 역함수, 고정점 등
함수의 기본 성질을 이용한 AIME 문제를 다룹니다.
기출 빈도: 55회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraFunctionsAndPropertiesModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_functions_and_properties",
        name="함수 성질 (정의역, 치역, 합성, 역함수)",
        domain="integer",
        namespace="alg_func_prop",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'involution' | 'composition_domain' | 'fixed_points' | 'iteration'"),
            "a": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=20, description="함수 파라미터 a"),
            "b": FieldSpec(dtype=int, domain="Z", min_val=-10, max_val=20, description="함수 파라미터 b"),
            "n": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=100, description="범위/반복 횟수"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=5,
        category="algebra",
        tags=["function", "domain", "range", "composition", "inverse", "fixed_point", "involution"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["fixed_point_count", "iteration_result"],
        bridge_input_accepts=["polynomial_value"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["involution", "composition_domain", "fixed_points", "iteration"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "involution":
                # f(f(x)) = x 조건 만족하는 선형 함수 f(x) = (ax+b)/(cx+d)
                # 간소화: f(x) = a - x (자명한 인볼루션) → f(f(x))=x 해의 합
                # f(x) = n - x 이면 고정점: n-x=x → x=n/2
                # 정수 범위 [-n..n]에서 f(f(x))=x 되는 정수 x 개수 = 2n+1 (전부)
                # 더 흥미: f(x) = (ax+b)/(cx-a), ad+bc != 0, 인볼루션
                # 간소화: f(x)=(px+q) mod m, f(f(x))=x mod m 해 개수
                p = random.choice([m for m in range(2, 20) if math.gcd(m, 1) == 1])
                m = random.randint(10, 80)
                # f(x) = (m-1-x) mod m 이면 f(f(x))=x always. 해 개수 = m
                # f(x) = (p*x) mod m 이면 f(f(x))=p^2*x mod m=x iff p^2≡1 (mod m)
                # p^2 ≡ 1 (mod m) 해: p = ±1 mod m 뿐이면 자명
                # 새 접근: f:{1..n}→{1..n}, f(f(x))=x인 전사함수 개수
                # = 인볼루션(involution) 개수 a(n)
                n = random.randint(4, 14)
                seed = {"mode": mode, "a": 0, "b": 0, "n": n}

            elif mode == "composition_domain":
                # f(x) = x^2 - a, g(x) = x + b
                # f(g(x)) = (x+b)^2 - a 의 정수 해 중 |f(g(x))| <= n 인 x 개수
                a = random.randint(1, 15)
                b = random.randint(-5, 5)
                n = random.randint(10, 60)
                seed = {"mode": mode, "a": a, "b": b, "n": n}

            elif mode == "fixed_points":
                # f(x) = ax^2 + bx + c 에서 f(x)=x 해 → ax^2 + (b-1)x + c = 0
                # 정수 해의 합 = -(b-1)/a (비에타)
                # 정수 해가 존재하도록 판별식 >= 0 보장
                a = random.choice([1, 2, 3])
                # (b-1)^2 - 4ac >= 0 이고 정수근이 되도록
                r1 = random.randint(-8, 8)
                r2 = random.randint(-8, 8)
                # ax^2 + (b-1)x + c = a(x-r1)(x-r2) = a*x^2 - a(r1+r2)x + a*r1*r2
                b = 1 - a * (r1 + r2)
                c_val = a * r1 * r2
                n = abs(c_val) + abs(b)  # 사용하지 않지만 일관성을 위해
                seed = {"mode": mode, "a": a, "b": b, "n": n, "c_val": c_val}

            else:  # iteration
                # f(x) = (ax + b) mod m, f^(n)(x_0) 계산 (n번 반복 적용)
                a = random.randint(2, 7)
                b = random.randint(1, 10)
                m = random.randint(50, 200)
                n = random.randint(5, 50)
                x0 = random.randint(0, m - 1)
                seed = {"mode": mode, "a": a, "b": b, "n": n, "m": m, "x0": x0}

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"mode": "fixed_points", "a": 1, "b": -3, "n": 10, "c_val": 2}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]

        if mode == "involution":
            # {1,...,n} 위의 인볼루션 개수: a(n) = a(n-1) + (n-1)*a(n-2)
            n = seed["n"]
            if n <= 0:
                return 1
            dp = [0] * (n + 1)
            dp[0] = 1
            dp[1] = 1
            for i in range(2, n + 1):
                dp[i] = dp[i - 1] + (i - 1) * dp[i - 2]
            return dp[n] % 1000

        elif mode == "composition_domain":
            # f(g(x)) = (x+b)^2 - a, |결과| <= n 인 정수 x 개수
            a = seed["a"]
            b = seed["b"]
            n = seed["n"]
            count = 0
            # (x+b)^2 - a <= n  =>  (x+b)^2 <= n+a  =>  |x+b| <= sqrt(n+a)
            # (x+b)^2 - a >= -n =>  (x+b)^2 >= a-n
            bound = math.isqrt(n + a)
            for dx in range(-bound, bound + 1):
                val = dx * dx - a
                if abs(val) <= n:
                    count += 1
            return count % 1000

        elif mode == "fixed_points":
            # f(x)=x 고정점: ax^2+(b-1)x+c=0 의 두 근 r1,r2
            # 근의 합 = -(b-1)/a, 근의 곱 = c/a
            # 답 = |r1| + |r2| + |r1*r2|
            a_coeff = seed["a"]
            b = seed["b"]
            c_val = seed["c_val"]
            # 근 직접 계산
            disc = (b - 1) ** 2 - 4 * a_coeff * c_val
            if disc < 0:
                return 0
            sqrt_disc = math.isqrt(disc)
            if sqrt_disc * sqrt_disc != disc:
                return 0
            r1_num = -(b - 1) + sqrt_disc
            r2_num = -(b - 1) - sqrt_disc
            denom = 2 * a_coeff
            if r1_num % denom != 0 or r2_num % denom != 0:
                return 0
            r1 = r1_num // denom
            r2 = r2_num // denom
            return (abs(r1) + abs(r2) + abs(r1 * r2)) % 1000

        else:  # iteration
            # f^(n)(x0) where f(x) = (a*x + b) mod m
            a = seed["a"]
            b = seed["b"]
            m = seed["m"]
            n = seed["n"]
            x = seed["x0"]
            for _ in range(n):
                x = (a * x + b) % m
            return x % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        ans = self.execute(seed)
        mode = seed["mode"]
        fixed_count = ans if mode in ("involution", "fixed_points", "composition_domain") else 0
        return {
            "fixed_point_count": fixed_count,
            "iteration_result": ans,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]

        if mode == "involution":
            n = seed["n"]
            return [
                f"1. {{1, 2, ..., {n}}} 위의 인볼루션(f(f(x))=x인 전사함수) 개수를 구합니다.",
                f"2. 점화식 a(n) = a(n-1) + (n-1)*a(n-2)를 세웁니다.",
                f"3. a(0)=1, a(1)=1부터 a({n})까지 순차적으로 계산합니다.",
                f"4. 결과를 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "composition_domain":
            a = seed["a"]
            b = seed["b"]
            n = seed["n"]
            return [
                f"1. f(x)=x^2-{a}, g(x)=x+{b}로 놓으면 f(g(x))=(x+{b})^2-{a}입니다.",
                f"2. |f(g(x))| <= {n}을 만족하는 정수 x를 찾습니다.",
                f"3. (x+{b})^2 <= {n+a}이므로 |x+{b}| <= {math.isqrt(n+a)}입니다.",
                f"4. 범위 내 각 x에 대해 조건을 확인하고 개수를 셉니다.",
            ]
        elif mode == "fixed_points":
            a_coeff = seed["a"]
            b = seed["b"]
            c_val = seed["c_val"]
            return [
                f"1. f(x)={a_coeff}x^2+{b}x+{c_val}에서 f(x)=x를 풀어 고정점을 구합니다.",
                f"2. {a_coeff}x^2+{b-1}x+{c_val}=0으로 정리합니다.",
                f"3. 판별식과 근의 공식으로 두 근 r1, r2를 구합니다.",
                f"4. |r1|+|r2|+|r1*r2|를 계산하고 mod 1000을 취합니다.",
            ]
        else:
            a = seed["a"]
            b = seed["b"]
            m = seed["m"]
            n = seed["n"]
            x0 = seed["x0"]
            return [
                f"1. f(x)=({a}x+{b}) mod {m}를 정의합니다.",
                f"2. x_0={x0}에서 시작하여 f를 {n}번 반복 적용합니다.",
                f"3. 각 단계에서 x_(k+1) = ({a}*x_k+{b}) mod {m}를 계산합니다.",
                f"4. x_{n}의 값이 최종 답입니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            mode = seed["mode"]

            if mode == "involution":
                n = seed["n"]
                # 독립 검증: 직접 계산
                dp = [0] * (n + 1)
                dp[0] = 1
                if n >= 1:
                    dp[1] = 1
                for i in range(2, n + 1):
                    dp[i] = dp[i - 1] + (i - 1) * dp[i - 2]
                return dp[n] % 1000

            elif mode == "composition_domain":
                a = seed["a"]
                b = seed["b"]
                n = seed["n"]
                count = 0
                for x in range(-200, 201):
                    val = (x + b) ** 2 - a
                    if abs(val) <= n:
                        count += 1
                return count % 1000

            elif mode == "fixed_points":
                a_coeff = seed["a"]
                b = seed["b"]
                c_val = seed["c_val"]
                # 브루트포스 검증
                roots = []
                for x in range(-200, 201):
                    if a_coeff * x * x + b * x + c_val == x:
                        roots.append(x)
                if len(roots) == 0:
                    return 0
                return (sum(abs(r) for r in roots) + abs(math.prod(roots))) % 1000

            else:  # iteration
                a = seed["a"]
                b = seed["b"]
                m = seed["m"]
                n = seed["n"]
                x = seed["x0"]
                for _ in range(n):
                    x = (a * x + b) % m
                return x % 1000

        except Exception:
            return None
