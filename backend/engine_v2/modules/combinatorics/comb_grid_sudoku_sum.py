"""
AIME 2025 I Problem 10 - Grid Sudoku Prime Sum (격자 채우기와 소인수분해 지수 합)
V2 이식(Porting) 완료 모듈.
"""

import math
import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class CombGridSudokuSumModule(AtomicModule):
    """
    3x(3K) 격자 채우기 경우의 수를 구하고, 그 소인수분해 결과 p*e의 합을 구하는 모듈.
    공식: N = (3K)! * S_K * (K!)^6 (S_K는 Franel Number)
    """

    META = ModuleMeta(
        module_id="comb_grid_sudoku_sum",
        name="Grid Sudoku Sum",
        category="combinatorics",
        domain="integer",
        namespace="comb.grid_sudoku",
        logic_depth=4,
        daps_contribution=10.0,
        min_difficulty=8,
        heuristic_weight=0.3,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Grid Permutations", "Sudoku Counting", "Franel Numbers", "Prime Factorization"],
        source_reference="AIME 2025 P10",
        input_schema={
            "K": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=4)
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Sum of p * e for total count N")
        }
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> Dict[str, Any]:
        """
        K 값에 따라 경우의 수가 기하급수적으로 늘어나므로 1~4 범위 내에서 선택합니다.
        """
        # K=4 이상은 숫자가 너무 커서 소인수분해 계산에 병목이 올 수 있으므로 주의
        K_options = [1, 2, 3]
        if difficulty_hint > 11.0: K_options.append(4)
        
        K = random.choice(K_options)
        return {"K": K}

    def execute(self, seed: Dict[str, Any]) -> int:
        K = seed["K"]
        
        # 1. Franel Number S_K = sum(C(K, k)^3)
        s_k = 0
        for k in range(K + 1):
            s_k += math.comb(K, k) ** 3
            
        # 2. Total Ways N = (3K)! * S_K * (K!)^6
        # 직접 큰 수를 곱하지 않고 소인수별 지수를 합쳐서 계산 (성능 최적화)
        prime_exponents = {}
        
        def add_factors(n, multiplier=1):
            if n <= 1: return
            temp = n
            d = 2
            while d * d <= temp:
                while temp % d == 0:
                    prime_exponents[d] = prime_exponents.get(d, 0) + multiplier
                    temp //= d
                d += 1
            if temp > 1:
                prime_exponents[temp] = prime_exponents.get(temp, 0) + multiplier

        def add_factorial_factors(n, multiplier=1):
            for i in range(2, n + 1):
                add_factors(i, multiplier)

        # (3K)!
        add_factorial_factors(3 * K, 1)
        # S_K
        add_factors(s_k, 1)
        # (K!)^6
        add_factorial_factors(K, 6)
        
        # 3. Sum p * e
        result_sum = 0
        for p, e in prime_exponents.items():
            result_sum += p * e
            
        return result_sum % 1000

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        K = seed["K"]
        return [
            f"Step 1: 3 x {3*K} 격자의 제약 조건(각 행과 3x{K} 블록 내 중복 금지)을 만족하는 경우의 수를 조합론적으로 분석합니다.",
            f"Step 2: 전체 경우의 수 N이 (3K)! * S_K * (K!)^6 꼴임을 유도합니다. 여기서 S_K는 3제곱 조합의 합인 프라넬 수(Franel Number)입니다.",
            f"Step 3: 도출된 N을 소인수분해하여 N = p1^e1 * p2^e2 * ... 꼴로 나타냅니다. (K={K} 에 대한 계산 수행)",
            f"Step 4: 각 소수(p)와 그 지수(e)의 곱의 총합인 sum(p * e)를 계산하여 최종 정답을 도출합니다."
        ]
