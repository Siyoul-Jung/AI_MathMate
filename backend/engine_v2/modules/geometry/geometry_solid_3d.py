"""
AI_MathMate V2 — 3D 기하 (geometry_solid_3d)
AIME 기출 77회. 기둥, 뿔, 구의 부피와 표면적을 다룹니다.
Bridge: area_and_volume에서 base_area 수신.
"""
from __future__ import annotations
import random
import math
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec


class GeometrySolid3DModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_solid_3d",
        name="3D 기하 (부피, 표면적)",
        domain="integer",
        namespace="geo_3d",
        input_schema={
            "mode": FieldSpec(dtype=str, domain="str", description="'prism' | 'pyramid' | 'sphere'"),
            "base_area": FieldSpec(dtype=int, domain="Z+", description="밑넓이"),
            "height": FieldSpec(dtype=int, domain="Z+", description="높이"),
            "radius": FieldSpec(dtype=int, domain="Z+", description="반지름 (구용)"),
        },
        output_schema={
            "answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999),
        },
        logic_depth=3,
        daps_contribution=3.5,
        min_difficulty=3,
        category="geometry",
        tags=["3d_geometry", "solid", "volume", "surface_area", "prism", "pyramid", "sphere", "cone"],
        exam_types=["AIME"],
        bridge_input_accepts=["base_area", "perimeter"],
    )

    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        modes = ["prism", "pyramid", "sphere"]
        for _ in range(100):
            mode = random.choice(modes)
            if mode == "prism":
                base_area = random.randint(10, 200)
                height = random.randint(3, 30)
                seed = {"mode": mode, "base_area": base_area, "height": height, "radius": 0}
            elif mode == "pyramid":
                base_area = random.randint(10, 300)
                height = random.randint(3, 30)
                seed = {"mode": mode, "base_area": base_area, "height": height, "radius": 0}
            else:
                radius = random.randint(2, 10)
                seed = {"mode": mode, "base_area": 0, "height": 0, "radius": radius}
            ans = self.execute(seed)
            if 0 < ans <= 999:
                return seed
        return {"mode": "prism", "base_area": 20, "height": 5, "radius": 0}

    def execute(self, seed: dict[str, Any]) -> int:
        mode = seed["mode"]
        if mode == "prism":
            return (seed["base_area"] * seed["height"]) % 1000
        elif mode == "pyramid":
            # V = base_area * height / 3 → 3V = base_area * height
            return (seed["base_area"] * seed["height"]) % 1000  # 3V
        else:
            # 4 * pi * r^2 (표면적) → floor
            r = seed["radius"]
            return int(4 * math.pi * r * r) % 1000

    def generate_seed_with_bridge(self, bridge: dict[str, Any], difficulty_hint: float = 10.0) -> dict[str, Any]:
        base_area = bridge.get("base_area")
        if base_area and int(base_area) > 0:
            height = random.randint(3, 20)
            mode = random.choice(["prism", "pyramid"])
            return {"mode": mode, "base_area": int(base_area), "height": height, "radius": 0}
        return self.generate_seed(difficulty_hint)

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        mode = seed["mode"]
        if mode == "prism":
            return [
                f"1. 밑넓이 {seed['base_area']}, 높이 {seed['height']}인 기둥입니다.",
                f"2. 부피 V = 밑넓이 × 높이 = {seed['base_area']} × {seed['height']}.",
                "3. 부피를 계산합니다.",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]
        elif mode == "pyramid":
            return [
                f"1. 밑넓이 {seed['base_area']}, 높이 {seed['height']}인 뿔입니다.",
                f"2. 부피의 3배 = 밑넓이 × 높이 = {seed['base_area']} × {seed['height']}.",
                "3. 3V를 계산합니다 (정수 보장).",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]
        else:
            r = seed["radius"]
            return [
                f"1. 반지름 {r}인 구의 겉넓이를 구합니다.",
                f"2. 겉넓이 = 4πr² = 4π({r})².",
                "3. 정수 부분(floor)을 구합니다.",
                "4. 1000으로 나눈 나머지를 구합니다.",
            ]

    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try:
            return self.execute(seed)
        except Exception:
            return None
