"""
AIME 2025 I Problem 4 - Quadratic Lattice Union (이차식 격자점 합집합)
V2 이식(Porting) 완료 모듈.
"""

import math
import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class AlgebraQuadraticLatticeModule(AtomicModule):
    """
    Find the number of lattice points (x, y) with -L <= x, y <= L
    satisfying Ax^2 + Bxy + Cy^2 = 0.
    Logic: Factors into two lines and counts unique lattice points.
    """

    META = ModuleMeta(
        module_id="algebra_quadratic_lattice",
        name="Quadratic Lattice Union",
        category="algebra",
        domain="integer",
        namespace="alg.lattice",
        logic_depth=4,
        daps_contribution=6.0,
        min_difficulty=4,
        heuristic_weight=0.1,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Quadratic Factorization", "Lattice Points", "Coordinate Geometry"],
        source_reference="AIME 2025 P04",
        input_schema={
            "A": FieldSpec(dtype=int, domain="Z", min_val=-100, max_val=100),
            "B": FieldSpec(dtype=int, domain="Z", min_val=-200, max_val=200),
            "C": FieldSpec(dtype=int, domain="Z", min_val=-100, max_val=100),
            "L": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=200),
            "a1": FieldSpec(dtype=int, domain="Z"),
            "b1": FieldSpec(dtype=int, domain="Z"),
            "a2": FieldSpec(dtype=int, domain="Z"),
            "b2": FieldSpec(dtype=int, domain="Z")
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Total lattice points count")
        }
    )

    def generate_seed(self, difficulty_hint: float = 6.0) -> Dict[str, Any]:
        """
        인수분해 가능한 정수 계수 조합을 먼저 생성한 뒤 A, B, C를 도출합니다.
        """
        max_attempts = 100
        for _ in range(max_attempts):
            # 두 직선 a1x + b1y = 0 과 a2x + b2y = 0 생성
            a1, b1 = self._get_rand_coeff(), self._get_rand_coeff()
            a2, b2 = self._get_rand_coeff(), self._get_rand_coeff()
            
            # 기약 분수 형태로 정규화
            g1, g2 = math.gcd(a1, b1), math.gcd(a2, b2)
            a1, b1, a2, b2 = a1//g1, b1//g1, a2//g2, b2//g2
            
            # 두 직선이 겹치지 않도록 방어
            if (a1, b1) == (a2, b2) or (a1, b1) == (-a2, -b2):
                continue
                
            A, B, C = a1*a2, a1*b2 + a2*b1, b1*b2
            L = random.randint(50, 150)
            
            ans = self._solve_internal(a1, b1, a2, b2, L)
            if 10 <= ans <= 999:
                return {
                    "A": A, "B": B, "C": C, "L": L,
                    "a1": a1, "b1": b1, "a2": a2, "b2": b2
                }
                
        # Fallback (AIME 2025 P04 원본)
        return {"A": 12, "B": -1, "C": -6, "L": 100, "a1": 3, "b1": 2, "a2": 4, "b2": -3}

    def execute(self, seed: Dict[str, Any]) -> int:
        return self._solve_internal(seed["a1"], seed["b1"], seed["a2"], seed["b2"], seed["L"])

    def _solve_internal(self, a1, b1, a2, b2, L) -> int:
        c1 = self._count_on_line(a1, b1, L)
        c2 = self._count_on_line(a2, b2, L)
        return c1 + c2 - 1 # 원점 중복 차감

    def _count_on_line(self, a, b, L) -> int:
        # a'x + b'y = 0 => (x, y) = (kb', -ka')
        # |kb'| <= L, |ka'| <= L => |k| <= min(L/|b'|, L/|a'|)
        if a == 0 and b == 0: return 0 # 예외
        g = math.gcd(a, b)
        ar, br = abs(a // g), abs(b // g)
        
        limit_k = float('inf')
        if br != 0: limit_k = min(limit_k, L // br)
        if ar != 0: limit_k = min(limit_k, L // ar)
        
        return int(2 * limit_k + 1)

    def _get_rand_coeff(self) -> int:
        c = random.randint(-8, 8)
        return c if c != 0 else 1

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        A, B, C, L = seed["A"], seed["B"], seed["C"], seed["L"]
        a1, b1, a2, b2 = seed["a1"], seed["b1"], seed["a2"], seed["b2"]
        return [
            f"Step 1: 이차 방정식 {A}x^2 + {B}xy + {C}y^2 = 0 을 인수분해합니다. 이는 두 직선 ({a1}x + {b1}y)({a2}x + {b2}y) = 0 의 합집합을 의미합니다.",
            f"Step 2: 첫 번째 직선 {a1}x + {b1}y = 0 위에 있으며 영역 -{L} <= x, y <= {L} 내에 존재하는 격자점의 개수를 계산합니다.",
            f"Step 3: 두 번째 직선 {a2}x + {b2}y = 0 위에 있으며 동일 영역 내에 존재하는 격자점의 개수를 계산합니다.",
            f"Step 4: 두 직선의 격자점 수의 합에서 두 직선이 만나는 유일한 점인 원점 (0,0)의 중복을 1회 차감하여 합집합의 전체 격자점 수를 도출합니다."
        ]
