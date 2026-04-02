import math
import itertools
import random
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "NUM-DIVISIBILITY-22-PERM",
        "categories": ["Combinatorics", "Number Theory"],
        "topics": ["Divisibility Rules", "Alternating Sum", "Restricted Permutations"],
        "context_type": "abstract",
        "level": 5,
        "has_image": False,
        "is_mock_ready": True,
        "seed_constraints": {
            "digits": {"min_val": "12345678", "max_val": "23456789", "type": "str", "description": "8 distinct digits"},
            "divisor": {"min_val": 22, "max_val": 22, "type": "int", "description": "Divisor (default 22)"},
            "compare_val": {"min_val": 1000, "max_val": 3000, "type": "int", "description": "Value to compare N against"}
        },
        "logic_steps": [
            {"step": 1, "title": "배수 판정 조건 분석", "description": "22의 배수가 되기 위해 마지막 자리가 짝수여야 하고, 자릿수 교대합이 11의 배수임을 파악."},
            {"step": 2, "title": "부분집합 합 방정식 수립", "description": "홀수 번째 자리와 짝수 번째 자리 숫자의 합이 각각 전체 합의 절반인 18이 되어야 함을 유도."},
            {"step": 3, "title": "조건부 순열 카운팅", "description": "마지막 자리에 짝수가 오는 경우를 고정하고 나머지 자리를 채우는 경우의 수 N을 산출."},
            {"step": 4, "title": "비교값과의 차이 산출", "description": "|N - compare_val|를 계산하여 최종 정답 도출."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def solve_static(cls, digits_str, divisor):
        digits = [int(d) for d in digits_str]
        total_sum = sum(digits)
        # 22-divisibility: divisible by 2 and 11
        evens = [d for d in digits if d % 2 == 0]
        count_n = 0
        for d8 in evens:
            remaining = [d for d in digits if d != d8]
            feasible_sums = [ (total_sum - 11*k)//2 for k in [-2, 0, 2] if (total_sum - 11*k) % 2 == 0 ]
            for target_total in feasible_sums:
                needed = target_total - d8
                for combo in itertools.combinations(remaining, 3):
                    if sum(combo) == needed:
                        count_n += math.factorial(3) * math.factorial(4)
        return count_n

    @classmethod
    def generate_seed(cls, level=3):
        SAFE_FALLBACK = {'digits': '12345678', 'divisor': 22, 'compare_val': 2025, 'expected_t': 279}
        for _ in range(100):
            digits = "".join(random.sample("123456789", 8))
            N = cls.solve_static(digits, 22)
            compare_val = random.randint(max(100, N - 900), N + 900)
            ans = abs(N - compare_val)
            if 0 <= ans <= 999:
                return {'digits': digits, 'divisor': 22, 'compare_val': compare_val, 'expected_t': ans}
        return SAFE_FALLBACK

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            digits = "".join(random.sample("123456789", 4))
            count = sum(1 for p in itertools.permutations([int(d) for d in digits]) if int("".join(map(str, p))) % 11 == 0)
            return {'digits': digits, 'divisor': 11, 'expected_t': float(count), 'drill_level': 1}
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Basic Divisibility Rule",
                "goal": "Apply the rule for divisibility by 11.",
                "details": "주어진 4개의 숫자를 한 번씩 사용하여 11의 배수가 되는 4자리 정수의 개수를 구하는 기초 상황을 설정하세요."
            }
        elif level == 2:
            return {
                "focus": "Alternating Sum Constraint",
                "goal": "Formulate the subset sum equation for 11-divisibility.",
                "details": "각 자릿수의 교대합 성질을 이용하여 부분합 조건을 정교하게 구성하는 단계를 유도하세요."
            }
        return {
            "focus": "Full Combinatorial Parity",
            "goal": "Verify divisibility by 2 and 11 simultaneously with counting.",
            "details": "8자리 숫자의 배치 중 22의 배수가 되는 경우의 수를 구하고, 특정 값과의 차이를 구하는 AIME 스타일로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        return f"How many 8-digit integers can be formed using digits ${seed['digits']}$ exactly once that are divisible by ${seed['divisor']}$? Let this be $N$. Find $|N - {seed['compare_val']}|$, modulo 1000."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Using digits ${seed['digits']}$ exactly once, how many 4-digit integers are divisible by 11?"
        return cls.get_narrative_instruction(seed)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) == 3:
            if seed['digits'] not in narrative: return False, "Digits missing"
            if str(seed['compare_val']) not in narrative: return False, "Compare value missing"
        return True, "OK"
