import random
from fractions import Fraction
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-21-01] 유리수와 순환소수 (T108 ~ T112)
# ==========================================

class T108_Master(BaseTMaster):
    """T108: 유리수와 소수의 분류"""
    def __init__(self):
        super().__init__("T108", "유한소수와 무한소수")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 유한소수: 분모의 소인수가 2나 5뿐인 기약분수
        def is_finite(n, d):
            g = MathUtils.get_gcd(n, d)
            d //= g
            while d % 2 == 0: d //= 2
            while d % 5 == 0: d //= 5
            return d == 1

        candidates = []
        for _ in range(5):
            n = random.randint(1, 20)
            d = random.randint(2, 50)
            candidates.append(Fraction(n, d))
            
        find_finite = random.choice([True, False])
        target_type = "유한소수" if find_finite else "무한소수"
        
        answers = [f for f in candidates if is_finite(f.numerator, f.denominator) == find_finite]
        
        if not answers or len(answers) == len(candidates):
            n = random.randint(1, 10)
            if find_finite:
                d = random.choice([2, 4, 5, 8, 10, 16, 20, 25])
            else:
                d = random.choice([3, 6, 7, 9, 11, 12, 13, 14])
            ans_frac = Fraction(n, d)
            candidates[0] = ans_frac
            answers = [ans_frac]

        ans = answers[0]
        
        data = {
            "question": f"다음 분수 중 {target_type}로 나타낼 수 {'있는' if find_finite else '없는'} 것은?",
            "options": list(set([f"{c.numerator}/{c.denominator}" for c in candidates])), # 중복 제거
            "answer": f"$\\frac{{{ans.numerator}}}{{{ans.denominator}}}$",
            "explanation": "기약분수로 나타내었을 때 분모의 소인수가 2나 5뿐이면 유한소수, 그 외의 소인수가 있으면 무한소수(순환소수)입니다."
        }
        
        # 옵션이 4개 미만이면 추가 생성 (드문 경우)
        while len(data["options"]) < 4:
            n = random.randint(1, 20)
            d = random.randint(2, 50)
            frac = f"{n}/{d}"
            if frac not in data["options"]:
                data["options"].append(frac)
        random.shuffle(data["options"])
        
        if q_type == "short_answer":
            data = {
                "question": f"분수 $\\frac{{{ans.numerator}}}{{{ans.denominator}}}$은 유한소수인가 무한소수인가?",
                "answer": target_type,
                "explanation": "기약분수로 나타내었을 때 분모의 소인수를 확인합니다."
            }
            
        return self._format_response(data, q_type, difficulty)

class T109_Master(BaseTMaster):
    """T109: 순환소수의 표현"""
    def __init__(self):
        super().__init__("T109", "순환마디")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        pattern = [str(random.randint(0, 9)) for _ in range(random.randint(1, 3))]
        prefix = [str(random.randint(0, 9)) for _ in range(random.randint(0, 2))]
        
        while len(pattern) == 1 and pattern[0] == '0':
             pattern = [str(random.randint(1, 9))]
             
        decimal_str = f"$0.{''.join(prefix)}{''.join(pattern)}\\dots$"
        cycle = "".join(pattern)
        
        data = {
            "question": f"순환소수 {decimal_str} 의 순환마디를 구하시오.",
            "answer": cycle,
            "explanation": f"소수점 아래에서 {cycle}이 반복되므로 순환마디는 {cycle}입니다."
        }
        
        if q_type == "multi":
            options = [cycle, cycle[::-1], prefix[-1]+cycle if prefix else cycle+'0', cycle+cycle[0]]
            options = list(set(options))[:4]
            while len(options) < 4: options.append(str(random.randint(10, 99)))
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T110_Master(BaseTMaster):
    """T110: 유한소수가 되도록 하는 미지수 구하기"""
    def __init__(self):
        super().__init__("T110", "유한소수 만들기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        k = random.choice([3, 7, 9, 11, 13])
        if difficulty == "Hard": k = random.choice([21, 33, 39])
        
        denom = k * random.choice([2, 4, 5, 8, 10, 20])
        num = random.randint(1, denom-1)
        
        while MathUtils.get_gcd(num, denom) % k == 0:
            num = random.randint(1, denom-1)
            
        factors = MathUtils.get_prime_factors(denom // MathUtils.get_gcd(num, denom))
        ans = 1
        for p, e in factors.items():
            if p != 2 and p != 5:
                ans *= (p**e)
                
        data = {
            "question": f"분수 $\\frac{{{num}}}{{{denom}}}$에 자연수 $x$를 곱하여 유한소수가 되게 하려고 한다. $x$의 값 중 가장 작은 자연수는?",
            "answer": ans,
            "explanation": f"분모를 소인수분해하여 2와 5 이외의 소인수를 없애야 합니다. {denom}의 소인수 중 2, 5가 아닌 것은 {ans}이므로 x는 {ans}의 배수여야 합니다."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 5) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T111_Master(BaseTMaster):
    """T111: 순환소수를 분수로 나타내기"""
    def __init__(self):
        super().__init__("T111", "순환소수를 분수로")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 순환마디 길이 1~2
        cycle_len = random.randint(1, 2)
        non_cycle_len = random.randint(0, 1)
        
        if difficulty == "Easy":
            non_cycle_len = 0
            cycle_len = 1
        elif difficulty == "Hard":
            non_cycle_len = random.randint(1, 2)
            cycle_len = random.randint(2, 3)
            
        # 분모 생성 (9, 90, 99, 900, 990, 999)
        denom_str = '9' * cycle_len + '0' * non_cycle_len
        denom = int(denom_str)
        
        # 분자 생성
        num = random.randint(1, denom - 1)
        while num % 2 == 0 or num % 5 == 0:
             num = random.randint(1, denom - 1)
             
        ans_frac = Fraction(num, denom)
        
        # 순환소수 표기 (텍스트)
        # 0.a (dot) 또는 0.ab (b dot)
        if non_cycle_len == 0:
            cycle_val = random.randint(1, 10**cycle_len - 1)
            cycle_str = f"{cycle_val:0{cycle_len}d}"
            q_str = f"0.\\dot{{{cycle_str[0]}}}" if len(cycle_str) == 1 else f"0.\\dot{{{cycle_str[0]}}}\\dot{{{cycle_str[-1]}}}"
            q_desc = f"순환소수 ${q_str}$"
            numerator = cycle_val
            denominator = int('9' * cycle_len)
        else:
            non_cycle_val = random.randint(0, 10**non_cycle_len - 1)
            non_cycle_str = f"{non_cycle_val:0{non_cycle_len}d}"
            cycle_val = random.randint(0, 10**cycle_len - 1)
            cycle_str = f"{cycle_val:0{cycle_len}d}"
            q_str = f"0.{non_cycle_str}\\dot{{{cycle_str[0]}}}" if len(cycle_str) == 1 else f"0.{non_cycle_str}\\dot{{{cycle_str[0]}}}\\dot{{{cycle_str[-1]}}}"
            q_desc = f"순환소수 ${q_str}$"
            
            total_val = int(non_cycle_str + cycle_str)
            numerator = total_val - int(non_cycle_str)
            denominator = int('9' * cycle_len + '0' * non_cycle_len)

        ans_frac = Fraction(numerator, denominator)
        
        data = {
            "question": f"{q_desc}를 기약분수로 나타내시오.",
            "answer": f"$\\frac{{{ans_frac.numerator}}}{{{ans_frac.denominator}}}$",
            "explanation": f"분모는 순환마디 숫자의 개수만큼 9를 쓰고 그 뒤에 소수점 아래 순환하지 않는 숫자의 개수만큼 0을 씁니다.\n분자는 (전체 수) - (순환하지 않는 부분) 입니다.\n$\\frac{{{numerator}}}{{{denominator}}} = \\frac{{{ans_frac.numerator}}}{{{ans_frac.denominator}}}$"
        }
        
        if q_type == "multi":
            f1 = Fraction(numerator, int('9' * (cycle_len + non_cycle_len)))
            f2 = Fraction(numerator, int('1' + '0' * (cycle_len + non_cycle_len)))
            f3 = Fraction(numerator + 1, denominator)
            
            options = [f"$\\frac{{{ans_frac.numerator}}}{{{ans_frac.denominator}}}$", 
                       f"$\\frac{{{f1.numerator}}}{{{f1.denominator}}}$",
                       f"$\\frac{{{f2.numerator}}}{{{f2.denominator}}}$",
                       f"$\\frac{{{f3.numerator}}}{{{f3.denominator}}}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T112_Master(BaseTMaster):
    """T112: 유리수와 순환소수의 관계 (O/X)"""
    def __init__(self):
        super().__init__("T112", "유리수와 순환소수 관계")

    def generate(self, difficulty="Normal", q_type="ox"):
        statements = [
            {"q": "모든 순환소수는 유리수이다.", "a": "O", "e": "순환소수는 분수로 나타낼 수 있으므로 유리수입니다."},
            {"q": "모든 무한소수는 유리수이다.", "a": "X", "e": "순환하지 않는 무한소수(무리수)는 유리수가 아닙니다."},
            {"q": "유리수는 정수와 유한소수로 이루어져 있다.", "a": "X", "e": "유리수에는 순환소수도 포함됩니다."},
            {"q": "모든 유한소수는 유리수이다.", "a": "O", "e": "유한소수는 분수로 나타낼 수 있으므로 유리수입니다."},
            {"q": "0은 유리수가 아니다.", "a": "X", "e": "0은 0/1 등으로 나타낼 수 있으므로 유리수입니다."}
        ]
        
        item = random.choice(statements)
        
        data = {
            "question": f"다음 설명의 참(O), 거짓(X)을 판별하시오.\n'{item['q']}'",
            "options": ["O", "X"],
            "answer": item['a'],
            "explanation": item['e']
        }
        
        return self._format_response(data, q_type, difficulty)
