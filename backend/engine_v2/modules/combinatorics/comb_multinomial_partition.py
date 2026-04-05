"""
AIME 2025 I Problem 3 - Multinomial Partition (조합 다항계수와 부등식 분할)
V2 이식(Porting) 완료 모듈.
"""

import math
import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class CombMultinomialPartitionModule(AtomicModule):
    """
    Find the number of ways to assign T distinct items into 3 ordered categories (C, V, S)
    such that C > V > S >= 1 and C + V + S = T.
    Result modulo 1000.
    """

    META = ModuleMeta(
        module_id="comb_multinomial_partition",
        name="Multinomial Partition",
        category="combinatorics",
        domain="integer",
        namespace="comb.multinomial",
        logic_depth=3,
        daps_contribution=6.5,
        min_difficulty=3,
        heuristic_weight=0.1,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Multinomial Coefficients", "Inequality Constraints", "Counting"],
        source_reference="AIME 2025 P03",
        input_schema={
            "T": FieldSpec(dtype=int, domain="Z+", min_val=7, max_val=45, description="Total number of items")
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Total ways modulo 1000")
        },
        bridge_output_keys=["T", "partition_count"],
        bridge_input_accepts=["n_elements", "sequence_value"],
    )

    def generate_seed(self, difficulty_hint: float = 6.5) -> Dict[str, Any]:
        """
        T가 커질수록 계산량이 많아짐 (AIME 범위 0~999 유지)
        """
        # 난이도 조절: T를 조절하여 복잡도 조절
        low = int(max(7, difficulty_hint))
        high = int(min(45, difficulty_hint * 4))
        
        # 3차원 방어: 0~999 범위 내 정수 정답이 나오는 T 탐색
        max_attempts = 50
        for _ in range(max_attempts):
            T = random.randint(low, high)
            ans = self._solve_internal(T)
            if 1 <= ans <= 999:
                return {"T": T}
                
        return {"T": 10}

    def execute(self, seed: Dict[str, Any]) -> int:
        return self._solve_internal(seed["T"])

    def _solve_internal(self, T: int) -> int:
        """
        C + V + S = T, C > V > S >= 1 탐색 및 다항계수 합산
        """
        total_count = 0
        # S >= 1, V > S => V >= 2, C > V => C >= 3. T >= 1+2+3 = 6.
        for s in range(1, T // 3 + 1):
            for v in range(s + 1, T):
                c = T - s - v
                if c > v:
                    # T! / (C!V!S!)
                    ways = math.factorial(T) // (math.factorial(c) * math.factorial(v) * math.factorial(s))
                    total_count += ways
        return total_count % 1000

    def get_bridge_output(self, seed: Dict[str, Any]) -> Dict[str, Any]:
        """T와 partition_count(execute 결과)를 하류 모듈에 전달."""
        ans = self.execute(seed)
        return {
            "T": seed["T"],
            "partition_count": ans,
        }

    def generate_seed_with_bridge(
        self, bridge: Dict[str, Any], difficulty_hint: float = 6.5
    ) -> Dict[str, Any]:
        """상위 모듈의 n_elements 또는 sequence_value를 T로 활용 (유효 범위 5-20)."""
        candidate = bridge.get("n_elements") or bridge.get("sequence_value")
        if candidate is not None:
            candidate = int(candidate)
            if 5 <= candidate <= 20:
                T = candidate
            elif candidate > 20:
                T = 20
            else:
                T = max(7, candidate)
        else:
            T = random.randint(7, 20)

        # 0-999 범위 검증
        ans = self._solve_internal(T)
        if 1 <= ans <= 999:
            return {"T": T}

        # 폴백: 유효 범위 내 탐색
        for _ in range(50):
            T = random.randint(7, 20)
            ans = self._solve_internal(T)
            if 1 <= ans <= 999:
                return {"T": T}
        return {"T": 10}

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        T = seed["T"]
        return [
            f"Step 1: 총 {T}개의 서로 다른 항목을 3개의 카테고리(C, V, S)로 분할하는 상황입니다. 조건 C > V > S >= 1 을 만족하는 모든 정수 순서쌍 (C, V, S)를 찾습니다.",
            f"Step 2: 각 순서쌍에 대해 서로 다른 {T}개를 C, V, S개로 나누는 방법의 수인 다항계수 {T}! / (C! * V! * S!) 를 계산합니다.",
            f"Step 3: 각 경우의 수를 모두 합산합니다. 분할 정수론적 제약 조건에 따라 가능한 모든 배치를 전수 조사합니다.",
            f"Step 4: 합산된 전체 경우의 수를 1000으로 나눈 나머지(modulo 1000)를 구하여 정답을 산출합니다."
        ]
