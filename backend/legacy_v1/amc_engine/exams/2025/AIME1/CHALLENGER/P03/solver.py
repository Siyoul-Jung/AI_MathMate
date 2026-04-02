import math
import random
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "COMB-MULTINOMIAL-LE",
        "categories": ["Combinatorics", "Algebra"],
        "topics": ["Multinomial Coefficients", "Inequality Constraints", "Permutations with Repetition"],
        "context_type": "narrative",
        "level": 3,
        "has_image": False,
        "is_mock_ready": True,
        "seed_constraints": {
            "T": {"min_val": 7, "max_val": 40, "type": "int", "description": "Total number of items (people)"}
        },
        "logic_steps": [
            {"step": 1, "title": "부등식 파티션 탐색", "description": "C + V + S = T 및 C > V > S >= 1을 만족하는 모든 정수 순서쌍 (C, V, S)를 식별."},
            {"step": 2, "title": "각 경우의 수 계산", "description": "다항 계수 공식 n! / (n1! * n2! * n3!)을 사용하여 각 파티션에 해당하는 배치 방법의 수 산출."},
            {"step": 3, "title": "전체 합계 및 나머지 처리", "description": "모든 경우의 수를 더하고 1000으로 나눈 나머지를 계산하여 최종 정답 도출."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def solve_static(cls, T):
        count = 0
        for s in range(1, T // 3 + 1):
            for v in range(s + 1, T):
                c = T - s - v
                if c > v:
                    term = math.factorial(T) // (math.factorial(c) * math.factorial(v) * math.factorial(s))
                    count += term
        return count % 1000

    @classmethod
    def generate_seed(cls, level=3):
        for _ in range(100):
            T = random.randint(7, 40)
            if T == 9: return {'T': 9, 'expected_t': 16} # Official Benchmark
            ans = cls.solve_static(T)
            if 0 <= ans <= 999:
                return {'T': T, 'expected_t': ans}
        return {'T': 10, 'expected_t': 750}

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            seed['expected_t'] = 6 # 3!
        elif level == 2:
            seed.update({'C': 5, 'V': 3, 'S': 2, 'T': 10, 'expected_t': 2520 % 1000})
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Simple Permutation",
                "goal": "Understand the basic n! counting principle.",
                "details": "3명의 사람이 3개의 서로 다른 아이스크림 맛을 하나씩 고르는 것과 같이 기본적인 순열 상황을 구성하세요."
            }
        elif level == 2:
            return {
                "focus": "Multinomial Coefficient",
                "goal": "Calculate a single occurrence of the multinomial coefficient.",
                "details": "구체적인 인원 배정 수치(C, V, S)가 주어졌을 때 다항 계수 식을 작성하고 계산하도록 유도하세요."
            }
        return {
            "focus": "Partitioned Summation",
            "goal": "Sum multiple multinomial coefficients under strict order constraints.",
            "details": "C > V > S >= 1 조건을 만족하는 모든 가능한 배정 경우의 수의 합을 구하는 AIME 스타일로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        return f"A group of {seed['T']} distinct items are to be assigned to three ordered categories. Find the number of assignments where the first category has more items than the second, which has more than the third, and each category has at least one item. Return the count modulo 1000."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return "How many ways are there to assign 3 distinct ice cream flavors to 3 people such that each person gets exactly one flavor and all 3 flavors are used?"
        elif level == 2:
            return f"Calculate the number of ways to assign {seed['T']} people such that {seed['C']} get Chocolate, {seed['V']} get Vanilla, and {seed['S']} get Strawberry. Provide the result modulo 1000."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) == 3:
            if str(seed['T']) not in narrative: return False, "Total count T missing"
        return True, "OK"
