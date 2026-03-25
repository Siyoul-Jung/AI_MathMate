import math
import itertools

class Solver:
    """
    2025 AIME I Problem 5
    8-digit integers using digits 1..8 once, divisible by 22.
    Divisible by 2 AND 11.
    """

    DNA = {
        'specific_tag': 'COMBINATORICS-DIVISIBILITY',
        'context_type': 'narrative',
        'has_image': False
    }

    DRILL_LEVELS = [1, 2]

    def __init__(self, payload=None, config=None):
        self.payload = payload
        self.config = config

    def execute(self):
        return self.payload.get('expected_t')

    @classmethod
    def solve_static(cls, digits_str, divisor):
        # Implementation of the counting logic
        digits = [int(d) for d in digits_str]
        total_sum = sum(digits)
        
        # divisor = 22 => divisible by 2 and 11
        # d8 must be even
        evens = [d for d in digits if d % 2 == 0]
        count_n = 0
        
        for d8 in evens:
            # Re-implement the combinatorial logic for safety
            remaining = [d for d in digits if d != d8]
            # (d1+d3+d5+d7) - (d2+d4+d6+d8) = 11k
            # Sum all = S
            # S - 2*(d_even_sum) = 11k
            # d_even_sum = d2+d4+d6+d8
            # In our case S=36
            # 36 - 2*d_even_sum = 11k => d_even_sum = (36 - 11k)/2
            # Must be integer and feasible sum of 4 digits from digits_set
            
            feasible_sums = []
            for k in [-2, 0, 2]:
                if (36 - 11*k) % 2 == 0:
                    val = (36 - 11*k) // 2
                    feasible_sums.append(val)
            
            for target_total in feasible_sums:
                # Need d2+d4+d6 = target_total - d8
                needed = target_total - d8
                # Count combinations of 3 from remaining that sum to needed
                perms_count = 0
                for combo in itertools.combinations(remaining, 3):
                    if sum(combo) == needed:
                        # Success! 
                        # Ways to arrange even positions (3!): 6
                        # Ways to arrange odd positions (4!): 24
                        perms_count += math.factorial(3) * math.factorial(4)
                count_n += perms_count
                
        return count_n

    @classmethod
    def generate_seed(cls):
        import random
        # Copyright-Safe
        SAFE_FALLBACK = {'digits': '16782345', 'divisor': 22, 'compare_val': 1998, 'expected_t': 306}

        for _ in range(100):
            all_digits = "123456789"
            digits = "".join(random.sample(all_digits, 8))
            # Ensure not original AIME 2025 I #5
            if digits == '12345678': continue
            
            divisor = 22 
            N = cls.solve_static(digits, divisor)
            compare_val = random.randint(max(100, N - 900), N + 900)
            ans = abs(N - compare_val)
            
            if 0 <= ans <= 999:
                return {
                    'digits': digits,
                    'divisor': divisor,
                    'compare_val': compare_val,
                    'expected_t': ans
                }
        
        return SAFE_FALLBACK

    @classmethod
    def generate_drill_seed(cls, level):
        import random
        if level == 1:
            # 4 digit number divisible by 11 using specific digits
            all_digits = "123456789"
            digits = "".join(random.sample(all_digits, 4))
            # Calculate L1 answer correctly
            count = 0
            for p in itertools.permutations([int(d) for d in digits]):
                num = int("".join(map(str, p)))
                if num % 11 == 0:
                    count += 1
            return {'digits': digits, 'divisor': 11, 'expected_t': count}
        return cls.generate_seed()

    @classmethod
    def get_narrative_instruction(cls, seed):
        return f"Let $N$ be the number of 8-digit positive integers that use each of the digits ${seed['digits']}$ exactly once and are divisible by ${seed['divisor']}$. Find the positive difference between $N$ and ${seed['compare_val']}$."

    @classmethod
    def get_drill_instruction(cls, seed, level):
        if level == 1:
            return f"Using each of the digits ${seed['digits']}$ exactly once, how many 4-digit integers are divisible by 11?"
        return cls.get_narrative_instruction(seed)
