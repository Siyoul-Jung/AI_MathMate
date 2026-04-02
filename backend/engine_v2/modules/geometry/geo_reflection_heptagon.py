"""
AIME 2025 I Problem 2 - Heptagon Area with Reflection (기하 닮음과 반사 영역)
V2 이식(Porting) 완료 모듈.
"""

import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeoReflectionHeptagonModule(AtomicModule):
    """
    On triangle ABC, given ratios AD:DE:EB and AF:FG:GC.
    Find the area of heptagon AFNBCEM given area of DEGF.
    Logic: Total Area S = Area(DEGF) / [((r1+r2)/T)^2 - (r1/T)^2]
    """

    META = ModuleMeta(
        module_id="geo_reflection_heptagon",
        name="Heptagon Area Reflection",
        category="geometry",
        domain="real",
        namespace="geo.heptagon",
        logic_depth=4,
        daps_contribution=7.0,
        min_difficulty=2,
        heuristic_weight=0.1,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Area Ratio", "Similarity", "Polygon Area"],
        source_reference="AIME 2025 P02",
        input_schema={
            "r1": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=5),
            "r2": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=10),
            "r3": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=5),
            "area_part": FieldSpec(dtype=int, domain="Z+", min_val=10, max_val=500)
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="Area of the heptagon")
        }
    )

    def generate_seed(self, difficulty_hint: float = 7.0) -> Dict[str, Any]:
        """
        DAPS 난이도에 따라 비율과 넓이를 조절합니다.
        정수 정답이 나오도록 (area_part * T^2) % ((r1+r2)^2 - r1^2) == 0 인 조합을 찾습니다.
        """
        max_attempts = 200
        for _ in range(max_attempts):
            r1 = random.randint(1, 3)
            r2 = random.randint(2, 6)
            r3 = random.randint(1, 4)
            area_part = random.randint(50, 400)
            
            total_r = r1 + r2 + r3
            diff_sq = (r1 + r2)**2 - r1**2
            denom = total_r**2
            
            # 정수 결과 보장 및 AIME 범위(0~999) 체크
            if (area_part * denom) % diff_sq == 0:
                ans = (area_part * denom) // diff_sq
                if 100 <= ans <= 999:
                    return {
                        "r1": r1, "r2": r2, "r3": r3,
                        "area_part": area_part
                    }
        
        # Fallback (AIME 2025 P02 원본 데이터)
        return {"r1": 1, "r2": 4, "r3": 2, "area_part": 288}

    def execute(self, seed: Dict[str, Any]) -> int:
        r1, r2, r3, ap = seed["r1"], seed["r2"], seed["r3"], seed["area_part"]
        total_r = r1 + r2 + r3
        diff_sq = (r1 + r2)**2 - r1**2
        ans = (ap * (total_r**2)) // diff_sq
        return int(ans)

    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        r1, r2, r3, ap = seed["r1"], seed["r2"], seed["r3"], seed["area_part"]
        total_r = r1 + r2 + r3
        return [
            f"Step 1: 삼각형 ABC에서 닮음비를 이용합니다. 작은 삼각형 ADF와 중간 삼각형 AEG의 넓이 비는 길이 비의 제곱인 ({r1}/{total_r})^2 와 (({r1}+{r2})/{total_r})^2 입니다.",
            f"Step 2: 주어진 사각형 DEGF의 넓이 {ap}는 두 삼각형 AEG와 ADF의 넓이 차이임을 이용해 전체 삼각형 넓이 S를 구합니다.",
            f"Step 3: 수치 계산 결과 S = {ap} * {total_r}^2 / (({r1}+{r2})^2 - {r1}^2) 를 산출합니다.",
            f"Step 4: 기하학적 대칭성에 의해 구하고자 하는 헵타곤 AFNBCEM의 넓이가 전체 삼각형 S와 같음을 확인하고 최종 정답을 도출합니다."
        ]
