"""
AIME 2025 I Problem 1 - Base Divisibility (진법 나눗셈과 약수 조건)
V2 이식(Porting) 완료 모듈.
"""

import math
import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class NTBaseDivisibilityModule(AtomicModule):
    """
    Find the sum of all integer bases b such that (1Y)_b divides (XW)_b.
    Condition: (b + Y) divides (Xb + W)
    Equivalent to: (b + Y) divides (W - XY)
    """

    META = ModuleMeta(
        module_id="nt_base_divisibility",
        name="Base Divisibility",
        category="number_theory",
        domain="integer",
        namespace="nt.base_div",
        logic_depth=4,
        daps_contribution=6.0,
        min_difficulty=1,
        heuristic_weight=0.1,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Base Conversion", "Divisibility", "Polynomial Division"],
        source_reference="AIME 2025 P01",
        input_schema={
            "X": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=15),
            "Y": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=15),
            "W": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=15)
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Sum of valid bases b")
        }
    )

    def generate_seed(self, difficulty_hint: float = 6.0) -> Dict[str, Any]:
        """
        DAPS 난이도에 따라 X, Y, W 범위를 조절합니다.
        |W - XY| 가 클수록 약수가 많아질 확률이 높습니다.
        """
        scale = int(min(15, max(5, difficulty_hint * 1.5)))
        
        max_attempts = 100
        for _ in range(max_attempts):
            X = random.randint(2, scale)
            Y = random.randint(1, scale)
            W = random.randint(1, scale)
            
            # 2차원 방어: |W - XY| 가 너무 작으면 해가 없을 수 있음
            remainder_const = abs(W - X * Y)
            if remainder_const < 20:
                continue
                
            ans = self._solve_internal(X, Y, W)
            # 3차원 방어: AIME 정답 범위 (0~999) 및 해가 최소 2개 이상인 경우 선호
            if 10 <= ans <= 999:
                return {"X": X, "Y": Y, "W": W}
                
        # Fallback (AIME 2025 P01 원본 근사치)
        return {"X": 9, "Y": 7, "W": 7}

    def execute(self, seed: Dict[str, Any]) -> int:
        return self._solve_internal(seed["X"], seed["Y"], seed["W"])

    def _solve_internal(self, X, Y, W) -> int:
        """
        b + Y | Xb + W  => b + Y | X(b + Y) + (W - XY)
        => b + Y | W - XY
        """
        R = abs(W - X * Y)
        if R == 0: return 0 # 무한히 많은 해 방지
        
        factors = self._get_factors(R)
        min_b = max(X, Y, W, 1) # 진법 제약 b > max_digit
        
        valid_bases = [ (f - Y) for f in factors if (f - Y) > min_b ]
        return sum(valid_bases)

    def _get_factors(self, n: int) -> List[int]:
        f = set()
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                f.add(i)
                f.add(n // i)
        return sorted(list(f))

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        X, Y, W = seed["X"], seed["Y"], seed["W"]
        R = abs(W - X * Y)
        return [
            f"Step 1: 주어진 진법 수 (1{Y})_b 와 ({X}{W})_b 를 10진법 수식으로 변환합니다. 각각 b+{Y} 와 {X}b+{W} 가 됩니다.",
            f"Step 2: 나눗셈 조건을 수식화합니다. {X}b + {W} = {X}(b + {Y}) + ({W} - {X}*{Y}) 이므로, b + {Y} 는 |{W} - {X*Y}| = {R} 의 약수여야 합니다.",
            f"Step 3: {R}의 약수들 중에서 진법 제약 조건 b > max({X}, {Y}, {W}) 를 만족하는 b 값을 모두 찾습니다.",
            f"Step 4: 모든 조건을 만족하는 b 값들을 합산하여 최종 결과를 산출합니다."
        ]
