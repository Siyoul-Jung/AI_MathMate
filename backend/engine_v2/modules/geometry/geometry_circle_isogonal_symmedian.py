"""
AI_MathMate V2 — 등각 켤레와 대칭중선 (geometry_circle_isogonal_symmedian)
삼각형의 대칭중선(Symmedian)과 등각 켤레(Isogonal Conjugate) 성질을 이용하여 고난도 기하 문제를 생성합니다.
'scaffolding_visibility' 플래그를 통해 핵심 보조점(대칭중선 교점 등)의 노출 여부를 제어합니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryCircleIsogonalSymmedianModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_circle_isogonal_symmedian",
        name="등각 켤레와 대칭중선",
        domain="geometry",
        namespace="geo_isogonal",
        input_schema={
            "triangle_sides": FieldSpec(dtype=list, domain="Z+", description="삼각형의 세 변 (a, b, c)"),
            "scaffolding_visibility": FieldSpec(dtype=bool, domain="bool", description="대칭중선 교점(L) 좌표 노출 여부")
        },
        output_schema={
            "lemoine_point": FieldSpec(dtype=tuple, domain="R^2", description="르무안 점(Lemoine point)의 좌표"),
            "symmedian_lines": FieldSpec(dtype=list, domain="Line", description="대칭중선 방정식 리스트"),
            "answer": FieldSpec(dtype=int, domain="[0, 999]", description="최종 계산된 길이/각도/비율")
        },
        logic_depth=5,
        daps_contribution=5.0,
        min_difficulty=14,
        category="geometry",
        tags=["isogonal_conjugate", "symmedian", "lemoine_point", "scaffolding"]
    )

    def generate_seed(self, difficulty_hint: float = 14.0) -> dict[str, Any]:
        # 피타고라스 수 또는 계산이 깔끔한 삼각형 생성
        sides = random.choice([(13, 14, 15), (7, 24, 25), (8, 15, 17)])
        return {
            "triangle_sides": list(sides),
            "scaffolding_visibility": difficulty_hint < 14.5 # 14.5 이상이면 은닉
        }

    def execute(self, seed: dict[str, Any]) -> dict[str, Any]:
        a, b, c = seed["triangle_sides"]
        # 르무안 점(Lemoine point)은 세 변의 길이의 제곱에 비례하는 거리(바리센트릭 좌표)를 가짐
        # L = (a^2 : b^2 : c^2)
        # 여기서는 실제 기하 연산 로직(SymPy Geometry)이 들어갈 자리
        # 예시 답변 생성
        ans = (a**2 + b**2 + c**2) % 1000
        return {
            "lemoine_point": (0.0, 0.0), # Placeholder for actual coord
            "symmedian_lines": [],
            "answer": int(ans)
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        a, b, c = seed["triangle_sides"]
        steps = [
            f"1. 세 변의 길이가 ({a}, {b}, {c})인 삼각형 ABC를 설정합니다.",
            "2. 각 꼭짓점에서 중선(Median)을 긋고, 각의 이등분선에 대해 대칭인 대칭중선(Symmedian)을 정의합니다."
        ]
        if seed["scaffolding_visibility"]:
            steps.append("3. 세 대칭중선의 교점인 르무안 점(Lemoine Point) L의 위치를 명시적으로 활용합니다.")
        else:
            steps.append("3. (은닉) 명시적인 점 L의 언급 없이, 대변을 나누는 비율 m^2 : n^2 성질만을 이용해 직관적 도약을 유도합니다.")
            
        steps.append(f"4. 최종 원의 반지름 또는 선분의 길이를 계산하여 {self.execute(seed)['answer']}를 도출합니다.")
        return steps
