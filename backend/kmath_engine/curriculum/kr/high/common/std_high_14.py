import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

class High14_1_Function_Master(BaseTMaster):
    """
    고등 공통수학 - 함수 (함수의 뜻과 함숫값)
    """
    def __init__(self):
        super().__init__("High14_1", "함숫값 구하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # f(x) = ax + b or f(x) = x^2 + ax + b
        func_type = random.choice(["linear", "quadratic"])
        
        if func_type == "linear":
            a = random.choice([i for i in range(-5, 6) if i != 0])
            b = random.randint(-9, 9)
            f_str = f"{a}x"
            if b >= 0: f_str += f" + {b}"
            else: f_str += f" - {abs(b)}"
            
            def f(x): return a * x + b
            
        else:
            a = random.randint(-5, 5)
            b = random.randint(-5, 5)
            f_str = "x^2"
            if a > 0: f_str += f" + {a}x"
            elif a < 0: f_str += f" - {abs(a)}x"
            if b > 0: f_str += f" + {b}"
            elif b < 0: f_str += f" - {abs(b)}"
            
            def f(x): return x**2 + a * x + b
            
        k = random.randint(-3, 3)
        ans = f(k)
        
        logic_steps = self.get_logic_steps("High14_1", k=k)
        
        data = {
            "question": f"함수 $f(x) = {f_str}$ 에 대하여, $f({k})$의 값을 구하시오.",
            "answer": ans,
            "explanation": [
                f"$x$ 자리에 ${k}$를 대입합니다.",
                f"$f({k}) = {f_str.replace('x', f'({k})')} = {ans}$"
            ],
            "logic_steps": logic_steps,
            "strategy": "함수식의 x 자리에 주어진 값을 대입하여 계산합니다."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 5) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High14_2_CompositeFunction_Master(BaseTMaster):
    """
    고등 공통수학 - 합성함수
    """
    def __init__(self):
        super().__init__("High14_2", "합성함수")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # f(x) = ax + b, g(x) = cx + d
        a = random.randint(2, 5) * random.choice([-1, 1])
        b = random.randint(-5, 5)
        c = random.randint(2, 5) * random.choice([-1, 1])
        d = random.randint(-5, 5)
        
        f_str = f"{a}x" + (f" + {b}" if b >= 0 else f" - {abs(b)}")
        g_str = f"{c}x" + (f" + {d}" if d >= 0 else f" - {abs(d)}")
        
        def f(x): return a * x + b
        def g(x): return c * x + d
        
        # (f o g)(k) or (g o f)(k)
        case = random.choice(["fog", "gof"])
        k = random.randint(-3, 3)
        
        if case == "fog":
            inner_val = g(k)
            ans = f(inner_val)
            q_expr = f"$(f \\circ g)({k})$"
            expl = [
                f"$(f \\circ g)({k}) = f(g({k}))$",
                f"먼저 $g({k})$를 구합니다: $g({k}) = {c}({k}) + ({d}) = {inner_val}$",
                f"구한 값을 $f(x)$에 대입합니다: $f({inner_val}) = {a}({inner_val}) + ({b}) = {ans}$"
            ]
            logic_steps = self.get_logic_steps("High14_2_fog", k=k, inner_val=inner_val)
        else:
            inner_val = f(k)
            ans = g(inner_val)
            q_expr = f"$(g \\circ f)({k})$"
            expl = [
                f"$(g \\circ f)({k}) = g(f({k}))$",
                f"먼저 $f({k})$를 구합니다: $f({k}) = {a}({k}) + ({b}) = {inner_val}$",
                f"구한 값을 $g(x)$에 대입합니다: $g({inner_val}) = {c}({inner_val}) + ({d}) = {ans}$"
            ]
            logic_steps = self.get_logic_steps("High14_2_gof", k=k, inner_val=inner_val)

        data = {
            "question": f"두 함수 $f(x) = {f_str}, g(x) = {g_str}$ 에 대하여, {q_expr}의 값을 구하시오.",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps,
            "strategy": "합성함수 (f∘g)(x)는 g(x)를 먼저 계산하고 그 결과를 f(x)에 대입합니다. 순서에 주의하세요."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 10) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High14_3_InverseFunction_Master(BaseTMaster):
    """
    고등 공통수학 - 역함수
    """
    def __init__(self):
        super().__init__("High14_3", "역함수 함숫값")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # f(x) = ax + b
        # f^-1(k) = ? => f(ans) = k
        
        a = random.choice([2, 3, 4, 5]) * random.choice([-1, 1])
        b = random.randint(-10, 10)
        
        # 정답(x값)을 먼저 정하고 k(y값)를 계산
        ans = random.randint(-5, 5)
        k = a * ans + b
        
        f_str = f"{a}x" + (f" + {b}" if b >= 0 else f" - {abs(b)}")
        
        logic_steps = self.get_logic_steps("High14_3", k=k)
        
        data = {
            "question": f"함수 $f(x) = {f_str}$ 의 역함수를 $f^{{-1}}(x)$라 할 때, $f^{{-1}}({k})$의 값을 구하시오.",
            "answer": ans,
            "explanation": [
                f"$f^{{-1}}({k}) = a$ 라고 하면 $f(a) = {k}$ 입니다.",
                f"${a}a + ({b}) = {k}$",
                f"${a}a = {k - b}$",
                f"$a = {ans}$"
            ],
            "logic_steps": logic_steps,
            "strategy": "역함수의 성질 f⁻¹(b) = a ⇔ f(a) = b 를 이용하여 방정식을 풉니다."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 3) + [ans]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
