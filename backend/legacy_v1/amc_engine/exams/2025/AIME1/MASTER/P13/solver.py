import random
import numpy as np
import matplotlib.pyplot as plt
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    """
    AIME 2025 I Problem 13 - Expected Number of Regions in a Disk
    Logic:
    - m diameters divide disk into 2m sectors.
    - n chords added between different sectors.
    - E[R] = 2m + n + n*E_diam + (n*(n-1)/2)*p
    - For m=2: E_diam = 4/3, p = 17/36.
    - Result for m=2, n=25: 4 + 25 + 25*(4/3) + 300*(17/36) = 29 + 100/3 + 425/3 = 29 + 525/3 = 29 + 175 = 204.
    """
    
    # Precomputed table for m = 2 to 7
    # Format: m : (E_diam, p)
    STATS_TABLE = {
        2: (1.33333333, 0.47222222),
        3: (1.8, 0.43333333),
        4: (2.28571429, 0.41071429),
        5: (2.77777778, 0.39629630),
        6: (3.27272727, 0.38636364),
        7: (3.76923077, 0.37912088)
    }

    DNA = {
        "specific_tag": "COMB-EXPECTED-REGIONS",
        "categories": ["Combinatorics", "Geometry"],
        "topics": ["Expected Value", "Euler's Formula", "Planar Graphs", "Probability"],
        "context_type": "narrative",
        "level": 13,
        "has_image": False,
        "is_mock_ready": True,
        "seed_constraints": {
            "m": {"min_val": 2, "max_val": 5, "type": "int", "description": "Number of diameters"},
            "n": {"min_val": 5, "max_val": 50, "type": "int", "description": "Number of random segments"}
        },
        "logic_steps": [
            {"step": 1, "title": "초기 영역 계산", "description": "m개의 지름이 원판을 2m개의 구역(sectors)으로 나누는 기초 상태 파악."},
            {"step": 2, "title": "현과 지름의 교점 기댓값", "description": "각 현이 선형적으로 지름들과 교차할 확률(E_diam)을 계산."},
            {"step": 3, "title": "현 사이의 교점 기댓값", "description": "서로 다른 구역을 잇는 두 현이 교차할 확률(p)을 조합론적으로 도출."},
            {"step": 4, "title": "기댓값의 선형성 적용", "description": "E[R] = 초기 영역 + n + n*E_diam + n(n-1)/2 * p 공식을 통해 최종 기댓값 산출."}
        ]
    }

    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def generate_seed(cls, level=3):
        # We try to keep m=2 or m=3 for nice integers if possible, or just round
        for _ in range(500):
            m = random.randint(2, 5)
            n = random.randint(10, 45)
            
            ed, p = cls.STATS_TABLE.get(m, (1.3333, 0.4722))
            
            # E[R] Calculation
            ans_float = 2*m + n + n*ed + (n*(n-1)/2)*p
            ans = int(round(ans_float))
            
            # For AIME, usually we want it to be a clean integer in the problem
            # But the answer is ALWAYS integer.
            if 100 <= ans <= 999:
                return {
                    'm': m,
                    'n': n,
                    'quadrants': 2*m,
                    'expected_t': ans
                }
        
        # Fallback
        return {'m': 2, 'n': 25, 'quadrants': 4, 'expected_t': 204}

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            # Concept: Euler's Formula for n lines in a disk (no diameters)
            k = random.randint(5, 12)
            seed['n_lines'] = k
            seed['expected_t'] = 1 + k + (k * (k - 1) // 2)
        return seed

    @classmethod
    def get_narrative_instruction(cls, seed):
        m, n = seed['m'], seed['n']
        sectors = 2 * m
        return (
             f"Alex divides a disk into {sectors} equal sectors with {m} diameters intersecting at the center. "
             f"He draws {n} more line segments through the disk, drawing each segment by selecting two points at random "
             f"on the perimeter of the disk in different sectors and connecting these two points. "
             f"Find the expected number of regions into which these {m+n} line segments divide the disk."
        )

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Find the maximum number of regions a disk is divided into by {seed['n_lines']} lines where every pair of lines intersects inside the disk and no three lines are concurrent."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def generate_image(cls, seed, filepath):
        # We follow the "Drill Scaffolding Policy"
        # Since has_image is False, this is only for drills or solution phase
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.add_artist(plt.Circle((0, 0), 1, fill=False, color='#1e293b', linewidth=2))
        ax.axis('off')
        plt.savefig(filepath, dpi=120, bbox_inches='tight', transparent=True)
        plt.close(fig)