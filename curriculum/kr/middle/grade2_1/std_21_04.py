import random
from core.base import BaseTMaster
from core.math_utils import MathUtils

# ==========================================
# [STD-21-04] 일차부등식 (T122 ~ T125)
# ==========================================

class T122_Master(BaseTMaster):
    """T122: 부등식의 성질"""
    def __init__(self):
        super().__init__("T122", "부등식의 성질")

    def generate(self, difficulty="Normal", q_type="multi"):
        # a < b 일 때, 옳은/옳지 않은 것 찾기
        base_cond = "$a < b$"
        
        # Options generation
        c1 = random.randint(1, 10)
        opt1 = f"$a + {c1} < b + {c1}$" # True
        
        c2 = random.randint(1, 10)
        opt2 = f"$a - {c2} < b - {c2}$" # True
        
        c3 = random.randint(2, 5)
        opt3 = f"${c3}a < {c3}b$" # True
        
        c5 = random.randint(2, 5)
        opt5 = f"$-{c5}a > -{c5}b$" # True (flip)
        
        # False case: Mul negative without flip
        c6 = random.randint(2, 5)
        false_opt = f"$-{c6}a < -{c6}b$"
        
        data = {
            "question": f"{base_cond} 일 때, 다음 중 옳지 않은 것은?",
            "options": [opt1, opt2, opt3, opt5, false_opt],
            "answer": false_opt,
            "explanation": "부등식의 양변에 음수를 곱하거나 나누면 부등호의 방향이 바뀝니다. 따라서 음수를 곱했는데 부등호 방향이 그대로인 것이 옳지 않습니다."
        }
        
        if q_type == "multi":
            options = [opt1, opt2, opt3, opt5, false_opt]
            random.shuffle(options)
            data["options"] = options
        elif q_type == "ox":
             is_correct = random.choice([True, False])
             stmt = opt5 if is_correct else false_opt
             data = {
                 "question": f"{base_cond} 일 때, {stmt} 이다. (O/X)",
                 "options": ["O", "X"],
                 "answer": "O" if is_correct else "X",
                 "explanation": "음수를 곱하거나 나누면 부등호 방향이 반대가 되어야 합니다."
             }

        return self._format_response(data, q_type, difficulty)

class T123_Master(BaseTMaster):
    """T123: 일차부등식의 풀이"""
    def __init__(self):
        super().__init__("T123", "일차부등식 풀이")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # ax + b > c
        a = random.choice([i for i in range(-5, 6) if i != 0])
        b = random.randint(-10, 10)
        
        # 정수 해가 나오도록 c 설정
        k = random.randint(-5, 5)
        c = k * a + b
        
        symbol = random.choice([">", "<", "≥", "≤"])
        
        expr = f"{a}x"
        if b >= 0: expr += f" + {b}"
        else: expr += f" - {abs(b)}"
        
        latex_symbol = "\\ge" if symbol == "≥" else ("\\le" if symbol == "≤" else symbol)
        question = f"${expr} {latex_symbol} {c}$"
        
        # Solution
        rhs = c - b
        flip_map = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}
        final_symbol = symbol if a > 0 else flip_map[symbol]
        final_latex_symbol = "\\ge" if final_symbol == "≥" else ("\\le" if final_symbol == "≤" else final_symbol)
        val = rhs // a

        answer = f"$x {final_latex_symbol} {val}$"
        
        data = {
            "question": f"다음 일차부등식을 푸시오.\n{question}",
            "answer": answer,
            "explanation": f"이항하면 ${a}x {latex_symbol} {rhs}$. 양변을 ${a}$로 나누면 부등호 방향이 {'바뀌어' if a < 0 else '그대로여서'} {answer}가 됩니다."
        }
        
        if q_type == "multi":
            # 오답 생성 시에도 LaTeX 포맷 적용
            w1 = f"$x {latex_symbol} {val}$" if a < 0 else f"$x {final_latex_symbol} {val}$" # 부호 안바꿈
            w2 = f"$x {final_latex_symbol} {-val}$"
            w3 = f"$x {latex_symbol} {-val}$"
            
            options = [answer, w1, w2, w3]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T124_Master(BaseTMaster):
    """T124: 복잡한 일차부등식의 풀이"""
    def __init__(self):
        super().__init__("T124", "복잡한 일차부등식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # a(x + b) < cx + d
        a = random.randint(2, 5)
        b = random.randint(1, 5)
        c = random.randint(2, 5)
        
        while a == c: c = random.randint(2, 5)
        
        lhs_coeff = a - c
        k = random.randint(-5, 5)
        d = k * lhs_coeff + (a * b) # 정수 해 보장
        
        symbol = random.choice([">", "<", "≥", "≤"])
        latex_symbol = "\\ge" if symbol == "≥" else ("\\le" if symbol == "≤" else symbol)
        question = f"${a}(x + {b}) {latex_symbol} {c}x + {d}$"
        
        rhs_val = d - (a * b)
        flip_map = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}
        final_symbol = symbol if lhs_coeff > 0 else flip_map[symbol]
        final_latex_symbol = "\\ge" if final_symbol == "≥" else ("\\le" if final_symbol == "≤" else final_symbol)
        val = rhs_val // lhs_coeff
        
        answer = f"$x {final_latex_symbol} {val}$"
        
        data = {
            "question": f"다음 일차부등식을 푸시오.\n{question}",
            "answer": answer,
            "explanation": f"괄호를 풀면 ${a}x + {a*b} {latex_symbol} {c}x + {d}$. 이항하여 정리하면 ${lhs_coeff}x {latex_symbol} {rhs_val}$. 따라서 {answer}."
        }
        
        if q_type == "multi":
            flip_latex = "\\ge" if flip_map[final_symbol] == "≥" else ("\\le" if flip_map[final_symbol] == "≤" else flip_map[final_symbol])
            options = [
                answer,
                f"$x {flip_latex} {val}$",
                f"$x {final_latex_symbol} {-val}$",
                f"$x {flip_latex} {-val}$"
            ]
            while len(options) < 4:
                options.append(f"$x {final_latex_symbol} {random.randint(-10, 10)}$")
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T125_Master(BaseTMaster):
    """T125: 해가 주어졌을 때 미지수 구하기"""
    def __init__(self):
        super().__init__("T125", "해가 주어진 경우")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # coeff*x - a < rhs_const 의 해가 x < sol_val 일 때 a 구하기
        coeff = random.choice([2, 3, 4])
        sol_val = random.randint(1, 5)
        rhs_const = random.randint(1, 10)
        
        symbol = "<"
        
        # coeff*x < rhs_const + a  => x < (rhs_const + a)/coeff
        # (rhs_const + a)/coeff = sol_val => a = coeff*sol_val - rhs_const
        a = coeff * sol_val - rhs_const
        
        question = f"${coeff}x - a {symbol} {rhs_const}$ 의 해가 $x {symbol} {sol_val}$ 일 때, 상수 $a$의 값은?"
        
        data = {
            "question": question,
            "answer": a,
            "explanation": f"부등식을 풀면 ${coeff}x {symbol} {rhs_const} + a$, 즉 $x {symbol} \\frac{{{rhs_const} + a}}{{{coeff}}}$ 입니다. \n이것이 {sol_val}과 같아야 하므로 $\\frac{{{rhs_const} + a}}{{{coeff}}} = {sol_val} \\Rightarrow a = {a}$."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(a, 3, 5) + [a]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)