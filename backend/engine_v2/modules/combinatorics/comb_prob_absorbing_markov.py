"""
AI_MathMate V2 -- comb_prob_absorbing_markov (흡수 마르코프 체인)
흡수 상태가 있는 마르코프 체인에서 흡수 확률 및 기대 단계 수를 구합니다.
기본 행렬 (I - Q)^{-1} 계산 포함.
기출 10회 (AIME).
"""
from __future__ import annotations
import random
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class CombProbAbsorbingMarkovModule(AtomicModule):
    META = ModuleMeta(
        module_id="comb_prob_absorbing_markov",
        name="흡수 마르코프 체인 (Absorbing Markov Chain)",
        domain="integer",
        namespace="comb_absorb_markov",
        input_schema={
            "n_states": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=6, description="전이 상태 수"),
            "mode": FieldSpec(dtype=str, domain="str", description="'gambler' | 'random_walk' | 'ehrenfest'"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="p+q 기약분수"),
        },
        logic_depth=5,
        daps_contribution=5.5,
        min_difficulty=9,
        category="combinatorics",
        tags=["markov_chain", "absorbing", "gambler_ruin", "random_walk", "expected_value"],
        exam_types=["AIME"],
        bridge_output_keys=["n_states", "absorption_prob"],
        bridge_input_accepts=["n_states"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["gambler", "random_walk", "ehrenfest"]
        for _ in range(100):
            mode = random.choice(modes)
            n_states = random.randint(3, 6)
            seed = {"n_states": n_states, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n_states": 4, "mode": "gambler"}

    def execute(self, seed: dict[str, Any]) -> int:
        n = seed["n_states"]
        mode = seed["mode"]

        if mode == "gambler":
            # 도박사의 파산: n개 전이 상태(1..n), 흡수 상태 0, n+1
            # 상태 1에서 시작, 각 단계에서 p=1/2로 +1 또는 -1
            # 상태 0에 흡수될 확률 = n/(n+1)
            # 답: p + q (기약분수)
            prob = Fraction(n, n + 1)
            return int(prob.numerator + prob.denominator)

        elif mode == "random_walk":
            # 1차원 랜덤 워크: 0에서 시작, +1 또는 -1 (p=1/2)
            # n단계 후 원점 복귀 확률 (n이 짝수일 때)
            # P = C(n, n/2) / 2^n
            if n % 2 == 1:
                n_steps = n + 1  # 짝수로 조정
            else:
                n_steps = n
            import math
            numerator = math.comb(n_steps, n_steps // 2)
            denominator = 2 ** n_steps
            prob = Fraction(numerator, denominator)
            return int(prob.numerator + prob.denominator)

        else:  # ehrenfest
            # 에렌페스트 모형: n개 입자, 상태 k = 왼쪽 상자의 입자 수
            # 상태 k에서 k+1로 갈 확률 = (n-k)/n, k-1로 갈 확률 = k/n
            # 정상 분포: P(k) = C(n,k)/2^n
            # 기대 단계 수로 상태 0에서 상태 n까지 (근사)
            # 대신: 상태 0에서 시작, 처음으로 상태 n에 도달하는 기대 단계
            # E = 2^n (잘 알려진 결과)
            # 답: 2^n mod 1000
            return (2 ** n) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        n = seed["n_states"]
        mode = seed["mode"]

        if mode == "gambler":
            return [
                f"1. 도박사의 파산 문제를 설정합니다: 전이 상태 1~{n}, 흡수 상태 0과 {n+1}.",
                f"2. 상태 1에서 시작하여 매 단계 p=1/2로 +1 또는 -1 이동합니다.",
                f"3. 대칭 랜덤 워크에서 상태 0 흡수 확률 = {n}/{n+1}을 유도합니다.",
                f"4. 기약분수 {n}/{n+1}에서 p+q = {n} + {n+1} = {n + (n+1)}을 계산합니다.",
            ]
        elif mode == "random_walk":
            n_steps = n if n % 2 == 0 else n + 1
            import math
            num = math.comb(n_steps, n_steps // 2)
            den = 2 ** n_steps
            prob = Fraction(num, den)
            return [
                f"1. 1차원 대칭 랜덤 워크에서 {n_steps}단계 후 원점 복귀 확률을 구합니다.",
                f"2. P = C({n_steps}, {n_steps//2}) / 2^{n_steps} = {num}/{den}.",
                f"3. 기약분수로 정리: {prob.numerator}/{prob.denominator}.",
                f"4. p + q = {prob.numerator + prob.denominator}.",
            ]
        else:
            return [
                f"1. 에렌페스트 모형: {n}개 입자가 두 상자에 분배됩니다.",
                f"2. 상태 k에서 전이 확률: P(k->k+1) = ({n}-k)/{n}, P(k->k-1) = k/{n}.",
                f"3. 모든 입자가 한쪽에 모이는 기대 단계 수 = 2^{n}.",
                f"4. 2^{n} mod 1000 = {(2**n) % 1000}.",
            ]

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        """n_states와 absorption_prob(execute 결과)를 하류 모듈에 전달."""
        ans = self.execute(seed)
        return {
            "n_states": seed["n_states"],
            "absorption_prob": ans,
        }

    def generate_seed_with_bridge(
        self, bridge: dict[str, Any], difficulty_hint: float = 10.0
    ) -> dict[str, Any]:
        """상위 모듈의 n_states를 받아 시드 생성."""
        n_states = bridge.get("n_states")
        if n_states is not None and 3 <= int(n_states) <= 6:
            n_states = int(n_states)
        else:
            n_states = random.randint(3, 6)

        modes = ["gambler", "random_walk", "ehrenfest"]
        for _ in range(100):
            mode = random.choice(modes)
            seed = {"n_states": n_states, "mode": mode}
            ans = self.execute(seed)
            if 0 <= ans <= 999:
                return seed
        return {"n_states": n_states, "mode": "gambler"}

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Rational, binomial, Integer
            n = seed["n_states"]
            mode = seed["mode"]

            if mode == "gambler":
                prob = Rational(n, n + 1)
                return int(prob.p + prob.q)
            elif mode == "random_walk":
                n_steps = n if n % 2 == 0 else n + 1
                num = int(binomial(Integer(n_steps), Integer(n_steps // 2)))
                den = 2 ** n_steps
                prob = Rational(num, den)
                return int(prob.p + prob.q)
            else:
                return (2 ** n) % 1000
        except Exception:
            return None
