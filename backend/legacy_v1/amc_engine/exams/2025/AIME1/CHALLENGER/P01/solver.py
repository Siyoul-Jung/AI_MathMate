import math
import random
import matplotlib.pyplot as plt
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "NT-BASE-DIV-SUM",
        "categories": ["Number Theory"],
        "topics": ["Base Conversion", "Divisibility", "Polynomial Division", "Divisor Counting"],
        "context_type": "abstract",
        "level": 1,
        "has_image": False,
        "is_mock_ready": True,
        "seed_constraints": {
            "X": {"min_val": 2, "max_val": 12, "type": "int", "description": "High digit of dividend"},
            "Y": {"min_val": 1, "max_val": 15, "type": "int", "description": "Low digit of divisor"},
            "W": {"min_val": 1, "max_val": 15, "type": "int", "description": "Low digit of dividend"}
        },
        "logic_steps": [
            {"step": 1, "title": "진법 변환 및 수식화", "description": "각 진법 수를 10진법 다항식 (b+Y)와 (Xb+W)로 변환하고 나눗셈 조건을 명시."},
            {"step": 2, "title": "나눗셈 정리", "description": "Xb+W = X(b+Y) + (W-XY) 관계식을 활용하여 (b+Y)가 (W-XY)의 약수여야 함을 유도."},
            {"step": 3, "title": "가능한 진법 후보 탐색", "description": "|W-XY|의 약수들 중 진법 제약 조건 b > max(digits)를 만족하는 b 값들을 식별."},
            {"step": 4, "title": "합산 및 정답 도출", "description": "조건을 만족하는 모든 진법 b를 합산하여 최종 정답 산출."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def generate_seed(cls, level=3):
        # Official Benchmark: 17_b divides 97_b for b > 9.
        # X=9, Y=7, W=7. min_b=9. Result 70.
        GOLDEN = {'X': 9, 'Y': 7, 'W': 7, 'divisor_str': '17', 'dividend_str': '97', 'min_b': 9, 'remainder_constant': 56, 'expected_t': 70}
        for _ in range(100):
            # 5% chance to return golden directly for stability
            if random.random() < 0.05: return GOLDEN
            X, Y, W = random.randint(2, 12), random.randint(1, 15), random.randint(1, 15)
            # ...
            min_b = max(X, Y, W)
            R = abs(W - X * Y)
            if R < 25: continue
            factors = cls.get_factors(R)
            valid_bases = [k - Y for k in factors if (k - Y) > min_b]
            if len(valid_bases) >= 2:
                ans = sum(valid_bases)
                if 0 <= ans <= 999:
                    return {
                        'X': X, 'Y': Y, 'W': W,
                        'divisor_str': f"1{cls.to_base_char(Y)}",
                        'dividend_str': f"{cls.to_base_char(X)}{cls.to_base_char(W)}",
                        'min_b': min_b, 'remainder_constant': R, 'expected_t': ans
                    }
        return GOLDEN

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            seed['target_b'] = seed['min_b'] + random.randint(2, 5)
            seed['expected_t'] = float(seed['X'] * seed['target_b'] + seed['W'])
        elif level == 2:
            X, Y, W, min_b = seed['X'], seed['Y'], seed['W'], seed['min_b']
            factors = cls.get_factors(abs(W - X * Y))
            valid_bases = [k - Y for k in factors if (k - Y) > min_b]
            seed['expected_t'] = float(min(valid_bases))
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Base Conversion",
                "goal": "Verify the student can convert a base-b number to base-10.",
                "details": "주어진 특정 진법(b)의 수 {dividend_str}를 10진법으로 변환하는 기초적인 상황을 설정하세요."
            }
        elif level == 2:
            return {
                "focus": "Divisibility Search",
                "goal": "Find the smallest valid base satisfying the division property.",
                "details": "나눗셈이 떨어지는 가장 작은 진법 b를 찾는 과정에 집중하여 지문을 구성하세요."
            }
        return {
            "focus": "Full AIME Theory",
            "goal": "Find the sum of all valid bases.",
            "details": "제시된 다항식 형태의 진법 나눗셈 조건을 만족하는 모든 진법의 합을 구하는 정규 AIME 스타일로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        div, dnd, min_b = seed['divisor_str'], seed['dividend_str'], seed['min_b']
        return f"Find the sum of all integer bases $b > {min_b}$ such that the base-$b$ number ${dnd}_b$ is divisible by the base-$b$ number ${div}_b$."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Find the base-10 value of the number ${seed['dividend_str']}_{{{seed['target_b']}}}$."
        elif level == 2:
            return f"Find the smallest integer base $b > {seed['min_b']}$ such that ${seed['dividend_str']}_b$ is divisible by ${seed['divisor_str']}_b$."
        return cls.get_narrative_instruction(seed)

    @staticmethod
    def get_factors(n):
        return sorted({i for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0} | {n // i for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0})

    @staticmethod
    def to_base_char(n):
        return str(n) if n < 10 else chr(ord('A') + (n - 10))

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        div, dnd = seed.get('divisor_str'), seed.get('dividend_str')
        if seed.get('drill_level') != 1:
            if div not in narrative: return False, f"Divisor {div} missing"
            if dnd not in narrative: return False, f"Dividend {dnd} missing"
        return True, "OK"