import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-21-03] 다항식의 계산 (T117 ~ T121)
# ==========================================

class T117_Master(BaseTMaster):
    """T117: 다항식의 덧셈과 뺄셈"""
    def __init__(self):
        super().__init__("T117", "다항식의 덧셈/뺄셈")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # (ax + by + c) op (dx + ey + f)
        vars = ['x', 'y']
        
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        
        d = random.randint(-5, 5)
        e = random.randint(-5, 5)
        f = random.randint(-5, 5)
        
        # Ensure non-zero coefficients for x and y to make it a polynomial in two vars usually
        if a == 0: a = 1
        if d == 0: d = 1
        
        op = random.choice(['+', '-'])
        
        poly1 = self._format_poly(a, b, c, vars)
        poly2 = self._format_poly(d, e, f, vars)
        
        question = f"$({poly1}) {op} ({poly2})$"
        
        if op == '+':
            ra, rb, rc = a + d, b + e, c + f
        else:
            ra, rb, rc = a - d, b - e, c - f
            
        answer = self._format_poly(ra, rb, rc, vars)
        
        data = {
            "question": f"다음 식을 간단히 하시오.\n{question}",
            "answer": f"${answer}$",
            "explanation": "괄호를 풀고 동류항끼리 모아서 계산합니다."
        }
        
        if q_type == "multi":
            # Distractors
            if op == '+':
                w1 = self._format_poly(a - d, b - e, c - f, vars)
            else:
                w1 = self._format_poly(a + d, b + e, c + f, vars)
                
            w2 = self._format_poly(ra, rb, -rc, vars)
            w3 = self._format_poly(ra, -rb, rc, vars)
            
            options = [f"${answer}$", f"${w1}$", f"${w2}$", f"${w3}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

    def _format_poly(self, a, b, c, vars):
        terms = []
        if a != 0:
            terms.append(f"{a if a != 1 and a != -1 else '' if a == 1 else '-'}{vars[0]}")
        if b != 0:
            sign = "+" if b > 0 and terms else ""
            val = f"{b if abs(b) != 1 else '' if b == 1 else '-'}{vars[1]}"
            terms.append(f"{sign}{val}")
        if c != 0:
            sign = "+" if c > 0 and terms else ""
            terms.append(f"{sign}{c}")
            
        if not terms: return "0"
        return "".join(terms)

class T118_Master(BaseTMaster):
    """T118: 단항식과 다항식의 곱셈 (전개)"""
    def __init__(self):
        super().__init__("T118", "단항식×다항식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A(Bx + Cy)
        a = random.choice([i for i in range(-5, 6) if i != 0])
        b = random.choice([i for i in range(-5, 6) if i != 0])
        c = random.choice([i for i in range(-5, 6) if i != 0])
        
        var_a = random.choice(['', 'x', 'y', 'a'])
        var_b = 'x'
        var_c = 'y'
        
        # Construct question
        monomial = f"{a}{var_a}" if a != 1 and a != -1 else (f"{var_a}" if a == 1 else f"-{var_a}")
        if var_a == '' and (a == 1 or a == -1): monomial = str(a)
        
        poly = f"{b}{var_b}" if b != 1 and b != -1 else (f"{var_b}" if b == 1 else f"-{var_b}")
        if c > 0:
            poly += f"+{c if c != 1 else ''}{var_c}"
        else:
            poly += f"{c if c != -1 else '-'}{var_c}"
            
        question = f"${monomial}({poly})$"
        
        # Calculate answer
        # Term 1: a*b * var_a*var_b
        coeff1 = a * b
        vars1 = "".join(sorted(var_a + var_b))
        term1 = f"{coeff1}{vars1}" if coeff1 != 1 and coeff1 != -1 else (f"{vars1}" if coeff1 == 1 else f"-{vars1}")
        
        # Term 2: a*c * var_a*var_c
        coeff2 = a * c
        vars2 = "".join(sorted(var_a + var_c))
        term2 = f"{coeff2}{vars2}" if coeff2 != 1 and coeff2 != -1 else (f"{vars2}" if coeff2 == 1 else f"-{vars2}")
        if coeff2 > 0: term2 = "+" + term2
        
        answer = f"{term1}{term2}"
        
        data = {
            "question": f"다음 식을 전개하시오.\n{question}",
            "answer": f"${answer}$",
            "explanation": "분배법칙을 이용하여 괄호 앞의 단항식을 괄호 안의 각 항에 곱합니다."
        }
        
        if q_type == "multi":
            # Distractors
            w1 = f"{term1}" # Missing term
            w2 = f"{term1}{term2.replace('+', '-').replace('-', '+') if term2.startswith(('+', '-')) else '-' + term2}" # Sign error
            w3 = f"{a*b}{var_b} + {a*c}{var_c}" # Missing variable multiplication
            
            options = [f"${answer}$", f"${w1}$", f"${w2}$", f"${w3}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T119_Master(BaseTMaster):
    """T119: 다항식과 단항식의 나눗셈"""
    def __init__(self):
        super().__init__("T119", "다항식÷단항식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # (Ax^2 + Bxy) / x  or similar
        # Ensure divisibility for integer coefficients
        
        divisor_coeff = random.choice([2, 3, 4, 5])
        divisor_var = random.choice(['x', 'y', 'a', 'b'])
        
        q1_coeff = divisor_coeff * random.randint(1, 5) * random.choice([-1, 1])
        q2_coeff = divisor_coeff * random.randint(1, 5) * random.choice([-1, 1])
        
        var1 = divisor_var + divisor_var # x^2
        
        dividend_term1 = f"{q1_coeff}{divisor_var}^2" # LaTeX 변환 시 ^{2}로 하면 좋음
        dividend_term2 = f"{q2_coeff}{divisor_var}{'y' if divisor_var == 'x' else 'x'}"
        if q2_coeff > 0: dividend_term2 = "+" + dividend_term2
        
        dividend = f"({dividend_term1}{dividend_term2})"
        divisor = f"{divisor_coeff}{divisor_var}"
        
        question = f"${dividend} \\div {divisor}$"
        
        # Answer
        ans1_coeff = q1_coeff // divisor_coeff
        ans1 = f"{ans1_coeff}{divisor_var}" if abs(ans1_coeff) != 1 else (f"{divisor_var}" if ans1_coeff == 1 else f"-{divisor_var}")
        
        ans2_coeff = q2_coeff // divisor_coeff
        ans2_var = 'y' if divisor_var == 'x' else 'x'
        ans2 = f"{ans2_coeff}{ans2_var}" if abs(ans2_coeff) != 1 else (f"{ans2_var}" if ans2_coeff == 1 else f"-{ans2_var}")
        if ans2_coeff > 0: ans2 = "+" + ans2
        
        answer = f"{ans1}{ans2}"
        
        data = {
            "question": f"다음 식을 간단히 하시오.\n{question}",
            "answer": f"${answer}$",
            "explanation": "다항식의 각 항을 단항식으로 나누거나, 역수의 곱셈으로 바꾸어 계산합니다."
        }
        
        if q_type == "multi":
            w1 = f"{ans1}"
            w2 = f"{ans1}{ans2.replace('+', '-').replace('-', '+') if ans2.startswith(('+', '-')) else '-' + ans2}"
            w3 = f"{q1_coeff}{divisor_var} + {q2_coeff}{'y' if divisor_var == 'x' else 'x'}"
            
            options = [f"${answer}$", f"${w1}$", f"${w2}$", f"${w3}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T120_Master(BaseTMaster):
    """T120: 사칙연산 혼합 계산"""
    def __init__(self):
        super().__init__("T120", "다항식 혼합 계산")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A(x + y) + B(x - y)
        a = random.randint(2, 5)
        b = random.randint(2, 5)
        op = random.choice(['+', '-'])
        
        poly1 = "x + y"
        poly2 = "x - y"
        
        question = f"${a}({poly1}) {op} {b}({poly2})$"
        
        # Calculate
        if op == '+':
            # (a+b)x + (a-b)y
            cx = a + b
            cy = a - b
        else:
            # (a-b)x + (a+b)y
            cx = a - b
            cy = a + b
            
        term_x = f"{cx}x" if cx != 0 else ""
        if cx == 1: term_x = "x"
        elif cx == -1: term_x = "-x"
        
        term_y = f"{cy}y" if cy != 0 else ""
        if cy == 1: term_y = "y"
        elif cy == -1: term_y = "-y"
        
        if term_y and not term_y.startswith("-") and term_x:
            term_y = "+" + term_y
            
        answer = f"{term_x}{term_y}"
        if not answer: answer = "0"
        
        data = {
            "question": f"다음 식을 간단히 하시오.\n{question}",
            "answer": f"${answer}$",
            "explanation": "분배법칙으로 괄호를 풀고 동류항끼리 계산합니다."
        }
        
        if q_type == "multi":
            # Distractors
            w1 = f"{a+b}x + {a+b}y"
            w2 = f"{a-b}x + {a-b}y"
            w3 = f"{a}x + {b}y"
            
            options = [f"${answer}$", f"${w1}$", f"${w2}$", f"${w3}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T121_Master(BaseTMaster):
    """T121: 식의 대입"""
    def __init__(self):
        super().__init__("T121", "식의 대입")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A = x - 2y, B = 2x + y
        # Find 2A - B
        
        a_expr = "x - 2y"
        b_expr = "2x + y"
        
        c1 = random.randint(2, 4)
        c2 = random.randint(1, 3)
        op = random.choice(['+', '-'])
        
        target_expr = f"${c1}A {op} {c2}B$" if c2 > 1 else f"${c1}A {op} B$"
        
        # Calculate
        # A = (1, -2), B = (2, 1)
        ax, ay = 1, -2
        bx, by = 2, 1
        
        if op == '+':
            rx = c1 * ax + c2 * bx
            ry = c1 * ay + c2 * by
        else:
            rx = c1 * ax - c2 * bx
            ry = c1 * ay - c2 * by
            
        term_x = f"{rx}x" if rx != 0 else ""
        if rx == 1: term_x = "x"
        elif rx == -1: term_x = "-x"
        
        term_y = f"{ry}y" if ry != 0 else ""
        if ry == 1: term_y = "y"
        elif ry == -1: term_y = "-y"
        
        if term_y and not term_y.startswith("-") and term_x:
            term_y = "+" + term_y
            
        answer = f"{term_x}{term_y}"
        if not answer: answer = "0"
        
        data = {
            "question": f"$A = {a_expr}, B = {b_expr}$ 일 때, {target_expr} 를 $x, y$에 대한 식으로 나타내시오.",
            "answer": f"${answer}$",
            "explanation": "주어진 식을 대입하여 괄호를 풀고 동류항끼리 계산합니다."
        }
        
        if q_type == "multi":
            w1 = f"{rx}x"
            w2 = f"{ry}y"
            w3 = f"{rx+1}x {term_y}"
            
            options = [f"${answer}$", f"${w1}$", f"${w2}$", f"${w3}$"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
