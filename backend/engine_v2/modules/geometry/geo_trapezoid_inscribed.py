"""
AIME 2025 I Problem 6 - Isosceles Trapezoid with Inscribed Circle (내접원을 갖는 등변사다리꼴)
V2 이식(Porting) 완료 모듈.
"""

import math
import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeoTrapezoidInscribedModule(AtomicModule):
    """
    An isosceles trapezoid has an inscribed circle of radius r and area A.
    Find the sum of the squares of its parallel sides (a^2 + b^2).
    Logic:
    1. h = 2r
    2. a+b = 2A/h = A/r
    3. c = (a+b)/2 (tangential property)
    4. (a-b)^2 = 4(c^2 - h^2)
    5. a^2 + b^2 = ((a+b)^2 + (a-b)^2) / 2
    """

    META = ModuleMeta(
        module_id="geo_trapezoid_inscribed",
        name="Inscribed Circle Trapezoid",
        category="geometry",
        domain="real",
        namespace="geo.trap_inscribed",
        logic_depth=4,
        daps_contribution=8.0,
        min_difficulty=6,
        heuristic_weight=0.1,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Isosceles Trapezoid", "Inscribed Circle", "Tangential Quadrilateral", "Pythagoras"],
        source_reference="AIME 2025 P06",
        input_schema={
            "radius": FieldSpec(dtype=int, domain="Z+", min_val=2, max_val=10),
            "area": FieldSpec(dtype=int, domain="Z+", min_val=20, max_val=500)
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Sum of squares of bases")
        }
    )

    def generate_seed(self, difficulty_hint: float = 8.0) -> Dict[str, Any]:
        """
        DAPS 난이도에 따라 반지름과 넓이를 조절합니다.
        조건: 넓이 A > 4r^2 (빗변 c가 높이 h보다 길어야 함)
        """
        max_attempts = 100
        for _ in range(max_attempts):
            radius = random.randint(2, 6)
            min_area = 4 * (radius**2) + 2
            area = random.randint(min_area, 300)
            
            # 정수 결과가 나오도록 필터링 (a+b = area/radius 가 정수여야 계산이 깔끔함)
            if area % radius == 0:
                ans = self._solve_internal(radius, area)
                if 100 <= ans <= 999: # AIME 정답 스펙
                    return {"radius": radius, "area": area}
                    
        return {"radius": 3, "area": 72}

    def execute(self, seed: Dict[str, Any]) -> int:
        return self._solve_internal(seed["radius"], seed["area"])

    def _solve_internal(self, radius, area) -> int:
        h = 2 * radius
        sum_ab = area / radius # (a+b) = 2A/h = 2A/2r = A/r
        c = sum_ab / 2.0
        
        # (a-b)^2 / 4 = c^2 - h^2
        half_diff_sq = c**2 - h**2
        if half_diff_sq < 0: return 0
        
        diff_ab_sq = 4 * half_diff_sq
        
        # a^2 + b^2 = ((a+b)^2 + (a-b)^2) / 2
        ans = (sum_ab**2 + diff_ab_sq) / 2
        return int(round(ans))

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        r, A = seed["radius"], seed["area"]
        h = 2 * r
        return [
            f"Step 1: 등변사다리꼴의 높이 h는 내접원의 지름과 같으므로 h = 2*{r} = {h} 입니다. 넓이 공식 A = (a+b)h/2 에 의해 두 밑변의 합 a+b = {A}/{r} = {A/r} 임을 도출합니다.",
            f"Step 2: 원에 외접하는 사각형의 성질에 따라, 마주보는 변의 합이 같습니다. 즉 a+b = 2c (c는 빗변) 이므로 빗변의 길이 c = {A/r/2} 임을 알 수 있습니다.",
            f"Step 3: 보조선을 내려 직각삼각형을 만들면 피타고라스 정리에 의해 (a-b)/2 의 제곱은 c^2 - h^2 와 같습니다. 이를 통해 (a-b)^2의 값을 구합니다.",
            f"Step 4: (a+b)^2 과 (a-b)^2 의 관계식을 활용하여 최종적으로 두 밑변의 제곱의 합 a^2 + b^2 를 산출합니다."
        ]
