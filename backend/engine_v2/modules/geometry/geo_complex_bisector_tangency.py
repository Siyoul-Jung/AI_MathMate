"""
AIME 2025 I Problem 8 - Complex Geometry Bisector Tangency
V2 이식(Porting) 완료 모듈.
"""

import random
import math
from fractions import Fraction
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeoComplexBisectorTangencyModule(AtomicModule):
    """
    복소평면상에서 두 점의 수직이등분선이 원에 접할 조건(k)을 구하는 모듈.
    """
    
    META = ModuleMeta(
        module_id="geo_complex_bisector_tangency",
        name="Complex Bisector Tangency",
        category="geometry",
        domain="real",
        namespace="geo.complex_tangency",
        logic_depth=4,
        daps_contribution=8.0,
        min_difficulty=6,
        heuristic_weight=0.1,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Perpendicular Bisector", "Circle Tangency", "Complex Magnitude"],
        source_reference="AIME 2025 P08",
        input_schema={
            "c_real": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=50, description="Real part of circle center"),
            "c_imag": FieldSpec(dtype=int, domain="Z", min_val=0, max_val=50, description="Imaginary part of circle center"),
            "r": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=20, description="Radius"),
            "p1_real": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20),
            "p1_imag": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20),
            "p2_real": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20),
            "p2_imag": FieldSpec(dtype=int, domain="Z", min_val=-20, max_val=20)
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Sum of numerator and denominator of the sum of k")
        }
    )

    def generate_seed(self, difficulty_hint: float = 13.0) -> Dict[str, Any]:
        """
        DAPS 점수에 따라 난수 범위를 제어하고,
        AIME 정답 포맷 (0~999 기약분수 분모+분자)을 만족할 때까지 루프를 돕니다.
        """
        # 난이도 기반 범위 (도메인 방어: 숫자가 커질수록 Fraction 분모가 거대해질 확률 증가)
        scale = int(min(20, max(5, difficulty_hint * 2)))
        
        max_attempts = 300
        for _ in range(max_attempts):
            c_real = random.randint(10, 10 + scale)
            c_imag = random.randint(10, 10 + scale)
            r = random.randint(2, 10)
            
            p1_real, p1_imag = random.randint(0, scale), random.randint(0, scale)
            p2_real, p2_imag = random.randint(0, scale), random.randint(0, scale)
            
            if (p1_real, p1_imag) == (p2_real, p2_imag): 
                continue # 두 점이 같으면 안됨
                
            ans_val = self._solve_internal(c_real, c_imag, r, p1_real, p1_imag, p2_real, p2_imag)
            if ans_val is None:
                continue
                
            # 정답 정규화 방어
            frac_res = Fraction(ans_val).limit_denominator(100)
            if frac_res.denominator > 1: # 기약분수 형태여야 의미있음
                ans = frac_res.numerator + frac_res.denominator
                if 0 <= ans <= 999:
                    return {
                        "c_real": c_real, "c_imag": c_imag, "r": r,
                        "p1_real": p1_real, "p1_imag": p1_imag,
                        "p2_real": p2_real, "p2_imag": p2_imag
                    }
                    
        # Fallback (방어선)
        return {
            'c_real': 25, 'c_imag': 20, 'r': 5, 
            'p1_real': 4, 'p1_imag': 0, 'p2_real': 0, 'p2_imag': 3
        }

    def execute(self, seed: Dict[str, Any]) -> int:
        """순수 수학 로직 계산"""
        ans_val = self._solve_internal(
            seed["c_real"], seed["c_imag"], seed["r"],
            seed["p1_real"], seed["p1_imag"], seed["p2_real"], seed["p2_imag"]
        )
        frac_res = Fraction(ans_val).limit_denominator(100)
        return int(frac_res.numerator + frac_res.denominator)

    def _solve_internal(self, c_r, c_i, r, p1_r, p1_i, p2_r, p2_i) -> float | None:
        """내부 코어 수학 연산"""
        x_mid_offset = (p1_r + p2_r) / 2.0
        y_mid = (p1_i + p2_i) / 2.0
        dx = p2_r - p1_r
        dy = p2_i - p1_i
        
        if dx == 0: return None # 수직선일 경우 k가 해에 영향을 미치지 않음
        m_s = dy / dx

        if dy == 0: # 수평선
            k1 = c_r - x_mid_offset - r
            k2 = c_r - x_mid_offset + r
            return k1 + k2

        m = -1.0 / m_s
        const_part = m * (c_r - x_mid_offset) - c_i + y_mid
        rhs = r * math.sqrt(m**2 + 1)
        k1 = (const_part - rhs) / m
        k2 = (const_part + rhs) / m
        return k1 + k2

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        return [
            "Step 1: 두 점 p1+k와 p2+k로부터 같은 거리에 있는 복소수 z의 궤적은 수직이등분선입니다. k값 이동에 따른 수직이등분선의 방정식을 k를 포함한 직선의 방정식으로 나타냅니다.",
            "Step 2: 수직이등분선이 주어진 중심 c와 반지름 r을 갖는 원에 접해야 하므로, 원의 중심에서 직선까지의 거리가 r과 같다는 점과 직선 사이의 거리 공식을 세웁니다.",
            "Step 3: 도출된 거리 공식을 풀면 k에 대한 2차 방정식 또는 형태가 도출되며, 직선이 원에 양쪽으로 접하는 두 가지 경우(두 개의 k값)가 만들어집니다.",
            "Step 4: 가능한 모든 k값의 합을 구합니다. 이를 기약분수 m/n 형태로 나타낸 뒤, 문제의 요구사항에 따라 m+n을 구합니다."
        ]
