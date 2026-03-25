import math
import random

class Solver:
    DRILL_LEVELS = [1, 2]
    def __init__(self, payload=None, config=None):
        self.payload = payload or {}
        self.config = config or {}

    @classmethod
    def solve_static(cls, T):
        # n_c > n_v > n_s >= 1
        # n_c + n_v + n_s = T
        count = 0
        for s in range(1, T // 3 + 1):
            for v in range(s + 1, T):
                c = T - s - v
                if c > v:
                    # Multinomial T! / (c! v! s!)
                    term = math.factorial(T) // (math.factorial(c) * math.factorial(v) * math.factorial(s))
                    count += term
        return count % 1000

    @classmethod
    def generate_seed(cls):
        # Copyright-Safe: Avoid T=9
        for _ in range(100):
            T = random.randint(7, 100)
            if T == 9: continue
            ans = cls.solve_static(T)
            return {'T': T, 'expected_t': ans}
        return {'T': 10, 'expected_t': 750}

    def execute(self):
        return self.payload['expected_t']

    @classmethod
    def get_narrative_instruction(cls, seed):
        return f"Calculate ice cream assignments for {seed['T']} players with flavor constraints C > V > S >= 1."

    @classmethod
    def generate_drill_seed(cls, level):
        import random
        if level == 1:
            # Level 1: Basic concept (e.g. 3 people, 3 flavors)
            return {'expected_t': 6}
        else:
            # Level 2: Coefficient calculation
            # Calculate for T=10, C=5, V=3, S=2 => 10! / (5! 3! 2!) = 3628800 / (120 * 6 * 2) = 2520
            return {'C': 5, 'V': 3, 'S': 2, 'T': 10, 'expected_t': 520} # 2520 % 1000 = 520

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return "How many ways are there to assign 3 distinct ice cream flavors (Chocolate, Vanilla, Strawberry) to 3 people such that each person gets exactly one flavor and all 3 flavors are used once?"
        else:
            return f"Calculate the multinomial coefficient for assigning {seed['T']} people to flavors where {seed['C']} people get Chocolate, {seed['V']} people get Vanilla, and {seed['S']} people get Strawberry. Provide the result modulo 1000."
