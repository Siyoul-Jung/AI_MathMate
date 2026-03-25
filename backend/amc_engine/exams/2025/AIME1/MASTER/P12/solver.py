import random

class Solver:
    DNA = {
        "context_type": "abstract",
        "specific_tag": "REGION-PLANE-INEQ",
        "level": 12
    }
    DRILL_LEVELS = [1, 2, 3]
    DIFFICULTY_BAND = "MASTER"

    def __init__(self, payload=None, config=None):
        self.payload = payload or {}

    @classmethod
    def generate_seed(cls):
        """
        N ≡ 3 (mod 6) 조건에서만 삼각형 꼭짓점이 정수가 되어 깔끔한 문제 생성.
        Answer = (N+3)^2 / 12 + 3
        N ∈ {3, 9, ..., 105} (18가지, AIME 정답 ≤ 999 보장)
        """
        # Original AIME 2025 I #12 used N=75 (Ans: 510)
        for _ in range(50):
            k = random.randint(0, 17)
            N = 6 * k + 3
            if N == 75: continue
            
            ans = (N + 3) ** 2 // 12 + 3
            return {
                'N': N,
                'expected_t': ans,
                'P1': (-1, -1, N + 2),
                'P2': (round(N/3,1), round(N/3,1), round(N/3,1))
            }
        return {'N': 33, 'expected_t': 111, 'P1': (-1, -1, 35), 'P2': (11.0, 11.0, 11.0)}

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        
        if level == 1:
            x = random.randint(-5, 5)
            y = random.randint(-5, 5)
            z = seed['N'] - x - y
            mid_val = y - z*x
            seed['target_point'] = (x, y, z)
            seed['expected_t'] = float(mid_val)
        elif level == 2:
            seed['expected_t'] = -1.0
        else:
            pass
            
        return seed

    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_drill_instruction(cls, seed, level):
        N = seed['N']
        if level == 1:
            x, y, z = seed['target_point']
            return (
                "Construct a direct math drill problem focusing on algebraic evaluation.\n"
                f"Consider a point in 3D space $(x, y, z) = ({x}, {y}, {z})$.\n"
                "Evaluate the expression $y - zx$.\n"
                "Provide the numeric answer only."
            )
        elif level == 2:
            return (
                "Construct a technical math problem focusing on geometric boundaries.\n"
                "The inequality $x - yz < y - zx$ can be factored into $(x - y)(f(z)) < 0$.\n"
                "Identify the constant $c$ such that $f(z) = z - c$.\n"
                "Find the value of $c$."
            )
        else:
            import random
            themes = ["Satellite Mesh Optimization", "Architectural Stress Zones", "Subatomic Force Fields"]
            theme = random.choice(themes)
            return (
                f"Construct a difficult modeling problem wrapped in the theme of [{theme}].\n"
                f"Embed this math: Points on the plane $x + y + z = {N}$ satisfy $x - yz < y - zx < z - xy$.\n"
                "There is exactly one finite area formed by these constraints.\n"
                "Calculate this area, express it as $a\sqrt{b}$, and find $a + b$."
            )

    @classmethod
    def get_narrative_instruction(cls, seed):
        N = seed['N']
        return (
            "Write an official AIME competition problem.\n"
            f"Plane: $x + y + z = {N}$. Condition: $x - yz < y - zx < z - xy$.\n"
            "Find the sum $a+b$ where the finite area is $a\sqrt{b}$."
        )

    @classmethod
    def verify_narrative(cls, narrative, seed):
        """
        Legacy interface — actual verification handled by verifier.py Stage 2 (REGION-PLANE-INEQ).
        """
        N = seed.get('N')
        if str(N) not in narrative:
            return False, f"Plane constant N={N} not found in narrative"
        return True, "OK"
