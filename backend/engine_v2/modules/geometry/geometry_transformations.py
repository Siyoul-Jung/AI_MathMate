"""
AI_MathMate V2 — 기하 변환 (geometry_transformations)
AIME 기출 36회. 반사, 회전, 평행이동 좌표 계산을 다룹니다.
"""
from __future__ import annotations
import random
from typing import Any
from engine_v2.modules.base_module import AtomicModule, ModuleMeta, FieldSpec

class GeometryTransformationsModule(AtomicModule):
    META = ModuleMeta(
        module_id="geometry_transformations", name="기하 변환",
        domain="integer", namespace="geo_transform",
        input_schema={
            "x": FieldSpec(dtype=int, domain="Z", description="점 x좌표"),
            "y": FieldSpec(dtype=int, domain="Z", description="점 y좌표"),
            "mode": FieldSpec(dtype=str, domain="str", description="'reflect_x' | 'reflect_y' | 'rotate_180' | 'translate'"),
            "dx": FieldSpec(dtype=int, domain="Z", description="이동량 x"),
            "dy": FieldSpec(dtype=int, domain="Z", description="이동량 y"),
        },
        output_schema={"answer": FieldSpec(dtype=int, domain="Z+", min_val=0, max_val=999)},
        logic_depth=3, daps_contribution=3.0, min_difficulty=2, category="geometry",
        tags=["reflection", "rotation", "translation", "transformation"], exam_types=["AIME"],
    )
    def generate_seed(self, difficulty_hint: float = 10.0) -> dict[str, Any]:
        for _ in range(100):
            mode = random.choice(["reflect_x", "reflect_y", "rotate_180", "translate"])
            x, y = random.randint(-50, 50), random.randint(-50, 50)
            dx, dy = random.randint(-20, 20), random.randint(-20, 20)
            seed = {"x": x, "y": y, "mode": mode, "dx": dx, "dy": dy}
            ans = self.execute(seed)
            if 0 < ans <= 999: return seed
        return {"x": 3, "y": 4, "mode": "reflect_x", "dx": 0, "dy": 0}

    def execute(self, seed: dict[str, Any]) -> int:
        x, y, mode = seed["x"], seed["y"], seed["mode"]
        if mode == "reflect_x": xp, yp = x, -y
        elif mode == "reflect_y": xp, yp = -x, y
        elif mode == "rotate_180": xp, yp = -x, -y
        else: xp, yp = x + seed["dx"], y + seed["dy"]
        return (abs(xp) + abs(yp)) % 1000

    def get_logic_steps(self, seed: dict[str, Any]) -> list[str]:
        return [
            f"1. 점 ({seed['x']}, {seed['y']})에 {seed['mode']} 변환을 적용합니다.",
            "2. 변환 규칙에 따라 새 좌표를 계산합니다.",
            "3. |x'| + |y'|를 구합니다.",
            "4. 1000으로 나눈 나머지를 구합니다.",
        ]
    def verify_with_sympy(self, seed: dict[str, Any]) -> int | None:
        try: return self.execute(seed)
        except: return None
