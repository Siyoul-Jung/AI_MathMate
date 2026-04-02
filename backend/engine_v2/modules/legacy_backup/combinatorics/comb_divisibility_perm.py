"""
AIME 2025 I Problem 5 - 22-Divisibility Permutations (22의 배수 판정과 순열 카운팅)
V2 이식(Porting) 완료 모듈.
"""

import math
import random
import itertools
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class CombDivisibilityPermModule(AtomicModule):
    """
    Find the number of 8-digit integers formed by 8 distinct digits that are divisible by 22.
    Logic: Divisible by 2 (last digit even) and 11 (alternating sum).
    """

    META = ModuleMeta(
        module_id="comb_divisibility_perm",
        name="Divisibility Permutations",
        category="combinatorics",
        domain="integer",
        namespace="comb.div22",
        logic_depth=4,
        daps_contribution=7.5,
        min_difficulty=5,
        heuristic_weight=0.1,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Divisibility Rules", "Alternating Sum", "Permutations"],
        source_reference="AIME 2025 P05",
        input_schema={
            "digits": FieldSpec(dtype=str, domain="Z", description="8 distinct digits string"),
            "compare_val": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=5000)
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="|N - compare_val| mod 1000")
        }
    )

    def generate_seed(self, difficulty_hint: float = 7.5) -> Dict[str, Any]:
        """
        8자리 숫자를 랜덤하게 선택하고 적절한 비교값을 생성합니다.
        """
        max_attempts = 50
        for _ in range(max_attempts):
            digits_list = random.sample("123456789", 8)
            digits_str = "".join(sorted(digits_list))
            
            N = self._solve_internal(digits_str)
            # 너무 개수가 0이거나 작으면 재미없으므로 적절한 N 탐색
            if N > 100:
                compare_val = random.randint(max(0, N - 800), N + 800)
                ans = abs(N - compare_val)
                if 0 <= ans <= 999:
                    return {"digits": digits_str, "compare_val": compare_val}
                    
        return {"digits": "12345678", "compare_val": 2025}

    def execute(self, seed: Dict[str, Any]) -> int:
        N = self._solve_internal(seed["digits"])
        return abs(N - seed["compare_val"]) % 1000

    def _solve_internal(self, digits_str: str) -> int:
        digits = [int(d) for d in digits_str]
        total_sum = sum(digits)
        
        # 22-divisibility: divisible by 2 and 11.
        # N = d1 d2 d3 d4 d5 d6 d7 d8
        # d8 must be even.
        # (d1+d3+d5+d7) - (d2+d4+d6+d8) = 11k.
        # S1 - S2 = 11k, S1 + S2 = T => 2S2 = T - 11k.
        
        evens = [d for d in digits if d % 2 == 0]
        count_n = 0
        
        # k can usually be -1, 0, 1 for 8 digits (sum approx 36)
        feasible_k = []
        for k in [-2, -1, 0, 1, 2]:
            if (total_sum - 11 * k) % 2 == 0:
                feasible_k.append(k)
                
        for k in feasible_k:
            S2_target = (total_sum - 11 * k) // 2
            
            for d8 in evens:
                S2_rem_target = S2_target - d8
                if S2_rem_target < 0: continue
                
                remaining = [d for d in digits if d != d8]
                # 7개 중 3개를 골라 합이 S2_rem_target 인 경우의 수
                comb_count = 0
                for combo in itertools.combinations(remaining, 3):
                    if sum(combo) == S2_rem_target:
                        comb_count += 1
                
                # 배치 방법: S1(4!) * S2_rem(3!)
                count_n += comb_count * math.factorial(4) * math.factorial(3)
                
        return count_n

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        return [
            f"Step 1: 22의 배수가 되기 위한 조건을 분석합니다. 마지막 자리가 짝수여야 하며(2의 배수), 홀수 번째 자리와 짝수 번째 자리 숫자의 교대합이 11의 배수여야 합니다.",
            f"Step 2: 주어진 숫자 집합 {seed['digits']}의 전체 합을 구하고, 교대합 방정식 S1 - S2 = 11k을 만족하는 부분집합 합 S2의 후보군을 결정합니다.",
            f"Step 3: 마지막 자리(짝수)를 고정한 상태에서, 나머지 짝수 번째 자리들에 들어갈 3개의 숫자를 선택하여 목표 합 S2를 만족하는 조합의 수를 구합니다.",
            f"Step 4: 각 조합에 대해 가능한 모든 순열(4! * 3!)을 곱하여 전체 배수의 개수 N을 산출하고, 주어진 값 {seed['compare_val']}과의 차이를 계산합니다."
        ]
