"""
AI_MathMate V2 — 반전 기하 (geometry_transform_inversion)
원을 직선으로, 직선을 원으로 변환하는 반전(Inversion) 기하학을 사용하여 고난도 기하 문제를 생성합니다.
'scaffolding_visibility' 플래그를 통해 반전의 중심(Inverse Center)과 반지름의 노출 여부를 제어합니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryTransformInversionModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_transform_inversion",
        name="반전 기하 (Inverse Geometry)",
        domain="integer",
        namespace="geo_inversion",
        input_schema={
            "circle_radius": FieldSpec(dtype=float, domain="R+", description="반전 원의 반지름 R"),
            "scaffolding_visibility": FieldSpec(dtype=bool, domain="bool", description="반전 중심 O의 위치 노출 여부")
        },
        output_schema={
            "inverse_point": FieldSpec(dtype=tuple, domain="R^2", description="반전된 점 P'의 좌표"),
            "transformed_shape": FieldSpec(dtype=str, domain=["circle", "line"], description="변환된 도형의 종류"),
            "answer": FieldSpec(dtype=int, domain="[0, 999]", description="최종 계산된 길이/각도")
        },
        logic_depth=5,
        daps_contribution=5.0,
        min_difficulty=14,
        category="geometry",
        tags=["inversion", "circle", "line", "scaffolding"]
    )

    def generate_seed(self, difficulty_hint: float = 14.0) -> dict[str, Any]:
        return {
            "circle_radius": float(random.randint(5, 15)),
            "scaffolding_visibility": difficulty_hint < 14.5
        }

    def execute(self, seed: dict[str, Any]) -> int:
        R = seed["circle_radius"]
        # OP * OP' = R^2 → R^2 mod 1000
        return int(R ** 2) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        R = seed["circle_radius"]
        steps = [
            f"1. 중심 O, 반지름 R={R} 인 반전 원(Circle of Inversion)을 설정합니다.",
            "2. 주어진 각 도형(원 또는 직선)의 위치 관계를 분석합니다."
        ]
        if seed["scaffolding_visibility"]:
            steps.append("3. 반전 중심 O를 기준으로 각 점을 P' = (R^2 / OP^2) * P 로 매핑하여 단순화된 문제로 변환합니다.")
        else:
            steps.append("3. (은닉) 지문에서 반전의 중심과 반지름을 명시하지 않고, 도형 사이의 거리 관계만을 주어 반전 기하 사용 여부를 스스로 판단하게 합니다.")
            
        steps.append(f"4. 변환된 평면에서 기하적 계산을 수행하여 R^2 mod 1000 = {self.execute(seed)}를 도출합니다.")
        return steps
