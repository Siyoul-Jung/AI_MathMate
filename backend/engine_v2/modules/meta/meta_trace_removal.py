"""
AI_MathMate V2 — 흔적 지우기 워크플로우 (meta_trace_removal)
출제자의 관점에서 정답에 이르는 핵심 징검다리(Scaffolding)를 지문에서 제거하여 난이도를 비약적으로 상승시킵니다.
DAPS 14.0 이상의 킬러 문항에서 각 원자 모듈의 'scaffolding_visibility'를 False로 강제 전환합니다.
"""
from __future__ import annotations
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class MetaTraceRemovalModule(AtomicModule):
    META = ModuleMeta(
        module_id="meta_trace_removal",
        name="흔적 지우기 (Trace Removal)",
        domain="meta",
        namespace="meta_trace",
        input_schema={
            "target_module_ids": FieldSpec(dtype=list, domain="ModuleID", description="은닉을 적용할 대상 모듈 목록"),
            "removal_intensity": FieldSpec(dtype=float, domain="[0, 1]", description="은닉 강도 (DAPS 연동)")
        },
        output_schema={
            "scaffolding_override": FieldSpec(dtype=dict, domain="bool", description="대상 모듈별 visibility 강제 설정값"),
            "logic_leap_bonus": FieldSpec(dtype=float, domain="R+", description="은닉으로 인해 추가되는 논리 깊이 보너스")
        },
        logic_depth=5,
        daps_contribution=4.5,
        min_difficulty=13,
        category="meta_logic",
        tags=["trace_removal", "scaffolding", "hiding", "killer_synthesis"]
    )

    def generate_seed(self, difficulty_hint: float = 13.0) -> dict[str, Any]:
        return {
            "target_module_ids": ["geometry_circle_isogonal_symmedian", "geometry_transform_inversion"],
            "removal_intensity": min(1.0, (difficulty_hint - 10) / 10)
        }

    def execute(self, seed: dict[str, Any]) -> dict[str, Any]:
        intensity = seed["removal_intensity"]
        override = {}
        for mid in seed["target_module_ids"]:
            # 강도가 0.7(DAPS 17급) 이상이면 무조건 scaffolding_visibility = False
            override[mid] = False if intensity > 0.4 else True
            
        return {
            "scaffolding_override": override,
            "logic_leap_bonus": intensity * 2.5 # 최대 2.5 난이도 상승 효과
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            "1. (Master Diagram) 문제의 무결성을 보장하는 모든 보조점과 선분(Scaffolding)을 기호적으로 생성합니다.",
            f"2. {seed['removal_intensity']} 강도에 따라 지문에서 명시적 좌표나 힌트가 되는 보조 정리 언급을 제거합니다.",
            "3. (Symbolic Replacement) 제거된 상수를 변수나 익명의 기호로 치환하여 학생의 '직관적 도약'을 강제합니다.",
            "4. 결과적으로 문제의 텍스트 레벨 복잡도는 줄어드나, 논리적 탐색 공간(Logic Depth)은 확장됩니다."
        ]
