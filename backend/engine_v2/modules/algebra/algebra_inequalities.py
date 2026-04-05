"""
AI_MathMate V2 — 부등식 (algebra_inequalities)
AM-GM, Cauchy-Schwarz, Power Mean 등을 이용한 최솟값/최댓값 계산 문제.
x+y+z=S, xyz=P 등의 제약 조건 하에서 대칭식의 극값을 결정론적으로 구합니다.
기출 빈도: 75회
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class AlgebraInequalitiesModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_inequalities",
        name="부등식 (AM-GM, Cauchy-Schwarz)",
        domain="integer",
        namespace="alg_ineq",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str", description="문제 유형: 'amgm_min' | 'amgm_product' | 'cauchy_schwarz' | 'power_mean'"),
            "s": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=100, description="변수 합 S"),
            "k": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=5, description="변수 개수"),
            "p": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=50, description="추가 파라미터"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="최종 정수 답"),
        },
        logic_depth=4,
        daps_contribution=4.5,
        min_difficulty=6,
        category="algebra",
        tags=["inequality", "AM-GM", "cauchy_schwarz", "power_mean", "optimization", "minimum", "maximum"],
        exam_types=["AIME", "AMC"],
        bridge_output_keys=["extremal_value", "sum_constraint"],
        bridge_input_accepts=["polynomial_value", "constant_c"],
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> dict[str, Any]:
        modes = ["amgm_min", "amgm_product", "cauchy_schwarz", "power_mean"]
        for _ in range(100):
            mode = random.choice(modes)

            if mode == "amgm_min":
                # x1+x2+...+xk = S (양의 실수), x1^2+x2^2+...+xk^2의 최솟값
                # QM-AM: 최솟값은 모두 같을 때 = S^2/k
                # 답 = floor(S^2 / k)
                k = random.randint(2, 5)
                s = random.randint(k, 60)
                p = k  # 사용하지 않지만 구조 일관성
                seed = {"mode": mode, "s": s, "k": k, "p": p}

            elif mode == "amgm_product":
                # x1+x2+...+xk = S (양의 정수), x1*x2*...*xk의 최댓값
                # AM-GM: 모두 S/k일 때 최대 → (S/k)^k
                # 정수 제약: S = qk + r → r개는 (q+1), (k-r)개는 q
                # 최대 곱 = q^(k-r) * (q+1)^r
                k = random.randint(2, 5)
                s = random.randint(k + 2, 50)
                p = 0
                seed = {"mode": mode, "s": s, "k": k, "p": p}

            elif mode == "cauchy_schwarz":
                # (a1^2+a2^2+...+ak^2)(b1^2+b2^2+...+bk^2) >= (a1*b1+...+ak*bk)^2
                # 구체화: a_i = x_i, b_i = 1 → (Σx_i^2)*k >= S^2
                # Σ(1/x_i) * Σ(x_i) >= k^2 (Cauchy-Schwarz)
                # x1+...+xk = S일 때 Σ(1/x_i)의 최솟값 = k^2/S
                # 답 = floor(k^2 * p / S) (p는 스케일링)
                k = random.randint(2, 5)
                s = random.randint(k, 40)
                p = random.randint(5, 30)
                seed = {"mode": mode, "s": s, "k": k, "p": p}

            else:  # power_mean
                # x+y = S, x^p + y^p의 최솟값 (양의 실수, p >= 2)
                # 최솟값은 x=y=S/2일 때: 2*(S/2)^p = S^p / 2^(p-1)
                # 답 = floor(S^p / 2^(p-1))
                k = 2
                s = random.randint(4, 30)
                p = random.randint(2, 5)
                seed = {"mode": mode, "s": s, "k": k, "p": p}

            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed

        return {"mode": "amgm_min", "s": 12, "k": 3, "p": 3}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        s = seed["s"]
        k = seed["k"]
        p = seed["p"]

        if mode == "amgm_min":
            # x1+...+xk = S, Σxi^2의 최솟값 = S^2 / k (Cauchy-Schwarz / QM-AM)
            # floor(S^2 / k) → 정수 답
            return (s * s // k) % 1000

        elif mode == "amgm_product":
            # 양의 정수 x1+...+xk = S, Πxi 최대
            # 가능한 한 균등하게: q = S // k, r = S % k
            q = s // k
            r = s % k
            if q == 0:
                return 0
            product = pow(q, k - r) * pow(q + 1, r)
            return product % 1000

        elif mode == "cauchy_schwarz":
            # x1+...+xk = S (양의 실수), Σ(1/xi)의 최솟값 = k^2/S
            # 답 = floor(k^2 * p / S)
            return (k * k * p // s) % 1000

        else:  # power_mean
            # x+y = S (양의 실수), x^p + y^p의 최솟값 = S^p / 2^(p-1)
            numerator = s ** p
            denominator = 2 ** (p - 1)
            return (numerator // denominator) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        return {
            "extremal_value": self.execute(seed),
            "sum_constraint": seed["s"],
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        s = seed["s"]
        k = seed["k"]
        p = seed["p"]

        if mode == "amgm_min":
            return [
                f"1. 양의 실수 x_1+...+x_{k}={s}에서 Σx_i^2의 최솟값을 구합니다.",
                f"2. QM-AM 부등식: (Σx_i^2)/{k} >= (Σx_i/{k})^2 이므로 Σx_i^2 >= {s}^2/{k}입니다.",
                f"3. 등호 조건: 모든 x_i = {s}/{k}일 때 달성됩니다.",
                f"4. 최솟값 = {s*s}//{k} = {s*s//k}이고, mod 1000을 취합니다.",
            ]
        elif mode == "amgm_product":
            q = s // k
            r = s % k
            return [
                f"1. 양의 정수 x_1+...+x_{k}={s}에서 Πx_i의 최댓값을 구합니다.",
                f"2. AM-GM에 의해 값들을 가능한 한 균등하게 배분합니다.",
                f"3. {s} = {k}*{q}+{r}이므로, {r}개는 {q+1}, {k-r}개는 {q}입니다.",
                f"4. 최대 곱 = {q}^{k-r} * {q+1}^{r}을 계산하고 mod 1000을 취합니다.",
            ]
        elif mode == "cauchy_schwarz":
            return [
                f"1. 양의 실수 x_1+...+x_{k}={s}에서 Σ(1/x_i)의 최솟값을 구합니다.",
                f"2. Cauchy-Schwarz: (Σx_i)(Σ1/x_i) >= {k}^2 이므로 Σ(1/x_i) >= {k*k}/{s}입니다.",
                f"3. 스케일링 p={p}를 적용: 답 = floor({k*k}*{p}/{s}) = {k*k*p//s}입니다.",
                f"4. 결과를 mod 1000으로 취합니다.",
            ]
        else:
            return [
                f"1. 양의 실수 x+y={s}에서 x^{p}+y^{p}의 최솟값을 구합니다.",
                f"2. 멱평균 부등식(Power Mean)에 의해 x=y={s}/2일 때 최소입니다.",
                f"3. 최솟값 = 2*({s}/2)^{p} = {s}^{p}/2^{p-1} = {s**p}//{2**(p-1)}입니다.",
                f"4. = {s**p // 2**(p-1)}이고, mod 1000을 취합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            mode = seed["mode"]
            s = seed["s"]
            k = seed["k"]
            p = seed["p"]

            if mode == "amgm_min":
                # 검증: 모두 s/k일 때 합 = k * (s/k)^2 = s^2/k
                val = k * (s / k) ** 2
                return int(val) % 1000

            elif mode == "amgm_product":
                q = s // k
                r = s % k
                if q == 0:
                    return 0
                product = pow(q, k - r) * pow(q + 1, r)
                # 검증: 합이 s인지 확인
                total = q * (k - r) + (q + 1) * r
                assert total == s, f"합 불일치: {total} != {s}"
                return product % 1000

            elif mode == "cauchy_schwarz":
                # 검증: 모두 s/k일 때 Σ(1/xi) = k/(s/k) = k^2/s
                val = k * k / s
                return int(val * p) % 1000

            else:
                numerator = s ** p
                denominator = 2 ** (p - 1)
                # 검증: x=y=s/2 대입
                half = s / 2
                val = 2 * (half ** p)
                assert abs(val - numerator / denominator) < 1e-9, "Power mean 검증 실패"
                return (numerator // denominator) % 1000

        except Exception:
            return None
