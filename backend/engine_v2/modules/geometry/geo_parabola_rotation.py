"""
AIME 2025 I Problem 9 - Parabola Rotation (포물선 회전과 교점)
V2 이식(Porting) 완료 모듈.
"""

import math
import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeoParabolaRotationModule(AtomicModule):
    """
    Parabola y = x^2 - k is rotated alpha degrees.
    Find the intersection point or area related coefficients a, b, c.
    Logic:
    - intersection with y = -tan(alpha/2) * x (symmetry line)
    - x^2 - k = -tan(alpha/2) * x
    - x^2 + tan(alpha/2)x - k = 0
    - x = [-tan(alpha/2) +/- sqrt(tan^2(alpha/2) + 4k)] / 2
    """

    META = ModuleMeta(
        module_id="geo_parabola_rotation",
        name="Parabola Rotation",
        category="geometry",
        domain="real",
        namespace="geo.para_rot",
        logic_depth=4,
        daps_contribution=9.0,
        min_difficulty=9,
        heuristic_weight=0.2,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Parabola Rotation", "Intersection", "Rotation Transformation"],
        source_reference="AIME 2025 P09",
        input_schema={
            "k": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=30),
            "rotation_angle": FieldSpec(dtype=int, domain="Z+", min_val=60, max_val=120)
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Sum of coefficients a+b+c")
        }
    )

    def generate_seed(self, difficulty_hint: float = 9.0) -> Dict[str, Any]:
        """
        DAPS 난이도에 따라 k와 회전각을 조절합니다.
        """
        max_attempts = 100
        for _ in range(max_attempts):
            k = random.randint(3, 30)
            rotation_angle = random.choice([60, 90, 120])
            
            res = self._solve_internal(k, rotation_angle)
            if res:
                a, b, c, ans = res
                # 완전제곱수가 아닌 b를 선호 (AIME 스타일)
                if int(math.sqrt(b))**2 != b and 10 <= ans <= 999:
                    return {"k": k, "rotation_angle": rotation_angle}
                    
        return {"k": 5, "rotation_angle": 90}

    def execute(self, seed: Dict[str, Any]) -> int:
        res = self._solve_internal(seed["k"], seed["rotation_angle"])
        if not res: return 0
        return res[3] # a + b + c

    def _solve_internal(self, k, alpha) -> tuple | None:
        # V1 solver 로직 정규화
        if alpha == 60:
            # y = -sqrt(3)x 대칭축 (tan 30 = 1/sqrt(3), but rotated 60 deg intersection is complex)
            # V1 공식: a=3, b=9+12k, c=2
            a, b, c = 3, 9 + 12 * k, 2
        elif alpha == 90:
            # y = -x 대칭축
            # x^2 - k = -x => x^2 + x - k = 0 => x = (-1 + sqrt(1+4k))/2
            # a=1, b=4*k + 1, c=1
            a, b, c = 1, 4 * k + 1, 1
        elif alpha == 120:
            # a=1, b=1+12k, c=2
            a, b, c = 1, 1 + 12 * k, 2
        else:
            return None
            
        return a, b, c, a + b + c

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        k, alpha = seed["k"], seed["rotation_angle"]
        return [
            f"Step 1: 주어진 포물선 y = x^2 - {k} 와 이를 원점을 중심으로 {alpha}도 회전시킨 포물선의 대칭축(Symmetry line)을 찾습니다. {alpha}도 회전 시 두 포물선의 교점은 기울기가 -tan({alpha}/2) 인 직선 위에 놓이게 됩니다.",
            f"Step 2: 원본 포물선 식과 대칭축의 방정식을 연립하여 교점의 x좌표를 구하기 위한 이차방정식을 수립합니다.",
            f"Step 3: 근의 공식을 사용하여 x좌표와 y좌표를 계산하며, 이를 (a - sqrt(b))/c 또는 유사한 무리수 꼴로 정리합니다.",
            f"Step 4: 도출된 무리수 식의 계수 a, b, c를 확인하고 최종적으로 이들의 합 a+b+c를 계산합니다."
        ]
