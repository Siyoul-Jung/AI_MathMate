import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-21-02] 단항식의 계산 (T113 ~ T116)
# ==========================================

class T113_Master(BaseTMaster):
    """T113: 지수법칙 (곱셈, 거듭제곱)"""
    def __init__(self):
        super().__init__("T113", "지수법칙(곱셈)")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # a^m * a^n = a^(m+n)
        # (a^m)^n = a^(mn)
        
        base = random.choice(['a', 'x', 'y', 'b'])
        m = random.randint(2, 5)
        n = random.randint(2, 5)
        
        type_ = random.choice(["mul", "pow"])
        
        if type_ == "mul":
            q_expr = f"${base}^{{{m}}} \\times {base}^{{{n}}}$"
            ans_exp = m + n
            expl = f"밑이 같은 거듭제곱의 곱셈은 지수끼리 더합니다. {m} + {n} = {ans_exp}"
        else:
            q_expr = f"$({base}^{{{m}}})^{{{n}}}$"
            ans_exp = m * n
            expl = f"거듭제곱의 거듭제곱은 지수끼리 곱합니다. {m} × {n} = {ans_exp}"
            
        ans = f"${base}^{{{ans_exp}}}$"
        
        data = {
            "question": f"다음 식을 간단히 하시오.\n{q_expr}",
            "answer": ans,
            "explanation": expl
        }
        
        if q_type == "multi":
            # 오답: 더하기/곱하기 혼동
            wrong_exp = m * n if type_ == "mul" else m + n
            options = [ans, f"${base}^{{{wrong_exp}}}$", f"${base}^{{{ans_exp+1}}}$", f"${base}^{{{ans_exp-1}}}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T114_Master(BaseTMaster):
    """T114: 지수법칙 (나눗셈)"""
    def __init__(self):
        super().__init__("T114", "지수법칙(나눗셈)")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # a^m ÷ a^n
        base = random.choice(['a', 'x', 'y'])
        n = random.randint(2, 5)
        diff = random.randint(1, 4)
        m = n + diff # m > n 보장 (중등 과정에서는 음수 지수 안 다룸)
        
        # 가끔 m = n 인 경우 (답 1)
        if random.random() < 0.2:
            m = n
            ans = "$1$"
            expl = f"지수가 같으므로 나눗셈의 결과는 1입니다."
        else:
            ans = f"${base}^{{{m-n}}}$"
            expl = f"밑이 같은 거듭제곱의 나눗셈은 지수끼리 뺍니다. {m} - {n} = {m-n}"
            
        data = {
            "question": f"다음 식을 간단히 하시오.\n${base}^{{{m}}} \\div {base}^{{{n}}}$",
            "answer": ans,
            "explanation": expl
        }
        
        if q_type == "multi":
            options = [ans, f"${base}^{{{m+n}}}$", "$0$", f"${base}^{{{n}}}$"]
            if ans == "$1$": options = ["$1$", "$0$", f"${base}$", f"${base}^2$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T115_Master(BaseTMaster):
    """T115: 단항식의 곱셈과 나눗셈"""
    def __init__(self):
        super().__init__("T115", "단항식의 곱셈/나눗셈")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # (ax^m) * (bx^n) 또는 나누기
        a = random.randint(2, 6) * random.choice([-1, 1])
        b = random.randint(2, 6) * random.choice([-1, 1])
        m = random.randint(1, 3)
        n = random.randint(1, 3)
        var = "x"
        
        op = random.choice(['×', '÷'])
        latex_op = "\\times" if op == '×' else "\\div"
        
        term1 = f"{a}{var}^{{{m}}}" if m > 1 else f"{a}{var}"
        term2 = f"{b}{var}^{{{n}}}" if n > 1 else f"{b}{var}"
        
        if op == '×':
            coeff = a * b
            exp = m + n
            ans = f"{coeff}{var}^{{{exp}}}"
            expl = f"계수는 계수끼리 곱하고({a}×{b}), 문자는 지수법칙을 이용하여 곱합니다({var}^{m}×{var}^{n})."
        else:
            # 나누어 떨어지도록 조정
            coeff = a * b
            exp = m + n
            # 문제: (coeff x^exp) ÷ (b x^n) = a x^m
            term1 = f"{coeff}{var}^{{{exp}}}"
            ans = f"{a}{var}^{{{m}}}" if m > 1 else f"{a}{var}"
            expl = f"계수는 계수끼리 나누고({coeff}÷{b}), 문자는 지수법칙을 이용하여 나눕니다({var}^{exp}÷{var}^{n})."
            
        data = {
            "question": f"다음 식을 간단히 하시오.\n${term1} {latex_op} {term2}$",
            "answer": f"${ans}$",
            "explanation": expl
        }
        
        if q_type == "multi":
            # 오답: 부호 실수, 지수 더하기/곱하기 혼동
            wrong_coeff = -coeff if op == '×' else -a
            wrong_exp = m * n if op == '×' else m + n # 말도 안되는 지수
            options = [f"${ans}$", f"${wrong_coeff}{var}^{{{exp if op=='×' else m}}}$", f"${coeff if op=='×' else a}{var}^{{{wrong_exp}}}$", f"${coeff if op=='×' else a}{var}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T116_Master(BaseTMaster):
    """T116: 단항식의 혼합 계산"""
    def __init__(self):
        super().__init__("T116", "단항식 혼합 계산")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A * B ÷ C 형태
        # 계수와 지수 계산이 복잡하지 않게 설정
        
        # 최종 정답: k * x^e
        k = random.randint(2, 5)
        e = random.randint(2, 5)
        
        # C: c * x^n
        c = random.randint(2, 4)
        n = random.randint(1, 3)
        
        # B: b * x^m
        b = random.randint(2, 4)
        m = random.randint(1, 3)
        
        # A = (Ans * C) / B 가 정수가 되도록 조정... 은 복잡하므로
        # A * B = Ans * C 로 역산
        # 계수: a * b = k * c => a = (k*c)/b. b를 k*c의 약수로 설정
        total_coeff = k * c
        divisors = [i for i in range(2, total_coeff) if total_coeff % i == 0]
        if not divisors: divisors = [1]
        b = random.choice(divisors)
        a = total_coeff // b
        
        # 지수: exp_a + m = e + n => exp_a = e + n - m
        exp_a = e + n - m
        if exp_a < 1: # 지수가 음수면 조정
            diff = 1 - exp_a
            exp_a += diff
            e += diff # 정답 지수도 증가
            
        term_a = f"{a}x^{{{exp_a}}}" if exp_a > 1 else f"{a}x"
        term_b = f"{b}x^{{{m}}}" if m > 1 else f"{b}x"
        term_c = f"{c}x^{{{n}}}" if n > 1 else f"{c}x"
        
        ans = f"{k}x^{{{e}}}"
        
        data = {
            "question": f"다음 식을 간단히 하시오.\n${term_a} \\times {term_b} \\div {term_c}$",
            "answer": f"${ans}$",
            "explanation": "곱셈과 나눗셈이 섞여 있을 때는 앞에서부터 차례대로 계산하거나, 나눗셈을 역수의 곱셈으로 바꾸어 계산합니다."
        }
        
        if q_type == "multi":
            options = [f"${ans}$", f"$-{ans}$", f"${k}x^{{{e+1}}}$", f"${k+1}x^{{{e}}}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
