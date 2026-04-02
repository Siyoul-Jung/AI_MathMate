import math
import random
import sympy.ntheory
import numpy as np
import matplotlib.pyplot as plt
from amc_engine.solvers.base_solver import BaseAIMESolver

class Solver(BaseAIMESolver):
    DNA = {
        "specific_tag": "COMB-SUDOKU-TOP3",
        "categories": ["Combinatorics"],
        "topics": ["Grid Permutations", "Sudoku Counting", "Franel Numbers", "Prime Factorization"],
        "context_type": "abstract",
        "level": 10,
        "has_image": True,
        "is_mock_ready": True,
        "seed_constraints": {
            "K": {"min_val": 1, "max_val": 3, "type": "int", "description": "Width of each 3xK block"}
        },
        "logic_steps": [
            {"step": 1, "title": "격자 구조 및 제약 파악", "description": "3x(3K) 격자에서 각 행과 3xK 블록이 1~3K를 중복 없이 포함해야 함을 이해."},
            {"step": 2, "title": "조합론적 공식 유도", "description": "프라넬 수(Franel number) S_K = sum(C(K,k)^3)를 활용하여 전체 경우의 수 N = (3K)! * S_K * (K!)^6 공식 도출."},
            {"step": 3, "title": "소인수분해 수행", "description": "구해진 경우의 수 N을 소인수분해하여 각 소수 p와 지수 e를 식별."},
            {"step": 4, "title": "지수와 소수의 곱 합산", "description": "최종적으로 sum(p * e)를 계산하여 정답 도출."}
        ]
    }
    
    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def get_logic_steps(cls, seed):
        return [s for s in cls.DNA['logic_steps']]

    @classmethod
    def compute_exact_answer(cls, K):
        S_K = sum(math.comb(K, k)**3 for k in range(K + 1))
        # Total ways: 3K! * S_K * (K!)^6
        total_ways = math.factorial(3 * K) * S_K * (math.factorial(K) ** 6)
        factors = sympy.ntheory.factorint(total_ways)
        return sum(p * e for p, e in factors.items())

    @classmethod
    def generate_seed(cls, level=3):
        for _ in range(50):
            K = random.choice([1, 2, 3])
            ans = cls.compute_exact_answer(K)
            if 0 <= ans <= 999:
                return {'K': K, 'expected_t': ans}
        return {'K': 2, 'expected_t': 38}

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        if level == 1:
            n = random.randint(5, 8)
            return {'n': n, 'expected_t': float(math.factorial(n)), 'drill_level': 1}
        return seed

    @classmethod
    def get_drill_intent(cls, level):
        if level == 1:
            return {
                "focus": "Factorial Counting",
                "goal": "Verify permutations of n distinct objects.",
                "details": "주어진 n명의 사람을 일렬로 세우는 기본적인 경우의 수를 구하는 상황을 설정하세요."
            }
        elif level == 2:
            return {
                "focus": "Latin Square Constraints",
                "goal": "Understand the row and block constraints in a grid.",
                "details": "행과 특정 모양의 블록에서 숫자가 중복되지 않아야 한다는 제약 조건을 해석하는 단계를 유도하세요."
            }
        return {
            "focus": "Prime Exponent Summation",
            "goal": "Apply Prime Factorization to calculate the final required sum.",
            "details": "전체 격자 채우기 경우의 수를 구하고, 이를 소인수분해하여 지수와 소수의 곱의 합을 구하는 AIME 스타일 문항으로 서술하세요."
        }

    @classmethod
    def get_narrative_instruction(cls, seed):
        k = seed['K']
        return f"A $3 \\times {3*k}$ grid is filled with numbers $1, 2, \\dots, {3*k}$ such that each row and each $3 \\times {k}$ block contain each number exactly once. Find the sum of $p \\cdot e$ where $\\prod p^e$ is the total count."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Find the number of ways to arrange numbers 1 to {seed['n']} in a single row."
        return cls.get_narrative_instruction(seed)

    @classmethod
    def generate_image(cls, seed, filepath):
        fig, ax = plt.subplots(figsize=(4, 2))
        ax.set_title(f"3 x {3*seed.get('K', 2)} Grid Filling", fontsize=10, fontweight='bold')
        ax.axis('off')
        plt.savefig(filepath, dpi=120, bbox_inches='tight')
        plt.close(fig)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        ok, msg = super().verify_narrative(narrative, seed)
        if not ok: return ok, msg
        if seed.get('drill_level', 3) == 3:
            if str(3*seed['K']) not in narrative: return False, "Grid dimension missing"
        return True, "OK"
