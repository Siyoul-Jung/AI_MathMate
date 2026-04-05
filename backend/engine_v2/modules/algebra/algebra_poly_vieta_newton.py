"""
AI_MathMate V2 — 고차 다항식과 뉴턴의 합 (algebra_poly_vieta_newton)
비에타의 정리(Vieta's Formulas)와 뉴턴의 합(Newton's Sums)을 결합하여 고난도 대칭식 문제를 생성합니다.
기존 algebra_polynomials_vieta 모듈의 기능을 포함하며 상위 개념인 Newton's Sum을 중심으로 통합되었습니다.
"""
from __future__ import annotations
import random
import sympy as sp
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class AlgebraPolyVietaNewtonModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_poly_vieta_newton",
        name="고차 다항식과 뉴턴의 합",
        domain="integer",
        namespace="alg_vieta_newton",
        input_schema={
            "degree": FieldSpec(dtype=int, domain="[3, 5]", description="다항식의 차수"),
            "target_power": FieldSpec(dtype=int, domain="[3, 8]", description="구하고자 하는 거듭제곱 합의 지수 n"),
            "roots": FieldSpec(dtype=list, domain="Z", description="다항식의 근 (생성 시 암호화)")
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z", description="S_n (근의 n제곱 합)"),
            "polynomial_coeffs": FieldSpec(dtype=list, domain="Z", description="다항식의 계수 [a_n, ..., a_0]")
        },
        logic_depth=5,
        daps_contribution=5.0,
        min_difficulty=13,
        category="algebra",
        tags=["vieta", "newton_sums", "symmetric_polynomials"],
        bridge_output_keys=["power_sum", "degree"],
        bridge_input_accepts=["root_abs_sum", "polynomial_degree"],
    )

    def generate_seed(self, difficulty_hint: float = 13.0) -> dict[str, Any]:
        degree = random.randint(3, 4) if difficulty_hint < 14 else 5
        roots = [random.randint(-5, 5) for _ in range(degree)]
        # 중복 근 방지 및 0 제외 (난이도 조절)
        roots = list(set([r for r in roots if r != 0]))
        while len(roots) < degree:
            new_r = random.randint(-7, 7)
            if new_r not in roots and new_r != 0:
                roots.append(new_r)
        
        return {
            "degree": degree,
            "target_power": random.randint(degree, degree + 3),
            "roots": roots
        }

    def execute(self, seed: dict[str, Any]) -> int:
        """S_n = sum(r_i^n) mod 1000을 반환."""
        roots = seed["roots"]
        n = seed["target_power"]
        answer = sum(r ** n for r in roots)
        return abs(answer) % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        """power_sum(S_n)과 degree를 하류 모듈에 전달."""
        ans = self.execute(seed)
        return {
            "power_sum": ans,
            "degree": seed["degree"],
        }

    def generate_seed_with_bridge(
        self, bridge: dict[str, Any], difficulty_hint: float = 13.0
    ) -> dict[str, Any]:
        """poly_complex_roots의 root_abs_sum을 target_power 힌트로 활용."""
        root_abs_sum = bridge.get("root_abs_sum")
        poly_degree = bridge.get("polynomial_degree")

        degree = int(poly_degree) if poly_degree is not None and 3 <= int(poly_degree) <= 5 else random.randint(3, 5)

        # root_abs_sum을 target_power 힌트로 사용 (유효 범위 내로 클램핑)
        if root_abs_sum is not None:
            tp = int(root_abs_sum) % 6 + 3  # 3~8 범위
        else:
            tp = random.randint(degree, degree + 3)

        roots = [random.randint(-5, 5) for _ in range(degree)]
        roots = list(set([r for r in roots if r != 0]))
        while len(roots) < degree:
            new_r = random.randint(-7, 7)
            if new_r not in roots and new_r != 0:
                roots.append(new_r)

        seed = {"degree": degree, "target_power": tp, "roots": roots}
        ans = self.execute(seed)
        if 0 <= ans <= 999:
            return seed
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            f"1. {seed['degree']}차 다항식의 계수를 통해 비에타의 정리(Vieta's Formulas)로 기본 대칭식 e_1, e_2, ... e_k를 구합니다.",
            f"2. 뉴턴의 공식(Newton's Sums) S_k + a_{{n-1}}S_{{k-1}} + ... + k a_{{n-k}} = 0 을 적용합니다.",
            f"3. S_1부터 순차적으로 계산하여 목표하는 S_{seed['target_power']} (근의 {seed['target_power']}제곱 합)을 도출합니다.",
            "4. 최종 정답을 000-999 범위(또는 문제 조건)에 맞춰 정제합니다."
        ]
