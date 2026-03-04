import math
import random
from fractions import Fraction

# ==========================================
# 1. 수학 공통 엔진 (Math Utility)
# ==========================================
class MathUtils:
    """모든 T-Master가 공통으로 사용하는 수학 연산 엔진"""
    
    @staticmethod
    def get_prime_factors(n):
        """소인수분해 결과를 dict 형태로 반환 (예: 12 -> {2: 2, 3: 1})"""
        i = 2
        factors = {}
        temp = n
        while i * i <= temp:
            if temp % i:
                i += 1
            else:
                temp //= i
                factors[i] = factors.get(i, 0) + 1
        if temp > 1:
            factors[temp] = factors.get(temp, 0) + 1
        return factors

    @staticmethod
    def is_prime(n):
        """소수 판별 알고리즘"""
        if n < 2: return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0: return False
        return True

    @staticmethod
    def get_gcd(a, b):
        """최대공약수 반환"""
        return math.gcd(a, b)

    @staticmethod
    def get_lcm(a, b):
        """최소공배수 반환"""
        return abs(a * b) // math.gcd(a, b)

    @staticmethod
    def get_random_fraction(min_val=-9, max_val=9, den_limit=10):
        """랜덤 기약분수 생성"""
        num = random.choice([i for i in range(min_val, max_val+1) if i != 0])
        den = random.randint(2, den_limit)
        return Fraction(num, den)

    @staticmethod
    def generate_distractors(answer, count=3, range_width=10, min_val=None):
        """정답 주변의 오답(distractors) 생성"""
        distractors = set()
        loop_cnt = 0
        while len(distractors) < count:
            loop_cnt += 1
            if loop_cnt > 100: break # 무한 루프 방지
            
            if isinstance(answer, int):
                d = answer + random.randint(-range_width, range_width)
                if min_val is not None and d < min_val:
                    continue
                if d != answer:
                    distractors.add(d)
        
        # 부족한 경우 채우기
        while len(distractors) < count:
            new_d = answer + len(distractors) + 1
            if min_val is not None and new_d < min_val:
                new_d = min_val + len(distractors)
            distractors.add(new_d)
            
        return list(distractors)
