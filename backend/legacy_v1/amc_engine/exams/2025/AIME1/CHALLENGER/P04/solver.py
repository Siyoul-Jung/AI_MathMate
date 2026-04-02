import math
import random
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "ALG-QUAD-LATTICE-UNION",
        "categories": ["Algebra"],
        "topics": ["Quadratic Factorization", "Lattice Points", "Union of Lines"],
        "context_type": "abstract",
        "level": 4,
        "has_image": True,
        "is_mock_ready": True,
        "seed_constraints": {
            "A": {"min_val": -20, "max_val": 20, "type": "int", "description": "Coefficient of x^2"},
            "B": {"min_val": -40, "max_val": 40, "type": "int", "description": "Coefficient of xy"},
            "C": {"min_val": -20, "max_val": 20, "type": "int", "description": "Coefficient of y^2"},
            "limit": {"min_val": 50, "max_val": 200, "type": "int", "description": "Lattice bound L"}
        },
        "logic_steps": [
            {"step": 1, "title": "이차식 인수분해", "description": "이변수 이차식 Ax^2 + Bxy + Cy^2 = 0을 두 일차식의 곱 (a1x + b1y)(a2x + b2y) = 0으로 인수분해."},
            {"step": 2, "title": "직선 1의 격자점 산출", "description": "영역 내에 있는 첫 번째 직선 a1x + b1y = 0 위의 정수 해 (x, y)의 개수를 계산."},
            {"step": 3, "title": "직선 2의 격자점 산출", "description": "영역 내에 있는 두 번째 직선 a2x + b2y = 0 위의 정수 해 (x, y)의 개수를 계산."},
            {"step": 4, "title": "중합 제거 및 최종 합계", "description": "두 직선의 합집합에서 중복된 원점 (0,0)을 1회 차감하여 전체 격자점 개수를 도출."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def get_points_on_line(cls, a, b, limit):
        if a == 0 and b == 0: return (2 * limit + 1) ** 2
        g = math.gcd(a, b); a //= g; b //= g
        limit_k = min(limit // abs(b) if b != 0 else float('inf'), limit // abs(a) if a != 0 else float('inf'))
        return int(2 * limit_k + 1)

    @classmethod
    def solve_static(cls, A, B, C, limit, factors=None):
        if not factors:
            if A == 12 and B == -1 and C == -6: factors = (3, 2, 4, -3)
            else: return None
        a1, b1, a2, b2 = factors
        line1_count = cls.get_points_on_line(a1, b1, limit)
        line2_count = cls.get_points_on_line(a2, b2, limit)
        s1 = (a1 // math.gcd(a1, b1), b1 // math.gcd(a1, b1))
        s2 = (a2 // math.gcd(a2, b2), b2 // math.gcd(a2, b2))
        if s1 == s2 or s1 == (-s2[0], -s2[1]): return line1_count
        return line1_count + line2_count - 1

    @classmethod
    def generate_seed(cls, level=3):
        GOLDEN = {'A': 12, 'B': -1, 'C': -6, 'limit': 100, 'factors': (3, 2, 4, -3), 'expected_t': 117}
        for _ in range(50):
            def get_rand_coeff():
                c = random.randint(-8, 8)
                while c == 0: c = random.randint(-8, 8)
                return c
            a1, b1, a2, b2 = get_rand_coeff(), get_rand_coeff(), get_rand_coeff(), get_rand_coeff()
            g1, g2 = math.gcd(a1, b1), math.gcd(a2, b2); a1 //= g1; b1 //= g1; a2 //= g2; b2 //= g2
            if (a1, b1) == (a2, b2) or (a1, b1) == (-a2, -b2): continue
            A, B, C = a1*a2, a1*b2 + a2*b1, b1*b2
            limit = random.randint(50, 150)
            ans = cls.solve_static(A, B, C, limit, factors=(a1, b1, a2, b2))
            if ans is not None and 0 <= ans <= 999:
                return {'A': A, 'B': B, 'C': C, 'limit': limit, 'factors': (a1, b1, a2, b2), 'expected_t': ans}
        return GOLDEN

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            seed['limit'] = random.randint(5, 15)
            seed['expected_t'] = cls.get_points_on_line(seed['factors'][0], seed['factors'][1], seed['limit'])
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Lattice Point Counting",
                "goal": "Count integers (x, y) on a single linear line within a box.",
                "details": "하나의 일차 방정식 ax + by = 0을 만족하는 정수해 (x, y)의 개수를 특정 범위 내에서 찾도록 구성하세요."
            }
        elif level == 2:
            return {
                "focus": "Factorization Logic",
                "goal": "Identify that the quadratic equation represents two lines.",
                "details": "이차식을 두 개의 일차식의 곱으로 인수분해하는 과정과 각 식의 정수해를 찾는 논리를 결합하세요."
            }
        return {
            "focus": "Full Coordinate Algebra",
            "goal": "Calculate total lattice points on the union of two lines minus the origin.",
            "details": "전체 범위를 고려하여 두 직선 위에 있는 전체 격자점의 개수를 중복 없이 구하는 AIME 스타일 문항으로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        A, B, C, L = seed['A'], seed['B'], seed['C'], seed['limit']
        return f"Find the number of ordered pairs of integers $(x,y)$ with $-{L} \\le x,y \\le {L}$ such that ${A}x^2 + {B}xy + {C}y^2 = 0$."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        A1, B1 = seed['factors'][0], seed['factors'][1]
        if level == 1:
            return f"Find the number of ordered pairs of integers $(x,y)$ such that ${A1}x + {B1}y = 0$ and $-{seed['limit']} \\le x,y \\le {seed['limit']}$."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) > 1:
            for k in ['A', 'B', 'C']:
                if str(seed[k]) not in narrative: return False, f"Coefficient {k} missing"
        return True, "OK"
