import random
from sympy import symbols, expand
from core.base import BaseTMaster

class High01_1_PolyMul_Master(BaseTMaster):
    """
    고등 공통수학 - 다항식의 연산 (곱셈/전개)
    """
    def __init__(self):
        super().__init__("High01_1", "다항식의 전개")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = symbols('x')
        
        # (ax + b)(cx^2 + dx + e) 형태
        a = random.choice([1, 2, 3])
        b = random.randint(-3, 3)
        c = random.choice([1, 2])
        d = random.randint(-3, 3)
        e = random.randint(-3, 3)
        
        poly1 = a*x + b
        poly2 = c*x**2 + d*x + e
        
        expr = poly1 * poly2
        expanded_expr = expand(expr)
        
        # 문제 표현
        q_str = f"$({str(poly1).replace('**', '^').replace('*', '')})({str(poly2).replace('**', '^').replace('*', '')})$"
        ans_str = f"${str(expanded_expr).replace('**', '^').replace('*', '')}$"
        
        logic_steps = self.get_logic_steps("High01_1")
        
        data = {
            "question": f"다음 식을 전개하시오.\n{q_str}",
            "answer": ans_str,
            "explanation": [
                "분배법칙을 이용하여 각 항을 곱합니다.",
                f"({a}x)({c}x^2) + ({a}x)({d}x) + ...",
                "동류항끼리 모아서 정리하면",
                f"{ans_str}"
            ],
            "logic_steps": logic_steps,
            "strategy": "분배법칙을 이용하여 괄호를 풀고, 동류항끼리 계산하여 내림차순으로 정리합니다."
        }
        
        if q_type == "multi":
            options_set = {ans_str}
            while len(options_set) < 4:
                fake_expr = expanded_expr + random.randint(-5, 5) * x**random.randint(0, 2)
                fake_ans = f"${str(fake_expr).replace('**', '^').replace('*', '')}$"
                options_set.add(fake_ans)
            
            options = list(options_set)
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High01_2_Remainder_Master(BaseTMaster):
    """
    고등 공통수학 - 나머지정리
    """
    def __init__(self):
        super().__init__("High01_2", "나머지정리")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = symbols('x')
        
        # f(x) = x^3 + ax^2 + bx + c
        # f(x)를 x-k로 나눈 나머지 R = f(k)
        
        k = random.randint(-3, 3)
        a = random.randint(-5, 5)
        b = random.randint(-5, 5)
        c = random.randint(-5, 5)
        
        f_x = x**3 + a*x**2 + b*x + c
        remainder = f_x.subs(x, k)
        
        f_str = str(f_x).replace('**', '^').replace('*', '')
        divisor_str = f"x - {k}" if k >= 0 else f"x + {-k}"
        
        logic_steps = self.get_logic_steps("High01_2", a=k)
        
        data = {
            "question": f"다항식 $P(x) = {f_str}$ 를 ${divisor_str}$ 로 나누었을 때의 나머지를 구하시오.",
            "answer": str(remainder),
            "explanation": [
                f"나머지정리에 의해 구하는 나머지는 $P({k})$ 입니다.",
                f"$P({k}) = ({k})^3 + {a}({k})^2 + {b}({k}) + {c}$",
                f"= {remainder}"
            ],
            "logic_steps": logic_steps,
            "strategy": "다항식 P(x)를 일차식 x-a로 나누었을 때의 나머지는 P(a)와 같습니다 (나머지정리)."
        }
        
        if q_type == "multi":
            options = [str(remainder)]
            while len(options) < 4:
                fake = remainder + random.randint(-5, 5)
                if str(fake) not in options:
                    options.append(str(fake))
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High01_3_Factorization_Master(BaseTMaster):
    """
    고등 공통수학 - 인수분해
    """
    def __init__(self):
        super().__init__("High01_3", "인수분해")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        x = symbols('x')
        
        # (x+a)(x+b)(x+c) 형태
        roots = [random.randint(-5, 5) for _ in range(3)]
        expr = expand((x + roots[0]) * (x + roots[1]) * (x + roots[2]))
        
        q_str = str(expr).replace('**', '^').replace('*', '')
        
        # 정답 포맷팅
        factors = []
        for r in roots:
            if r > 0: factors.append(f"(x + {r})")
            elif r < 0: factors.append(f"(x - {-r})")
            else: factors.append("x")
        ans_str = "".join(factors)
        
        logic_steps = self.get_logic_steps("High01_3")
        
        data = {
            "question": f"다음 식을 인수분해하시오.\n${q_str}$",
            "answer": f"${ans_str}$",
            "explanation": [
                "인수정리 또는 조립제법을 이용합니다.",
                f"상수항의 약수를 대입하여 0이 되는 값을 찾으면, 예를 들어 x={-roots[0]}일 때 0이 됩니다.",
                f"따라서 {ans_str}"
            ],
            "logic_steps": logic_steps,
            "strategy": "3차 이상의 다항식은 인수정리와 조립제법을 이용하여 인수를 찾습니다."
        }
        
        if q_type == "multi":
            # 객관식은 생략하거나 간단히 처리
            options = [f"${ans_str}$"]
            while len(options) < 4:
                fake_factors = []
                for r in roots:
                    fr = r + random.randint(-1, 1)
                    if fr > 0: fake_factors.append(f"(x + {fr})")
                    elif fr < 0: fake_factors.append(f"(x - {-fr})")
                    else: fake_factors.append("x")
                fake_ans = "".join(fake_factors)
                if f"${fake_ans}$" not in options:
                    options.append(f"${fake_ans}$")
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)