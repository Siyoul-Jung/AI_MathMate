"""
AI_MathMate V2 -- meta_rosetta_mapping (도메인 간 번역 전략 / Rosetta Mapping)
하나의 수학 문제를 다른 도메인(대수 <-> 기하, 조합 <-> 정수론 등)의 언어로 번역하여
학생이 도메인 전환(domain shift)이라는 비자명한 통찰을 요구받도록 합니다.
AIME 고난도 문항의 핵심: "이 문제가 사실은 X 문제다"라는 인식 자체가 도약.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class MetaRosettaMappingModule(AtomicModule):
    META = ModuleMeta(
        module_id="meta_rosetta_mapping",
        name="도메인 간 번역 전략 (Rosetta Mapping)",
        domain="integer",
        namespace="meta_rosetta",
        input_schema={
            "source_domain": FieldSpec(dtype=str, domain=["algebra", "geometry", "combinatorics", "number_theory"],
                                        description="원래 문제의 도메인"),
            "target_domain": FieldSpec(dtype=str, domain=["algebra", "geometry", "combinatorics", "number_theory"],
                                        description="번역 목표 도메인"),
            "mapping_type": FieldSpec(dtype=str, domain=["bijection", "homomorphism", "analogy"],
                                       description="매핑 유형"),
        },
        output_schema={
            "translation_hints": FieldSpec(dtype=list, domain="Steps", description="도메인 번역 힌트"),
            "domain_bridge": FieldSpec(dtype=dict, domain="str->str", description="개념 매핑 사전"),
            "daps_bonus": FieldSpec(dtype=float, domain="R+", description="도메인 전환 DAPS 보너스"),
        },
        logic_depth=5,
        daps_contribution=4.0,
        min_difficulty=12,
        category="meta",
        tags=["rosetta_mapping", "domain_shift", "bijection", "cross_domain", "insight"],
        v2_strategy_tags=["conceal", "anonymize"],
    )

    # 도메인 간 개념 매핑 테이블
    _DOMAIN_BRIDGES = {
        ("algebra", "geometry"): {
            "다항식의 근": "원과 직선의 교점",
            "판별식": "접선 조건",
            "부등식": "영역 경계",
            "이차식": "포물선/원뿔곡선",
        },
        ("algebra", "combinatorics"): {
            "다항식 전개": "이항계수",
            "급수의 합": "세기 문제",
            "인수분해": "집합의 분할",
            "행렬": "그래프 인접 행렬",
        },
        ("algebra", "number_theory"): {
            "정수해": "합동식",
            "유리수 조건": "나눗셈 정리",
            "다항식의 정수근": "인수 분해와 약수",
            "절댓값": "거리 함수",
        },
        ("geometry", "combinatorics"): {
            "격자점": "정수 쌍의 개수",
            "영역 분할": "오일러 공식 V-E+F",
            "대각선": "조합 C(n,2)",
            "볼록 껍질": "극단점 집합",
        },
        ("combinatorics", "number_theory"): {
            "순열": "나머지 연산",
            "부분집합의 합": "약수의 합",
            "이항계수": "뤼카 정리",
            "분할": "파티션 함수",
        },
        ("geometry", "number_theory"): {
            "격자점 삼각형": "픽의 정리",
            "피타고라스 삼조": "이차 디오판틴 방정식",
            "원 위의 유리점": "유리수 매개변수",
            "정다각형": "원시근",
        },
    }

    def generate_seed(self, difficulty_hint: float = 13.0) -> dict[str, Any]:
        domains = ["algebra", "geometry", "combinatorics", "number_theory"]
        mapping_types = ["bijection", "homomorphism", "analogy"]

        for _ in range(100):
            source = random.choice(domains)
            target = random.choice([d for d in domains if d != source])
            mapping_type = random.choice(mapping_types)
            seed = {
                "source_domain": source,
                "target_domain": target,
                "mapping_type": mapping_type,
            }
            # 매핑 테이블 존재 확인
            key = (source, target)
            rev_key = (target, source)
            if key in self._DOMAIN_BRIDGES or rev_key in self._DOMAIN_BRIDGES:
                return seed

        return {"source_domain": "algebra", "target_domain": "geometry", "mapping_type": "bijection"}

    def execute(self, seed: dict[str, Any]) -> int:
        """도메인 간 거리와 매핑 유형에서 결정론적 점수를 반환."""
        source = seed["source_domain"]
        target = seed["target_domain"]
        mapping_type = seed["mapping_type"]

        domain_vals = {"algebra": 11, "geometry": 23, "combinatorics": 37, "number_theory": 47}
        type_vals = {"bijection": 5, "homomorphism": 7, "analogy": 3}
        s_val = domain_vals.get(source, 1)
        t_val = domain_vals.get(target, 1)
        m_val = type_vals.get(mapping_type, 1)

        key = (source, target)
        rev_key = (target, source)
        n_bridges = len(self._DOMAIN_BRIDGES.get(key, self._DOMAIN_BRIDGES.get(rev_key, {})))

        return (s_val * t_val * m_val + n_bridges * 100) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        source = seed["source_domain"]
        target = seed["target_domain"]
        key = (source, target)
        rev_key = (target, source)
        n_bridges = len(self._DOMAIN_BRIDGES.get(key, self._DOMAIN_BRIDGES.get(rev_key, {})))
        return [
            f"1. 원래 문제를 '{source}' 도메인의 언어로 분석합니다.",
            f"2. '{source}' -> '{target}' 도메인 전환의 핵심 대응 관계를 식별합니다.",
            f"3. {n_bridges}개의 개념 쌍을 '{seed['mapping_type']}' 유형으로 매핑합니다.",
            f"4. '{target}' 도메인에서 문제를 재서술하여 새로운 풀이 경로를 개방합니다.",
        ]
