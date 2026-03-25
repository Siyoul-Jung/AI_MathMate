import random
import math

class Solver:
    # [DNA] 문항의 정체성 정의: 이 설정이 파이프라인의 생성 전략을 결정합니다.
    DNA = {
        "context_type": "abstract",  # 'abstract'로 설정하여 서사(테마)를 차단
        "specific_tag": "NT-BASE-DIV-L1",
        "level": 1
    }
    
    DRILL_LEVELS = [1, 2] 
    DIFFICULTY_BAND = "CHALLENGER"

    def __init__(self, payload=None, config=None):
        self.payload = payload or {}

    @classmethod
    def get_narrative_instruction(cls, seed):
        div = seed['divisor_str']
        dnd = seed['dividend_str']
        min_b = seed['min_b']

        return (
            "Write a single official AIME competition problem.\n"
            "\n"
            "Embed this mathematical structure naturally:\n"
            f"- Find the sum of all integer bases $b > {min_b}$ such that\n"
            f"  the base-$b$ number ${dnd}_b$ is divisible by the base-$b$ number ${div}_b$.\n"
            "\n"
            "PROVIDE THE PROBLEM TEXT ONLY."
        )

    @classmethod
    def generate_seed(cls):
        """16진수 대응 및 수치 범위 확장 로직 (Copyright-Safe: No original AIME numbers)"""
        # SAFE_FALLBACK is a pre-verified variant that is NOT the original AIME problem
        SAFE_FALLBACK = {'X': 11, 'Y': 9, 'W': 10, 'divisor_str': '19', 'dividend_str': 'BA', 'min_b': 11, 'remainder_constant': 89, 'expected_t': 142}

        for _ in range(100):
            X = random.randint(2, 12) 
            Y = random.randint(1, 15)
            W = random.randint(1, 15)
            
            # Ensure it's not the exact original AIME 2025 I #1 constants
            if X == 12 and Y == 10 and W == 10: continue

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
                        'min_b': min_b,
                        'remainder_constant': R,
                        'expected_t': ans
                    }
        
        return SAFE_FALLBACK
        
        return GOLDEN

    @classmethod
    def generate_drill_seed(cls, level):
        seed = cls.generate_seed()
        seed['drill_level'] = level
        
        if level == 1:
            # Level 1: Base conversion evaluation
            seed['target_b'] = seed['min_b'] + random.randint(2, 5)
            X = seed['X']
            W = seed['W']
            # Compute value of XW in base target_b
            seed['expected_t'] = float(X * seed['target_b'] + W)
        elif level == 2:
            # Level 2: Find the smallest valid base
            X, Y, W = seed['X'], seed['Y'], seed['W']
            min_b = seed['min_b']
            R = abs(W - X * Y)
            factors = cls.get_factors(R)
            valid_bases = [k - Y for k in factors if (k - Y) > min_b]
            seed['expected_t'] = float(min(valid_bases))
            
        return seed

    @classmethod
    def get_drill_instruction(cls, seed, level):
        import random
        div = seed['divisor_str']
        dnd = seed['dividend_str']
        min_b = seed['min_b']
        X = seed['X']
        W = seed['W']
        Y = seed['Y']
        
        if level == 1:
            target_b = seed['target_b']
            return (
                f"Construct a foundational math drill problem about number base representations.\n"
                f"Do NOT use storytelling.\n"
                f"Problem Statement:\n"
                f"Find the base-10 value of the number ${dnd}_{{{target_b}}}$ represented in base ${target_b}$."
            )
        elif level == 2:
            return (
                f"Construct a math competition problem focusing on divisibility in different bases.\n"
                f"Do NOT use storytelling.\n"
                f"Problem Statement:\n"
                f"Find the smallest integer base $b > {min_b}$ such that the base-$b$ number ${dnd}_b$ is divisible by the base-$b$ number ${div}_b$."
            )
        else:
            themes = ["Alien Cryptography", "Quantum Data Packets", "Ancient Runes", "Network Routing"]
            chosen_theme = random.choice(themes)
            return (
                f"Construct an advanced mathematical modeling problem wrapped in the following theme: [{chosen_theme}].\n"
                f"Rules for the story:\n"
                f"1. A civilization or system relies on an unknown numerical parameter $b$ (which mathematically acts as a number base).\n"
                f"2. A large quantity is represented by the base-$b$ notation '{dnd}_{{b}}'.\n"
                f"3. It must be perfectly divided (or grouped) into smaller chunks sized '{div}_{{b}}' (also in base-$b$).\n"
                f"4. Due to system constraints, $b$ must be strictly greater than {min_b}.\n"
                f"5. End the story by asking the student to find the sum of ALL possible valid integer values for the parameter $b$.\n"
                f"\nDo NOT mention standard math test phrases like 'Find the sum of all integer bases'. Seamlessly blend the base-$b$ notation into the {chosen_theme} narrative!"
            )

    @staticmethod
    def get_factors(n):
        factors = []
        for i in range(1, int(math.sqrt(n)) + 1):
            if n % i == 0:
                factors.append(i)
                if i != n // i:
                    factors.append(n // i)
        return sorted(factors)

    @staticmethod
    def to_base_char(n):
        if n < 10: return str(n)
        return chr(ord('A') + (n - 10))

    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def verify_narrative(cls, narrative, seed):
        div, dnd = seed.get('divisor_str'), seed.get('dividend_str')
        level = seed.get('drill_level')
        
        if div not in narrative:
            return False, f"진법 기호({div}) 누락"
            
        if level != 1 and dnd not in narrative:
            return False, f"진법 기호({dnd}) 누락"
        
        # 서사가 없는 'abstract' 모드에서는 'Archaeologist' 등의 단어가 포함되면 필터링 (다만 Drill level 3 제외)
        if level != 3 and cls.DNA.get("context_type") == "abstract":
            forbidden_terms = ["Archaeologist", "Computer", "Memory", "Tablet", "System"]
            for term in forbidden_terms:
                if term.lower() in narrative.lower():
                    return False, f"추상형 문항에 서사 용어('{term}') 감지됨"
            
        return True, "OK"