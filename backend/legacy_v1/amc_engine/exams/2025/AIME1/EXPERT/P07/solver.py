import math
from fractions import Fraction
import random
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "COMB-PAIRING-PROB",
        "categories": ["Combinatorics", "Probability"],
        "topics": ["Pairing Count", "Lexicographical Order", "Conditional Probability"],
        "context_type": "narrative",
        "level": 7,
        "has_image": False,
        "is_mock_ready": True,
        "seed_constraints": {
            "n_pairs": {"min_val": 4, "max_val": 7, "type": "int", "description": "Number of pairs (2n total items)"},
            "target_letter": {"min_val": "E", "max_val": "H", "type": "str", "description": "The specific letter to appear in the last pair"}
        },
        "logic_steps": [
            {"step": 1, "title": "전체 경우의 수 산출", "description": "2n개의 대상을 2개씩 짝짓는 총 방법의 수 (2n-1)!!를 계산."},
            {"step": 2, "title": "정렬 제약 조건 해석", "description": "쌍 내에서의 정렬과 쌍 간의 정렬 규칙에 따라 '마지막 쌍'의 수학적 의미를 정의."},
            {"step": 3, "title": "유리한 경우의 수 계산", "description": "타겟 문자가 마지막 쌍에 위치하게 되는 조합론적 배치 수를 산출."},
            {"step": 4, "title": "확률 및 정답 도출", "description": "확률 p = m/n을 구하고 m+n을 최종 정답으로 기록."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def solve_static(cls, n_pairs, target_idx):
        n = n_pairs * 2
        total_pairings = math.prod(range(n - 1, 0, -2))
        b, a = target_idx, n - 1 - target_idx
        count1 = a * math.comb(b, a-1) * math.factorial(a-1) * math.prod(range(b - a, 0, -2))
        count2 = math.factorial(a) if (b >= a and b > 0) else 0
        return Fraction(count1 + count2, total_pairings)

    @classmethod
    def generate_seed(cls, level=3):
        GOLDEN = {'n_pairs': 6, 'target_letter': 'G', 'expected_t': 821}
        for _ in range(50):
            n_pairs = random.randint(4, 7)
            target_idx = random.randint(n_pairs - 2, n_pairs + 1)
            target_char = chr(ord('A') + target_idx)
            prob = cls.solve_static(n_pairs, target_idx)
            if prob:
                ans = prob.numerator + prob.denominator
                if 0 <= ans <= 999:
                    return {'n_pairs': n_pairs, 'target_letter': target_char, 'expected_t': ans}
        return GOLDEN

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            n = random.choice([4, 6, 8, 10])
            return {'n_letters': n, 'expected_t': float(math.prod(range(n - 1, 0, -2))), 'drill_level': 1}
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Counting Principle",
                "goal": "Calculate the total number of pairings of n distinct items.",
                "details": "주어진 n개의 서로 다른 문자를 2개씩 짝지어 단어를 만드는 전체 경우의 수를 구하는 상황을 설정하세요."
            }
        elif level == 2:
            return {
                "focus": "Basic Probability",
                "goal": "Find the probability of a specific pair occurring.",
                "details": "전체 경우의 수 대비 특정 조건(예: 특정 두 문자가 한 쌍이 됨)을 만족하는 확률을 구하는 단계를 유도하세요."
            }
        return {
            "focus": "Order-Preserving Pairing",
            "goal": "Solve for the probability under complex alphabetizing constraints.",
            "details": "단어 내 알파벳 순서, 단어 간 알파벳 순서 정렬 조건을 모두 고려하여 마지막 단어의 첫 글자가 특정 문자일 확률을 구하는 AIME 스타일로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        n = seed['n_pairs'] * 2
        return f"{n} distinct items are randomly grouped into {seed['n_pairs']} pairs. The items within each pair are ordered, and then those pairs are sorted. If the last pair contains the target item '{seed['target_letter']}', find the probability $p$ as a reduced fraction and return sum of numerator and denominator."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Calculate the total number of ways to group {seed['n_letters']} distinct letters into pairs."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) == 3:
            if seed['target_letter'] not in narrative: return False, "Target letter missing"
        return True, "OK"
