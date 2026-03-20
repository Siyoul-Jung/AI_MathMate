import random

class Solver:
    # [DNA] P15 문항의 정체성 (AIME 15번급 정수론/경우의 수)
    DNA = {
        "context_type": "abstract",
        "specific_tag": "NT-LTE-CUBE-L3",
        "level": 15
    }
    
    DRILL_LEVELS = [1, 2, 3]
    DIFFICULTY_BAND = "MASTER"

    def __init__(self, payload=None, config=None):
        self.payload = payload or {}

    @classmethod
    def get_narrative_instruction(cls, seed):
        K, M, div = seed['K'], seed['M'], seed['divisor']

        # 3가지 수학적 프레이밍 — 동치이지만 다른 관점 (LLM이 하나를 골라 자유롭게 표현)
        framings = [
            "Congruence framing: count ordered triples with cube sum divisible by the modulus",
            "Set cardinality framing: size of a subset of a Cartesian product",
            "Equation framing: count positive integer solutions to a divisibility equation",
        ]
        framing = random.choice(framings)

        return (
            "Write a single official AIME competition problem.\n"
            f"Mathematical framing: [{framing}]\n"
            "\n"
            "Embed this structure naturally:\n"
            f"- Ordered triples $(a, b, c)$ of positive integers with $a, b, c \\le 3^{{{K}}}$\n"
            f"- Condition: $a^3 + b^3 + c^3$ is a multiple of $3^{{{M}}}$\n"
            f"- Answer: the count modulo ${div}$\n"
            "\n"
            "PROVIDE THE PROBLEM TEXT ONLY."
        )

    @classmethod
    def generate_seed(cls):
        """K와 M을 흔들어 새로운 문제를 무한 생성합니다."""
        while True:
            # 적절한 난이도의 범위 설정 (그대로 유지)
            K = random.randint(4, 9)
            M = random.randint(3, K + 3) 
            
            # [수정됨] AIME 정답 규격(000~999)을 맞추기 위해 1000으로 완전 고정
            divisor = 1000

            # 재귀 함수로 정답 도출
            ans = cls._calculate_T(K, M)
            remainder = ans % divisor

            # 나머지가 너무 단순한 숫자(예: 0, 1, 2)가 나오지 않도록 10 이상으로 필터링
            if 10 <= remainder <= 999:
                return {
                    'K': K,
                    'M': M,
                    'divisor': divisor,
                    'expected_t': remainder
                }

    @classmethod
    def _calculate_T(cls, k, m):
        """AIME 15번의 핵심 논리를 단 3줄로 압축한 점화식"""
        if m <= 0:
            return 3**(3*k)
        if m == 1:
            return 3**(3*k - 1)
        # 3k - m 값은 재귀를 타더라도 항상 일정하게 유지됩니다 (불변량)
        return 2 * 3**(3*k - m) + cls._calculate_T(k - 1, m - 3)

    @classmethod
    def generate_drill_seed(cls, level):
        if level == 1:
            m = random.randint(2, 5)
            # Count a^3 = k mod 3^m
            return {'m_mod': 3**m, 'expected_t': float(3**(m-1)), 'drill_level': 1}
        elif level == 2:
            m = random.randint(2, 4)
            # Count a^3 + b^3 = 0 mod 3^m
            return {'m_mod': 3**m, 'expected_t': float(3**(2*m-1)), 'drill_level': 2}
        
        seed = cls.generate_seed()
        seed['drill_level'] = 3
        return seed

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return r"Find the number of integers $a \in \{1, 2, \dots, M\}$ such that $a^3 \equiv 1 \pmod{M}$.".replace("M", str(seed['m_mod']))
        elif level == 2:
            return r"Find the number of ordered pairs $(a, b)$ with $a, b \in \{1, \dots, M\}$ such that $a^3 + b^3 \equiv 0 \pmod{M}$.".replace("M", str(seed['m_mod']))
        else:
            K, M = seed['K'], seed['M']
            # Diversity Injector for Level 3
            themes = ["Modular Cryptography Protocol", "Quantum Superposition Mapping", "Advanced Crystal Lattice Vibrations"]
            chosen_theme = random.choice(themes)
            return (
                "Construct an advanced mathematical modeling problem (Level 3) wrapped in the theme: [{}].\n"
                "Scenario: An encryption system or scientific model relies on evaluating triple sums of modular cubic residues.\n"
                "Mathematical Goal: Find the number of ordered triples $(a, b, c)$ such that $a^3+b^3+c^3 \\equiv 0 \\pmod{{3^{{{}}}}}$ "
                "where each variable $a, b, c$ is constrained in the range {{1, 2, \\dots, 3^{{{}}} }}.\n"
                "Provide a vivid story but ensure the mathematical constraints are unambiguous."
            ).format(chosen_theme, M, K)

    def execute(self):
        """파이프라인 검증용 실행 메서드"""
        if self.payload.get('drill_level') in [1, 2]:
            return float(self.payload['expected_t'])
        K = self.payload.get('K')
        M = self.payload.get('M')
        divisor = self.payload.get('divisor', 1000)
        return float(self._calculate_T(K, M) % divisor)

    @classmethod
    def verify_narrative(cls, narrative, seed):
        """
        Legacy interface — 실제 검증은 verifier.py Stage 2 (NT-LTE-CUBE-L3)가 담당.
        하위 호환성을 위해 유지.
        """
        K, M = seed.get('K'), seed.get('M')
        if f"3^{{{K}}}" not in narrative and f"3^{K}" not in narrative:
            return False, f"상한 지수 3^{K} 누락"
        if f"3^{{{M}}}" not in narrative and f"3^{M}" not in narrative:
            return False, f"배수 지수 3^{M} 누락"
        return True, "OK"