"""
AIME 2025 I Problem 12 - Geometrical Region of Cyclic Inequalities on a Plane
V2 이식(Porting) 완료 모듈.
"""

import random
from typing import Dict, Any, List
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class AlgebraCyclicIneqPlaneModule(AtomicModule):
    """
    평면 x + y + z = N 상의 순환 부등식 영역 넓이 계산 모듈.
    """
    
    # 1. 메타데이터(META) 규격화
    META = ModuleMeta(
        module_id="alg_cyclic_ineq_plane",
        name="Cyclic Inequalities on a Plane",
        category="algebra",
        domain="integer",
        namespace="algebra.cyclic_ineq",
        logic_depth=4,
        daps_contribution=12.0,
        min_difficulty=8,
        heuristic_weight=0.2,
        exam_types=["AIME"],
        languages=["en", "ko"],
        tags=["Cyclic Inequalities", "Plane Geometry", "Symmetric Regions"],
        source_reference="AIME 2025 P12",
        input_schema={
            "N": FieldSpec(dtype=int, domain="Z+", min_val=15, max_val=105, description="Sum of coordinates (N+3 must be multiple of 6)"),
            "expected_k": FieldSpec(dtype=int, domain="Z+", min_val=3, max_val=18, description="Scaling factor k")
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="a+b value")
        }
    )

    # 2. generate_seed() 함수 분리 및 2차원 방어선 구축 (Invariants & Constraints)
    def generate_seed(self, difficulty_hint: float = 13.0) -> Dict[str, Any]:
        """
        수학적 불변성을 만족시키는 N을 뽑습니다.
        N must be 6k-3 to make (N+3)^2 divisible by 12.
        답 = 3k^2 + 3 이므로 답이 0~999를 만족하도록 k 범위를 제한합니다.
        (max k = 18 -> 3(324)+3=975)
        """
        # 난이도별 k의 범위 조정 (3차원 방어: OOM 및 범위 이탈 방지)
        if difficulty_hint < 6.0:
            ks = list(range(3, 8))   # 쉬운 구간
        elif difficulty_hint < 11.0:
            ks = list(range(8, 13))  # 중간 구간
        else:
            ks = list(range(13, 19)) # 고난도 구간 (Master)

        # 2차원 도메인 제약조건 검증 루프 (While loop)
        max_attempts = 100
        for _ in range(max_attempts):
            k = random.choice(ks)
            N = 6 * k - 3
            
            # 예상 정답 = 3*k^2 + 3
            # AIME 0~999 규격 준수 검사
            ans = 3 * (k**2) + 3
            if 100 <= ans <= 999: # AIME 정답 스펙 통과 시
                return {"N": N, "expected_k": k}
                
        # 방어선: 최악의 경우(Fallback)
        return {"N": 75, "expected_k": 13}

    # 3. 순수 계산 로직 execute() 독립 (3차원 출력 보장)
    def execute(self, seed: Dict[str, Any]) -> int:
        """
        Seed 값 N을 받아 정확히 순수 파이썬 계산만 수행합니다. (지문 텍스트 없음)
        """
        N = seed["N"]
        # 도메인 로직: N+3 = 6k. k = (N+3)//6
        k = (N + 3) // 6
        a = 3 * (k**2)  # (N+3)^2 / 12 = 36k^2 / 12 = 3k^2
        b = 3
        return a + b

    # 4. 단계별 해설 get_logic_steps() 해체
    def get_logic_steps(self, seed: Dict[str, Any]) -> List[str]:
        N = seed["N"]
        return [
            f"Step 1 (경계면 분석): 주어진 부등식 x-yz < y-zx < z-xy의 경계를 조사합니다. x-yz = y-zx를 풀면 x=y 또는 z=-1의 경계 평면을 얻습니다.",
            f"Step 2 (정삼각형 영역): 평면 x+y+z={N}과 x,y,z=-1로 둘러싸인 정삼각형 영역을 파악합니다. 이 영역의 한 변의 길이는 ({N}+3)√2 입니다.",
            f"Step 3 (대칭 넓이 추출): 전체 삼각형 영역의 넓이는 √3/4 * ( ({N}+3)√2 )^2 = ({N}+3)^2 * √3 / 2 입니다. 해를 구하는 영역은 이 전체 넓이의 정확히 1/6에 해당하는 대칭 영역입니다.",
            f"Step 4 (값 계산): 따라서 유한 영역의 넓이는 ({N}+3)^2 * √3 / 12 입니다. N={N}을 대입하면 이 넓이는 a√b 형태로 정리되며, a+b를 구합니다."
        ]
