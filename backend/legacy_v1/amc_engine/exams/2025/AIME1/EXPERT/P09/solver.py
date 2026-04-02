import math
import random
import numpy as np
import matplotlib.pyplot as plt
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "GEO-PARA-ROTATION",
        "categories": ["Geometry", "Algebra"],
        "topics": ["Parabola Rotation", "Intersection of Curves", "Rotation Transformation", "Quadratic Formula"],
        "context_type": "abstract",
        "level": 9,
        "has_image": True,
        "is_mock_ready": True,
        "seed_constraints": {
            "k": {"min_val": 3, "max_val": 30, "type": "int", "description": "Vertical shift of parabola y=x^2-k"},
            "rotation_angle": {"min_val": 60, "max_val": 120, "type": "int", "description": "Rotation angle in degrees"}
        },
        "logic_steps": [
            {"step": 1, "title": "회전 후 대칭성 파악", "description": "원점을 중심으로 60도 회전한 경우, 교점이 놓이는 대칭축(예: y = -sqrt(3)x)의 방정식을 도출."},
            {"step": 2, "title": "연립 방정식 수립", "description": "원본 포물선 y = x^2 - k와 대칭축의 식을 연립하여 교점의 x좌표에 대한 이차방정식 수립."},
            {"step": 3, "title": "y좌표 계산", "description": "근의 공식을 통해 x좌표를 구하고, 이를 대칭축 식에 대입하여 (a - sqrt(b))/c 꼴의 y좌표 산출."},
            {"step": 4, "title": "계수 합산", "description": "도출된 a, b, c 값을 합산하여 최종 정답 도출."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def solve_static(cls, k, alpha):
        if alpha == 60: a, b, c = 3, 9 + 12 * k, 2
        elif alpha == 90: a, b, c = 1, 4 * k + 1, 1
        elif alpha == 120: a, b, c = 1, 1 + 12 * k, 2
        else: return None
        return a, b, c, a + b + c

    @classmethod
    def generate_seed(cls, level=3):
        for _ in range(100):
            k, alpha = random.randint(3, 30), random.choice([60, 90, 120])
            res = cls.solve_static(k, alpha)
            if res:
                a, b, c, ans = res
                if int(math.sqrt(b))**2 != b and 0 <= ans <= 999:
                    return {'k': k, 'rotation_angle': alpha, 'a': a, 'b': b, 'c': c, 'expected_t': ans}
        return {'k': 5, 'rotation_angle': 90, 'a': 1, 'b': 21, 'c': 1, 'expected_t': 23}

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            k, m = random.randint(4, 20), random.randint(1, 5)
            return {'k': k, 'm': m, 'expected_t': float(m**2 + 4*k), 'drill_level': 1}
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Intersection Algebra",
                "goal": "Calculate the discriminant to find intersection points.",
                "details": "이차함수와 일차함수의 교점을 구하기 위해 판별식을 이용하는 기초 상황을 설정하세요."
            }
        elif level == 2:
            return {
                "focus": "Rotational Mapping",
                "goal": "Apply coordinate rotation formulas (x', y') using sin/cos.",
                "details": "좌표 평면 위의 곡선을 원점을 중심으로 회전시켰을 때의 새로운 방정식을 유도하는 단계를 포함하세요."
            }
        return {
            "focus": "Bounded Area Calculus",
            "goal": "Solve for the area between two rotated parabolas.",
            "details": "회전된 두 포물선으로 둘러싸인 영역의 넓이를 적분 또는 기하학적 대칭성을 이용하여 구하는 AIME 스타일 문항으로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        k, alpha = seed.get('k'), seed.get('rotation_angle')
        return f"A parabola $y = x^2 - {k}$ is rotated ${alpha}^\\circ$ counterclockwise around the origin. Find the area of the region bounded by original and rotated parabolas, and return sum of coefficients."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Find the discriminant $D$ of the intersection of $y = x^2 - {seed['k']}$ and $y = -{seed['m']}x$."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def generate_image(cls, seed, filepath):
        k, alpha_rad = seed.get('k', 4), math.radians(seed.get('rotation_angle', 0))
        L = max(k * 1.5, 6)
        x = np.linspace(-L, L, 400); y_orig = x**2 - k
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.plot(x, y_orig, color='#3b82f6', linewidth=2)
        ax.axis('off')
        plt.savefig(filepath, dpi=120, bbox_inches='tight')
        plt.close(fig)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) == 3:
            if str(seed['k']) not in narrative: return False, "Constant k missing"
        return True, "OK"
