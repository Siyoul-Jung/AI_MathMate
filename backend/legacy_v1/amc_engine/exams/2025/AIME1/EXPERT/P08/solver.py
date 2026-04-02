import random
import math
from fractions import Fraction
import matplotlib.pyplot as plt
import numpy as np
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "COMPLEX-GEO-BIS-TANGENCY",
        "categories": ["Geometry", "Complex Numbers"],
        "topics": ["Perpendicular Bisector", "Circle Tangency", "Complex Magnitude", "Linear Algebra"],
        "context_type": "abstract",
        "level": 8,
        "has_image": True,
        "is_mock_ready": True,
        "seed_constraints": {
            "c_real": {"min_val": 10, "max_val": 40, "type": "int", "description": "Real part of circle center"},
            "c_imag": {"min_val": 10, "max_val": 40, "type": "int", "description": "Imaginary part of circle center"},
            "r": {"min_val": 2, "max_val": 10, "type": "int", "description": "Radius of circle"}
        },
        "logic_steps": [
            {"step": 1, "title": "수직이등분선 식 유도", "description": "두 점 p1+k와 p2+k로부터 같은 거리에 있는 점 z의 궤적(수직이등분선)을 k를 포함한 직선의 방정식으로 도출."},
            {"step": 2, "title": "접선 조건 수립", "description": "원의 중심 c에서 수직이등분선까지의 거리가 반지름 r과 같아야 함을 의미하는 $|z-c|=r$ 조건을 정립."},
            {"step": 3, "title": "k에 대한 방정식 풀이", "description": "점과 직선 사이의 거리 공식을 활용하여 k에 대한 방정식을 구성하고 가능한 모든 k값을 계산."},
            {"step": 4, "title": "합산 및 정규화", "description": "모든 k의 합 m/n을 구하고 m+n을 최종 정답으로 산출."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def solve_static(cls, c_real, c_imag, r, p1_real, p1_imag, p2_real, p2_imag):
        x_mid_offset, y_mid = (p1_real + p2_real) / 2, (p1_imag + p2_imag) / 2
        dx, dy = p2_real - p1_real, p2_imag - p1_imag
        if dx == 0: return 0
        m_s = dy / dx
        if dy == 0:
            k1, k2 = c_real - x_mid_offset - r, c_real - x_mid_offset + r
            return k1 + k2
        m = -1 / m_s
        const_part, rhs = m * (c_real - x_mid_offset) - c_imag + y_mid, r * math.sqrt(m**2 + 1)
        k1, k2 = (const_part - rhs) / m, (const_part + rhs) / m
        return k1 + k2

    @classmethod
    def generate_seed(cls):
        GOLDEN = {'c_real': 25, 'c_imag': 20, 'r': 5, 'p1_real': 4, 'p1_imag': 0, 'p2_real': 0, 'p2_imag': 3, 'expected_t': 77}
        for _ in range(100):
            c_real, c_imag, r = random.randint(10, 40), random.randint(10, 40), random.randint(2, 10)
            p1_real, p1_imag = random.randint(0, 10), random.randint(0, 10)
            p2_real, p2_imag = random.randint(0, 10), random.randint(0, 10)
            if (p1_real, p1_imag) == (p2_real, p2_imag): continue
            res = cls.solve_static(c_real, c_imag, r, p1_real, p1_imag, p2_real, p2_imag)
            frac_res = Fraction(res).limit_denominator(100)
            if frac_res.denominator > 1:
                ans = frac_res.numerator + frac_res.denominator
                if 0 <= ans <= 999:
                    return {'c_real': c_real, 'c_imag': c_imag, 'r': r, 'p1_real': p1_real, 'p1_imag': p1_imag, 'p2_real': p2_real, 'p2_imag': p2_imag, 'expected_t': ans}
        return GOLDEN

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            x, y = random.randint(10, 30), random.randint(10, 30)
            return {'x': x, 'y': y, 'A': 3, 'B': -4, 'C': -10, 'expected_t': 2.0, 'drill_level': 1}
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Coordinate Distance",
                "goal": "Calculate distance from a point to a line.",
                "details": "좌표 평면 위의 한 점에서 직선까지의 거리를 구하는 기초적인 원리를 묻는 상황을 설정하세요."
            }
        elif level == 2:
            return {
                "focus": "Perpendicular Bisector",
                "goal": "Relate the equidistant property to the perpendicular bisector in the complex plane.",
                "details": "수직이등분선 위의 한 점이 두 점으로부터 같은 거리에 있다는 성질을 복소평면 관점에서 서술하세요."
            }
        return {
            "focus": "Tangency & Intersection",
            "goal": "Solve for parameters that guarantee unique tangency/intersection.",
            "details": "원이 이동하는 수직이등분선과 유일한 교점(접점)을 가질 조건($|z-c|=r$)을 기하학적으로 해결하는 AIME 스타일 문항으로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        c, r = f"{seed['c_real']} + {seed['c_imag']}i", seed['r']
        p1, p2 = f"{seed['p1_real']} + {seed['p1_imag']}i", f"{seed['p2_real']} + {seed['p2_imag']}i"
        return f"Circle $C$ in the complex plane has radius ${r}$ and center ${c}$. Given points $p_1={p1}$ and $p_2={p2}$, find the sum of all real $k$ such that there is a unique $z$ satisfying $|z-c|=r$ and $|z-(p_1+k)|=|z-(p_2+k)|$. Return result sum(num+den)."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Calculate the distance from the point $({seed['x']}, {seed['y']})$ to the line ${seed['A']}x + {seed['B']}y + {seed['C']} = 0$."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def generate_image(cls, seed, filepath):
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.set_aspect('equal')
        ax.add_artist(plt.Circle((seed.get('c_real', 25), seed.get('c_imag', 20)), seed.get('r', 5), color='#4338ca', fill=False, linewidth=2))
        ax.axis('off')
        plt.savefig(filepath, dpi=120, bbox_inches='tight')
        plt.close(fig)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) == 3:
            for k in ['c_real', 'c_imag', 'r']:
                if str(seed[k]) not in narrative: return False, f"Key {k} missing"
        return True, "OK"
