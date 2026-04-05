"""
AI_MathMate V2 — 프톨레마이오스 정리 (geometry_circle_ptolemy)
원에 내접하는 사각형에서 AC * BD = AB * CD + AD * BC 를 활용하여
알려진 5개 변/대각선으로부터 나머지 대각선 길이를 구합니다.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometryCirclePtolemyModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_circle_ptolemy",
        name="프톨레마이오스 정리",
        domain="integer",
        namespace="geom_ptolemy",
        input_schema={
            "AB": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=100, description="변 AB 길이"),
            "BC": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=100, description="변 BC 길이"),
            "CD": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=100, description="변 CD 길이"),
            "DA": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=100, description="변 DA 길이"),
            "AC": FieldSpec(dtype=int, domain="Z+", min_val=1, max_val=200, description="대각선 AC 길이"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999, description="대각선 BD 길이 mod 1000"),
        },
        logic_depth=4,
        daps_contribution=4.0,
        min_difficulty=7,
        category="geometry",
        tags=["ptolemy", "cyclic_quadrilateral", "diagonal", "inscribed"],
        exam_types=["AIME"],
        bridge_output_keys=["diagonal_length", "product_sum"],
    )

    def generate_seed(self, difficulty_hint: float = 9.0) -> dict[str, Any]:
        for _ in range(100):
            # BD = (AB * CD + AD * BC) / AC 가 양의 정수가 되도록 구성
            AB = random.randint(2, 50)
            CD = random.randint(2, 50)
            AD = random.randint(2, 50)
            BC = random.randint(2, 50)

            numerator = AB * CD + AD * BC  # = AC * BD

            # AC를 numerator의 약수 중에서 선택 (BD가 정수가 되도록)
            divisors = [d for d in range(2, min(numerator, 201)) if numerator % d == 0]
            if not divisors:
                continue

            AC = random.choice(divisors)
            BD = numerator // AC

            seed = {"AB": AB, "BC": BC, "CD": CD, "DA": AD, "AC": AC}
            ans = self.execute(seed)
            if 0 <= ans <= 999 and ans > 0:
                return seed

        return {"AB": 5, "BC": 7, "CD": 3, "DA": 4, "AC": 1}

    def execute(self, seed: dict[str, Any]) -> int:
        AB = seed["AB"]
        BC = seed["BC"]
        CD = seed["CD"]
        DA = seed["DA"]
        AC = seed["AC"]

        # Ptolemy: AC * BD = AB * CD + AD * BC
        # BD = (AB * CD + AD * BC) / AC
        numerator = AB * CD + DA * BC
        if AC == 0 or numerator % AC != 0:
            return 0
        BD = numerator // AC
        return BD % 1000

    def get_bridge_output(self, seed: dict[str, Any]) -> dict[str, Any]:
        BD = self.execute(seed)
        AB, CD, DA, BC = seed["AB"], seed["CD"], seed["DA"], seed["BC"]
        return {
            "diagonal_length": BD,
            "product_sum": AB * CD + DA * BC,
        }

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        AB = seed["AB"]
        BC = seed["BC"]
        CD = seed["CD"]
        DA = seed["DA"]
        AC = seed["AC"]
        numerator = AB * CD + DA * BC
        BD = numerator // AC

        return [
            f"1. 원에 내접하는 사각형 ABCD에서 AB={AB}, BC={BC}, CD={CD}, DA={DA}, AC={AC}가 주어집니다.",
            f"2. 프톨레마이오스 정리를 적용합니다: AC * BD = AB * CD + AD * BC.",
            f"3. 우변을 계산합니다: {AB} * {CD} + {DA} * {BC} = {numerator}.",
            f"4. BD = {numerator} / {AC} = {BD}를 구합니다.",
            f"5. 결과 {BD}를 1000으로 나눈 나머지를 취합니다.",
        ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            from sympy import Integer
            AB = Integer(seed["AB"])
            BC = Integer(seed["BC"])
            CD = Integer(seed["CD"])
            DA = Integer(seed["DA"])
            AC = Integer(seed["AC"])

            numerator = AB * CD + DA * BC
            assert numerator % AC == 0, "프톨레마이오스 정리 정수 조건 불충족"
            BD = numerator // AC

            # 역검증: AC * BD == AB * CD + AD * BC
            assert AC * BD == AB * CD + DA * BC, "프톨레마이오스 등식 검증 실패"
            return int(BD % 1000)
        except Exception:
            return None
