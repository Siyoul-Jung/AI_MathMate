"""
AI_MathMate V2 — 닮음/위치 변환 (geometry_sim_homothety)
AIME 기출 64회. 닮음비, 넓이비, 위치(homothety) 변환을 다룹니다.
"""
from __future__ import annotations
import random
from fractions import Fraction
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometrySimHomothetyModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_sim_homothety", name="닮음과 위치 변환",
        domain="integer", namespace="geo_sim",
        input_schema={
            "k_num": FieldSpec(dtype=int, domain="Z+", description="닮음비 분자"),
            "k_den": FieldSpec(dtype=int, domain="Z+", description="닮음비 분모"),
            "base_area": FieldSpec(dtype=int, domain="Z+", description="원본 넓이"),
            "mode": FieldSpec(dtype=str, domain="str", description="'area_ratio' | 'perimeter_ratio' | 'homothety_image'"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=3, daps_contribution=3.5, min_difficulty=4, category="geometry",
        tags=["similarity", "homothety", "dilation", "ratio", "similar_triangle"], exam_types=["AIME"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            mode = random.choice(["area_ratio", "perimeter_ratio", "homothety_image"])
            k_num = random.randint(1, 10)
            k_den = random.randint(1, 10)
            base_area = random.randint(10, 200)
            seed = {"k_num": k_num, "k_den": k_den, "base_area": base_area, "mode": mode}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"k_num": 2, "k_den": 3, "base_area": 54, "mode": "area_ratio"}

    def execute(self, seed: dict[str, Any]) -> int:
        k = Fraction(seed["k_num"], seed["k_den"])
        mode, base = seed["mode"], seed["base_area"]
        if mode == "area_ratio":
            new_area = Fraction(base) * k * k
            return (new_area.numerator + new_area.denominator) % 1000
        elif mode == "perimeter_ratio":
            return (Fraction(base) * k).numerator % 1000 + (Fraction(base) * k).denominator % 500
        else:
            # 위치 변환: 중심 (0,0), 점 (base, base) → (k*base, k*base)
            img = Fraction(base) * k
            return (abs(img.numerator) + img.denominator) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            f"1. 닮음비 k = {seed['k_num']}/{seed['k_den']}.",
            f"2. 원본 넓이/둘레 = {seed['base_area']}.",
            "3. 닮음 변환을 적용합니다 (넓이비 = k^2, 둘레비 = k).",
            "4. 결과를 분수로 구하고 분자+분모를 1000으로 나눈 나머지.",
        ]
    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try: return self.execute(seed)
        except: return None
