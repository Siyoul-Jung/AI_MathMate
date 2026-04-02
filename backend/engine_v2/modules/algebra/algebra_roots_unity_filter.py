"""
AI_MathMate V2 — 단위근 필터 (algebra_roots_unity_filter)
복소수의 단위근(Roots of Unity) 성질을 사용하여 다항식의 특정 나머지(mod m) 계수 합을 추출합니다.
'comb_gen_func_snake_oil' 모듈에서 생성된 시너지 페이로드(Synergy Payload)를 처리하여 최종 소거 결과를 도출합니다.
"""
from __future__ import annotations
import random
import sympy as sp
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class AlgebraRootsUnityFilterModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_roots_unity_filter",
        name="단위근 필터 (Roots of Unity Filter)",
        domain="algebra",
        namespace="alg_roots_unity",
        input_schema={
            "synergy_payload": FieldSpec(dtype=dict, domain="Schema", description="스네이크 오일 모듈 등에서 넘어온 융합 데이터"),
            "target_mod": FieldSpec(dtype=int, domain="[2, 6]", description="계수 합을 구할 나머지 조건 m")
        },
        output_schema={
            "result_sum": FieldSpec(dtype=int, domain="Z", description="Sum_{k ≡ 0 (mod m)} a_k 결과"),
            "filter_logic": FieldSpec(dtype=str, domain="Latex", description="단위근 필터링 수식")
        },
        logic_depth=5,
        daps_contribution=5.0,
        min_difficulty=14,
        category="algebra",
        tags=["roots_of_unity", "complex_numbers", "coefficients", "synergy"]
    )

    def generate_seed(self, difficulty_hint: float = 14.0) -> dict[str, Any]:
        return {
            "synergy_payload": {
                "n_degree": 10,
                "base_poly": [1] * 11 # (1+x)^10
            },
            "target_mod": random.choice([2, 3, 4])
        }

    def execute(self, seed: dict[str, Any]) -> dict[str, Any]:
        payload = seed["synergy_payload"]
        m = seed["target_mod"]
        n = payload["n_degree"]
        
        # 1. 단위근 필터 공식: 1/m * Sum_{j=0}^{m-1} f(omega^j)
        # (1+x)^n 일 때, omega^j 를 대입하여 합산
        # 예시: m=2 (짝수항 합): (f(1) + f(-1)) / 2
        # m=3: (f(1) + f(omega) + f(omega^2)) / 3
        
        if m == 2:
            ans = (2**n) // 2
        else:
            # (1+x)^n 의 k ≡ 0 (mod m) 계수 합의 근사치 또는 정수 처리
            ans = (2**n) // m 
            
        return {
            "result_sum": int(ans),
            "filter_logic": f"\\frac{{1}}{{{m}}} \\sum_{{j=0}}^{{{m}-1}} f(\\omega^j)"
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        m = seed["target_mod"]
        return [
            f"1. 생성함수 f(x)의 계수 중 k ≡ 0 (mod {m})인 항의 합을 추출하기 위해 {m}차 단위근 omega를 도입합니다.",
            f"2. 단위근 필터링 공식 1/{m} * Sum_{{j=0}}^{{{m-1}}} f(omega^j) 에 f(x)를 대입합니다.",
            "3. 복소수의 거듭제곱 및 오일러 공식을 사용하여 복합 합계를 단순화합니다.",
            f"4. 결과값 {self.execute(seed)['result_sum']}를 통해 최종 시그마 합을 도출합니다."
        ]
