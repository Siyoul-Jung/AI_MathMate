"""
AIME V2 — algebra_func_periodicity (Heritage 90)
고도의 함수 주기성 및 대칭성을 다루는 원자 모듈입니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class AlgebraFuncPeriodicityModule(AtomicModule):
    META = ModuleMeta(
        module_id="algebra_func_periodicity",
        name="함수 주기성 (Advanced)",
        domain="real",
        namespace="alg_per",
        input_schema={
            "f0": FieldSpec(dtype=float, domain="R", description="초기값 f(0)"),
            "k": FieldSpec(dtype=float, domain="R+", description="상수 K"),
            "n": FieldSpec(dtype=int, domain="Z+", description="계산 타겟 N"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z", description="f(n)의 결과 (1000으로 나눈 나머지)")
        },
        logic_depth=5,
        daps_contribution=6.5,
        min_difficulty=10,
        v2_compatible=True,
        v2_strategy_tags=["conceal", "asymmetry"],
        category="algebra",
        tags=["function", "periodicity", "functional_equation"]
    )

    def generate_seed(self, difficulty_hint: float = 12.0) -> dict[str, Any]:
        # f(x+1) = (k - f(x)) / (1 + k*f(x)) 형태의 복합 주기함수
        # k=1 이면 주기 4, k=sqrt(3) 이면 주기 6 등 다양하게 설정 가능
        k_options = [1.0, 0.577, 1.732] # 1, 1/sqrt(3), sqrt(3)
        k = random.choice(k_options)
        f0 = random.uniform(0.1, 0.9)
        n = random.randint(100, 500)
        
        seed = {"f0": f0, "k": k, "n": n}
        
        # [Symmetry Breaker] 적용 예시 (정수형 변수가 있을 경우)
        # seed = self.apply_asymmetry(seed, strength=1.0)
        
        return seed

    def execute(self, seed: dict[str, Any]) -> int:
        f0, k, n = seed["f0"], seed["k"], seed["n"]
        # n 에 따른 함수값 시뮬레이션
        curr = f0
        # k=1 (tan 45) -> 주기 2 (특수 케이스)
        # 여기서는 예시로 f(x+1) = (f(x) + k) / (1 - k*f(x)) 형태 (tan 합 공식)
        # tan(a+b) 공식 활용 시 주기가 180/atan(k) 과 관련됨
        
        # 계산 편의상 tan(theta + alpha) 구조 사용
        import math
        alpha = math.atan(k)
        theta0 = math.atan(f0)
        theta_n = theta0 + n * alpha
        res = math.tan(theta_n)
        
        return int(abs(res * 100)) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        f0, k, n = seed["f0"], seed["k"], seed["n"]
        steps = [
            f"1. 주어진 함수 방정식 f(x+1) = (f(x) + {k}) / (1 - {k}*f(x)) 형태 분석",
            "2. 삼각함수의 탄젠트 합 공식 tan(A+B)와의 구조적 유사성 파악",
            f"3. f(x) = tan(theta)로 치환 시, f(x+1) = tan(theta + arctan({k})) 관계 도출",
            f"4. n단계 이동 후 f(n) = tan(arctan(f(0)) + n * arctan({k})) 계산",
            f"5. n={n} 대입 및 주기성 확인",
            f"6. 결과 정수화 및 1000으로 나눈 나머지 산출"
        ]
        
        # [Logic Concealer] 적용: 중간 단계를 뭉뚱그려 도약을 강제함
        if n > 10:
            steps = self.apply_concealment(steps)
            
        return steps
