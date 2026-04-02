"""
AI_MathMate V2 — 대칭성 파괴 및 꼼수 방지 (meta_symmetry_breaker)
수식의 완벽한 대칭성을 의도적으로 미틀어(Asymmetry Tuning), 학생들이 단순 대입(x=y)으로 답을 찍는 'Fakesolve'를 방지합니다.
13, 17, 333 같은 비대칭 소수/반소수를 주입하여 계산적 필연성을 강화합니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class MetaSymmetryBreakerModule(AtomicModule):
    META = ModuleMeta(
        module_id="meta_symmetry_breaker",
        name="대칭성 파괴 (Symmetry Breaker)",
        domain="meta",
        namespace="meta_symmetry",
        input_schema={
            "symmetry_type": FieldSpec(dtype=str, domain=["cyclic", "symmetric", "none"], description="기존 수식의 대칭 유형"),
            "asymmetry_intensity": FieldSpec(dtype=float, domain="[0, 1]", description="비대칭성 주입 강도")
        },
        output_schema={
            "prime_force_numbers": FieldSpec(dtype=list, domain="Primes", description="주입된 비대칭 소수 리스트"),
            "coefficient_tuning": FieldSpec(dtype=dict, domain="Float", description="변수별 계수 미세 조정값"),
            "fakesolve_resistance": FieldSpec(dtype=float, domain="R+", description="꼼수 풀이 방지 지수")
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=13,
        category="meta_logic",
        tags=["anti_fakesolve", "asymmetry", "prime_force", "tuning"]
    )

    def generate_seed(self, difficulty_hint: float = 13.0) -> dict[str, Any]:
        return {
            "symmetry_type": random.choice(["cyclic", "symmetric"]),
            "asymmetry_intensity": min(1.0, (difficulty_hint - 12) / 10)
        }

    def execute(self, seed: dict[str, Any]) -> dict[str, Any]:
        # 비대칭 소수 풀(Pool)에서 선택
        asymmetric_primes = [13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 101, 103, 107, 137, 331, 337]
        intensity = seed["asymmetry_intensity"]
        
        # 강도에 따라 주입할 소수 개수 결정
        num_primes = 1 if intensity < 0.5 else 2
        selected_primes = random.sample(asymmetric_primes, num_primes)
        
        # 계수 미세 조정 (x 계수는 17, y 계수는 13 등으로 설정하여 x=y 대입을 응징)
        tuning = {
            "coeff_x": selected_primes[0],
            "coeff_y": selected_primes[1] if len(selected_primes) > 1 else selected_primes[0] + 1
        }
        
        return {
            "prime_force_numbers": selected_primes,
            "coefficient_tuning": tuning,
            "fakesolve_resistance": intensity * 5.0
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        res = self.execute(seed)
        p1 = res['prime_force_numbers'][0]
        return [
            f"1. 생성된 수식의 {seed['symmetry_type']} 대칭성을 분석하여 'fakesolve' 취약 지점을 식별합니다.",
            f"2. (Asymmetry Tuning) x의 계수에는 {p1}를, y의 계수에는 다른 값을 주입하여 대칭을 미세하게 파괴합니다.",
            "3. (Prime Force) 10, 100 같은 둥근 숫자 대신 비대칭 소수를 주입하여 정답이 우연히 단순한 정수가 되지 않게 제어합니다.",
            f"4. 최종적으로 꼼수 풀이 방지 지수를 {res['fakesolve_resistance']}로 격상시켜 AIME 13-15번급의 변별력을 확보합니다."
        ]
