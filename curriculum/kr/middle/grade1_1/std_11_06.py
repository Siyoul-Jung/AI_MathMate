import random
from core.base import BaseTMaster
from core.math_utils import MathUtils

# ==========================================
# [STD-11-06] 일차식의 계산 (T32 ~ T38)
# ==========================================

class T32_Master(BaseTMaster):
    """T32: 다항식의 용어 정의"""
    def __init__(self):
        super().__init__("T32", "다항식의 용어")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 식: ax + b
        a = random.choice([i for i in range(-9, 10) if i != 0])
        b = random.randint(-9, 9)
        
        expr = f"{a}x"
        if b >= 0: expr += f" + {b}"
        else: expr += f" - {abs(b)}"
        
        q_target = random.choice(["x의 계수", "상수항", "항의 개수"])
        
        if q_target == "x의 계수":
            ans = a
        elif q_target == "상수항":
            ans = b
        else:
            ans = 2 if b != 0 else 1
            
        logic_steps = self.get_logic_steps("T32", q_target=q_target)

        data = {
            "question": f"다항식 {expr} 에서 {q_target}를 구하시오.",
            "answer": ans,
            "explanation": f"x의 계수는 x 앞에 곱해진 수({a}), 상수항은 숫자만 있는 항({b})입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = MathUtils.generate_distractors(ans, 3, 3) + [ans]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T34_Master(BaseTMaster):
    """T34: 일차식과 수의 곱셈/나눗셈"""
    def __init__(self):
        super().__init__("T34", "일차식과 수의 계산")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # (ax + b) * c 또는 (ax + b) / c
        if difficulty == "Easy": c = 2
        elif difficulty == "Hard": c = random.randint(5, 9)
        else: c = random.randint(2, 5)

        a = c * random.randint(1, 4) * random.choice([-1, 1])
        b = c * random.randint(1, 4) * random.choice([-1, 1])
        
        op = random.choice(['×', '÷'])
        
        if op == '×':
            # 곱셈은 나누어 떨어질 필요 없음
            c = random.randint(2, 5)
            a = random.randint(1, 5)
            b = random.randint(1, 5)
            expr = f"({a}x + {b}) × {c}"
            ans_a = a * c
            ans_b = b * c
        else:
            # 나눗셈은 정수로 떨어지게 설정
            expr = f"({a}x + {b}) ÷ {c}"
            ans_a = a // c
            ans_b = b // c
            
        ans_str = f"{ans_a}x"
        if ans_b >= 0: ans_str += f"+{ans_b}"
        else: ans_str += f"{ans_b}"
        
        logic_steps = self.get_logic_steps("T34")

        data = {
            "question": f"다음 식을 간단히 하시오.\n{expr}",
            "answer": ans_str,
            "explanation": f"분배법칙을 이용하여 괄호를 풉니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = [ans_str, ans_str.replace("+", "-"), f"{ans_a}x", f"{ans_b}"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T36_Master(BaseTMaster):
    """T36: 일차식의 덧셈과 뺄셈"""
    def __init__(self):
        super().__init__("T36", "일차식의 덧셈/뺄셈")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        if difficulty == "Easy":
            a = random.randint(1, 5); b = random.randint(1, 5); c = random.randint(1, 5); d = random.randint(1, 5)
        elif difficulty == "Hard":
            a = random.randint(-9, 9); b = random.randint(-9, 9); c = random.randint(-9, 9); d = random.randint(-9, 9)
        else:
            a = random.randint(-5, 5); b = random.randint(-5, 5); c = random.randint(-5, 5); d = random.randint(-5, 5)
        
        op = random.choice(['+', '-'])
        
        # 괄호 앞에 계수 추가 (랜덤)
        k1 = random.choice([1, 2])
        k2 = random.choice([1, 2])
        
        expr = f"{k1 if k1>1 else ''}({a}x + {b}) {op} {k2 if k2>1 else ''}({c}x + {d})"
        
        # 계산
        term1_a, term1_b = k1 * a, k1 * b
        term2_a, term2_b = k2 * c, k2 * d
        
        if op == '+':
            res_a = term1_a + term2_a
            res_b = term1_b + term2_b
        else:
            res_a = term1_a - term2_a
            res_b = term1_b - term2_b
            
        ans_str = f"{res_a}x"
        if res_b >= 0: ans_str += f"+{res_b}"
        else: ans_str += f"{res_b}"
        
        logic_steps = self.get_logic_steps("T36")

        data = {
            "question": f"다음 식을 간단히 하시오.\n{expr}",
            "answer": ans_str,
            "explanation": "분배법칙을 이용하여 괄호를 풀고 동류항끼리 계산합니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = [ans_str, ans_str.replace("+", "-"), f"{res_a}x", f"{res_b}"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)

class T38_Master(BaseTMaster):
    """T38: 어떤 식 구하기"""
    def __init__(self):
        super().__init__("T38", "어떤 식 구하기")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # A - B = C  => A = B + C (어떤 식 A 구하기)
        # 어떤 식에서 (ax+b)를 뺐더니 (cx+d)가 되었다.
        a = random.randint(1, 5)
        b = random.randint(1, 5)
        c = random.randint(1, 5)
        d = random.randint(1, 5)
        
        B_str = f"{a}x + {b}"
        C_str = f"{c}x + {d}"
        
        ans_a = a + c
        ans_b = b + d
        ans_str = f"{ans_a}x + {ans_b}"
        
        logic_steps = self.get_logic_steps("T38", B_str=B_str, C_str=C_str)

        data = {
            "question": f"어떤 식에서 ({B_str})를 뺐더니 ({C_str})가 되었다. 어떤 식을 구하시오.",
            "answer": ans_str,
            "explanation": f"어떤 식을 A라 하면, A - ({B_str}) = {C_str} 이므로 A = ({C_str}) + ({B_str}) 입니다.",
            "logic_steps": logic_steps
        }

        if q_type == "multi":
            options = [ans_str, ans_str.replace("+", "-"), f"{ans_a}x", f"{ans_b}"]
            random.shuffle(options)
            data["options"] = options

        return self._format_response(data, q_type, difficulty)