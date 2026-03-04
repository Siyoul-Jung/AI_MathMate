import random
from core.base import BaseTMaster
from core.math_utils import MathUtils

class High15_1_RationalFunc_Master(BaseTMaster):
    """
    고등 공통수학 - 유리함수
    """
    def __init__(self):
        super().__init__("High15_1", "유리함수의 점근선")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # y = k/(x-p) + q
        k = random.choice([1, -1, 2, -2])
        p = random.randint(-3, 3)
        q = random.randint(-3, 3)
        
        # 일반형: y = (ax+b)/(cx+d) -> 통분
        # y = (q(x-p) + k) / (x-p) = (qx - qp + k) / (x-p)
        num_a = q
        num_b = -q*p + k
        den_c = 1
        den_d = -p
        
        func_str = f"y = \\frac{{{num_a}x + {num_b}}}{{x + {den_d}}}"
        ans = f"x={p}, y={q}"
        
        logic_steps = self.get_logic_steps("High15_1", k=k, p=p, q=q)

        data = {
            "question": f"유리함수 ${func_str}$ 의 점근선의 방정식을 구하시오.",
            "answer": ans,
            "explanation": [f"분자를 분모로 나누어 표준형으로 고치면 $y = \\frac{{{k}}}{{x-{p}}} + {q}$", f"따라서 점근선은 $x={p}, y={q}$"],
            "logic_steps": logic_steps,
            "strategy": "분모가 0이 되는 x값과 x계수의 비(y값)가 점근선입니다."
        }
        
        if q_type == "multi":
            options = [ans, f"x={-p}, y={q}", f"x={p}, y={-q}", f"x={q}, y={p}"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class High15_2_IrrationalFunc_Master(BaseTMaster):
    """
    고등 공통수학 - 무리함수
    """
    def __init__(self):
        super().__init__("High15_2", "무리함수의 정의역")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # y = sqrt(ax+b) + c
        a = random.choice([1, -1, 2, -2])
        b = random.randint(-5, 5)
        c = random.randint(-3, 3)
        
        func_str = f"y = \\sqrt{{{a}x + {b}}} + {c}"
        
        # Domain: ax + b >= 0
        # if a > 0: x >= -b/a, if a < 0: x <= -b/a
        val = -b/a
        val_str = f"{int(val)}" if val.is_integer() else f"{val:.1f}"
        ineq = "\\ge" if a > 0 else "\\le"
        ans = f"x {ineq} {val_str}"
        
        logic_steps = self.get_logic_steps("High15_2", a=a, b=b)

        data = {
            "question": f"무리함수 ${func_str}$ 의 정의역을 구하시오.",
            "answer": f"${ans}$",
            "explanation": f"근호 안의 식 ${a}x + {b} \\ge 0$ 이어야 하므로 ${a}x \\ge {-b} \\Rightarrow {ans}$",
            "logic_steps": logic_steps,
            "strategy": "무리함수가 정의되려면 근호 안의 값이 0 이상이어야 합니다."
        }
        
        if q_type == "multi":
             # Distractors
            op_ineq = "\\le" if a > 0 else "\\ge"
            options = [f"$x {ineq} {val_str}$", f"$x {op_ineq} {val_str}$", f"$x {ineq} {-val}$", f"$x {op_ineq} {-val}$"]
            random.shuffle(options)
            data["options"] = options
        
        return self._format_response(data, q_type, difficulty)