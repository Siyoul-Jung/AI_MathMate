import random
import numpy as np
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    """
    AIME 2025 I Problem 12 - Geometrical Region of Cyclic Inequalities on a Plane
    Logic:
    - Plane: x + y + z = N
    - Inequalities: x - yz < y - xz < z - xy
    - Region is 1/6 of an equilateral triangle formed by x=-1, y=-1, z=-1.
    - Triangle side s = (N+3) * sqrt(2).
    - Triangle Area = sqrt(3)/4 * s^2 = (N+3)^2 * sqrt(3) / 2.
    - Finite Region Area = (1/6) * Triangle Area = (N+3)^2 * sqrt(3) / 12.
    - Ans = a + b, where a = (N+3)^2 / 12 and b = 3.
    """
    
    DNA = {
        "specific_tag": "ALG-CYCLIC-INEQ-PLANE",
        "categories": ["Algebra", "Geometry"],
        "topics": ["Cyclic Inequalities", "Plane Geometry", "Symmetric Regions"],
        "context_type": "abstract",
        "level": 12,
        "has_image": False,
        "is_mock_ready": True,
        "seed_constraints": {
            "N": {"min_val": 15, "max_val": 105, "type": "int", "description": "Sum of coordinates (N+3 must be multiple of 6)"}
        },
        "logic_steps": [
            {"step": 1, "title": "평면상의 경계선 분석", "description": "부등식 x-yz = y-zx 등을 정리하여 x=y 또는 z=-1과 같은 경계 평면을 도출."},
            {"step": 2, "title": "정삼각형 영역 식별", "description": "평면 x+y+z=N과 x,y,z=-1들이 만나는 정삼각형 영역과 그 꼭짓점 좌표를 계산."},
            {"step": 3, "title": "대칭성을 이용한 넓이 계산", "description": "전체 삼각형 영역이 6개의 대칭적인 부등식 영역으로 나뉨을 파악하여 1/6 넓이를 공식화."},
            {"step": 4, "title": "수치 대입 및 결과 산출", "description": "도출된 넓이 a*sqrt(b)에서 a와 b를 추출하여 최종 합산(a+b)."}
        ]
    }

    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def generate_seed(cls, level=3):
        # N must be 6k-3 to make (N+3)^2 divisible by 12.
        # N+3 = 6k. (6k)^2 = 36k^2. 36k^2 / 12 = 3k^2 (integer).
        ks = list(range(3, 18)) # k=13 gives N=75
        for _ in range(200):
            k = random.choice(ks)
            N = 6 * k - 3
            a = (N + 3)**2 // 12
            b = 3
            ans = a + b
            if 100 <= ans <= 999:
                return {
                    'N': N,
                    'a': a,
                    'b': b,
                    'expected_t': ans
                }
        return {'N': 75, 'a': 507, 'b': 3, 'expected_t': 510}

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def get_narrative_instruction(cls, seed):
        N = seed['N']
        return (
            f"The set of points in three-dimensional coordinate space that lie in the plane $x+y+z={N}$ "
            f"whose coordinates satisfy the inequalities $x-yz < y-xz < z-xy$ forms three disjoint convex regions. "
            f"Exactly one of these regions has finite area. The area of this finite region can be expressed "
            f"in the form $a\\sqrt{{b}},$ where $a$ and $b$ are positive integers and $b$ is not divisible "
            f"by the square of any prime. Find $a+b.$"
        )

    @classmethod
    def get_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            # Atomic: Check if a point is on the plane
            N = seed['N']
            x = random.randint(10, 30)
            y = random.randint(10, 30)
            z = N - x - y
            seed['point'] = (x, y, z)
            seed['expected_t'] = x + y + z
        return seed

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            x, y, z = seed['point']
            return f"Given the point $(x, y, z) = ({x}, {y}, {z})$, find the value of $x+y+z$."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def generate_image(cls, seed, filepath):
        # Scaffolded image for drills: show the plane and triangle
        fig = plt.figure(figsize=(4, 4))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(f"Plane x+y+z={seed['N']}", fontsize=10)
        ax.axis('off')
        plt.savefig(filepath, dpi=120, transparent=True)
        plt.close(fig)
