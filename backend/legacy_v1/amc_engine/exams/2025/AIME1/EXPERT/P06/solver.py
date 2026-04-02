import random
import numpy as np
import matplotlib.pyplot as plt
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "GEO-TRAPEZOID-INSCRIBED",
        "categories": ["Geometry"],
        "topics": ["Isosceles Trapezoid", "Inscribed Circle", "Tangential Quadrilateral", "Pythagoras"],
        "context_type": "abstract",
        "level": 6,
        "has_image": True,
        "is_mock_ready": True,
        "seed_constraints": {
            "radius": {"min_val": 2, "max_val": 6, "type": "int", "description": "Radius of inscribed circle"},
            "area": {"min_val": 20, "max_val": 300, "type": "int", "description": "Area of trapezoid (must be > 4r^2)"}
        },
        "logic_steps": [
            {"step": 1, "title": "밑변의 합 도출", "description": "넓이 A와 높이 h=2r 관계식을 통해 윗변과 아랫변의 합 s = a+b를 계산."},
            {"step": 2, "title": "외접 사각형 성질 적용", "description": "원 외접 사각형의 성질(a+b = 2c)에 따라 빗변 c의 길이를 산출."},
            {"step": 3, "title": "밑변의 차 계산", "description": "피타고라스 정리 (a-b)^2/4 + h^2 = c^2를 이용하여 (a-b)^2 값을 도출."},
            {"step": 4, "title": "제곱의 합 산출", "description": "a^2+b^2 = ((a+b)^2 + (a-b)^2)/2 공식을 사용하여 최종 정답 계산."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def solve_static(cls, radius, area):
        h = 2 * radius
        sum_rs = 2 * area / h
        side = sum_rs / 2
        half_diff_sq = side**2 - h**2
        diff_rs_sq = 4 * half_diff_sq
        return int(round((sum_rs**2 + diff_rs_sq) / 2))

    @classmethod
    def generate_seed(cls, level=3):
        for _ in range(100):
            radius = random.randint(2, 6)
            # Area must be > 4r^2
            min_area = 4 * (radius**2) + 2
            area = random.randint(min_area, 300)
            if area % radius == 0:
                ans = cls.solve_static(radius, area)
                if 0 <= ans <= 999:
                    return {'radius': radius, 'area': area, 'expected_t': ans}
        return {'radius': 3, 'area': 72, 'expected_t': 504}

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            h, s, r = random.randint(4, 12), random.randint(2, 10), random.randint(12, 20)
            return {'r': r, 's': s, 'h': h, 'expected_t': float((r+s)*h//2), 'drill_level': 1}
        elif level == 2:
            s, r = random.randint(2, 10), random.randint(12, 20)
            return {'r': r, 's': s, 'expected_t': float((r+s)//2), 'drill_level': 2}
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Basic Area Formula",
                "goal": "Calculate the area of a standard isosceles trapezoid.",
                "details": "주어진 밑변(r, s)과 높이(h)를 가진 등변사다리꼴의 넓이를 구하는 기초 상황을 설정하세요."
            }
        elif level == 2:
            return {
                "focus": "Inscribed Property",
                "goal": "Identify that the non-parallel side length is the average of the bases in a tangential trapezoid.",
                "details": "원 외접 사각형의 성질을 이용하여 빗변의 길이를 구하는 핵심 논리에 집중하세요."
            }
        return {
            "focus": "Geometric Synthesis",
            "goal": "Solve for the sum of squares of bases using inscribed circle radius and area.",
            "details": "내접원의 반지름과 넓이가 주어졌을 때, 등변사다리꼴의 성질을 종합하여 밑변 제곱의 합을 구하는 AIME 스타일 문항으로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        radius, area = seed.get('radius'), seed.get('area')
        return f"An isosceles trapezoid has an inscribed circle of radius {radius} and its area is {area}. Calculate the sum of the squares of the lengths of its two parallel sides."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Find the area of an isosceles trapezoid with parallel sides of length {seed['r']} and {seed['s']}, and a height of {seed['h']}."
        elif level == 2:
            return f"An isosceles trapezoid has an inscribed circle. If the parallel sides have length {seed['r']} and {seed['s']}, find the length of each non-parallel side."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def generate_image(cls, seed, filepath):
        fig, ax = plt.subplots(figsize=(4, 4))
        R = seed.get('radius', 3)
        ax.add_artist(plt.Circle((0, R), R, color='#3b82f6', fill=False, linewidth=2))
        ax.axis('off')
        plt.savefig(filepath, dpi=120, bbox_inches='tight')
        plt.close(fig)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) == 3:
            if str(seed['radius']) not in narrative or str(seed['area']) not in narrative:
                return False, "Radius or Area missing"
        return True, "OK"
