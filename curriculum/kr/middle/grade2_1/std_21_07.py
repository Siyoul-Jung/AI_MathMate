import random
from core.base import BaseTMaster
from core.math_utils import MathUtils

# ==========================================
# [STD-21-07] 연립일차방정식의 풀이 (T132 ~ T136)
# ==========================================

class T132_Master(BaseTMaster):
    """T132: 대입법을 이용한 풀이"""
    def __init__(self):
        super().__init__("T132", "대입법")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # y = ax + b 형태의 식을 다른 식에 대입
        x = random.randint(1, 5)
        y = random.randint(1, 5)
        
        # 식 1: y = ax + b
        a = random.choice([2, 3, -1, -2])
        b = y - a * x
        eq1 = f"y = {a}x + {b}" if b >= 0 else f"y = {a}x - {abs(b)}"
        if b == 0: eq1 = f"y = {a}x"
        
        # 식 2: cx + dy = e
        c = random.randint(1, 4)
        d = random.choice([1, 2, 3])
        e = c * x + d * y
        eq2 = f"{c}x + {d}y = {e}"
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "첫 번째 식(y에 관하여 푼 식)을 두 번째 식의 y 자리에 대입합니다.",
                "target_expr": f"${c}x + {d}({a}x + {b}) = {e}$" if b >= 0 else f"${c}x + {d}({a}x - {abs(b)}) = {e}$",
                "concept_id": "SUBSTITUTION_METHOD"
            },
            {
                "step_id": 2,
                "description": "괄호를 풀고 동류항끼리 계산하여 x의 값을 구합니다.",
                "target_expr": "",
                "concept_id": "SOLVE_LINEAR_EQ"
            },
            {
                "step_id": 3,
                "description": "구한 x의 값을 첫 번째 식에 대입하여 y의 값을 구합니다.",
                "target_expr": "",
                "concept_id": "FIND_REMAINING_VAR"
            }
        ]
        
        data = {
            "question": f"다음 연립방정식을 대입법으로 푸시오.\n{{ {eq1}\n{{ {eq2}",
            "answer": f"x={x}, y={y}",
            "explanation": [
                f"㉠식을 ㉡식에 대입하면 {c}x + {d}({a}x + {b}) = {e}",
                f"정리하면 x = {x}",
                f"x = {x}를 ㉠식에 대입하면 y = {y}"
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            w1 = f"x={x}, y={-y}"
            w2 = f"x={-x}, y={y}"
            w3 = f"x={y}, y={x}"
            options = [f"x={x}, y={y}", w1, w2, w3]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T133_Master(BaseTMaster):
    """T133: 가감법을 이용한 풀이"""
    def __init__(self):
        super().__init__("T133", "가감법")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 계수를 맞춰서 더하거나 빼는 문제
        x = random.randint(1, 5)
        y = random.randint(1, 5)
        
        # 식 1: ax + by = c
        a = random.randint(2, 5)
        b = random.randint(1, 5)
        c = a * x + b * y
        eq1 = f"{a}x + {b}y = {c}"
        
        # 식 2: dx - by = e (y의 계수 절댓값이 같고 부호 반대 -> 더하면 소거)
        d = random.randint(1, 5)
        e = d * x - b * y
        eq2 = f"{d}x - {b}y = {e}"
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "두 식의 y항의 계수가 절댓값이 같고 부호가 반대이므로, 두 식을 더하여 y를 소거합니다.",
                "target_expr": f"$({a}x + {b}y) + ({d}x - {b}y) = {c} + {e}$",
                "concept_id": "ELIMINATION_METHOD"
            },
            {
                "step_id": 2,
                "description": "x에 대한 일차방정식을 풉니다.",
                "target_expr": "",
                "concept_id": "SOLVE_LINEAR_EQ"
            },
            {
                "step_id": 3,
                "description": "구한 x의 값을 첫 번째 식에 대입하여 y의 값을 구합니다.",
                "target_expr": "",
                "concept_id": "FIND_REMAINING_VAR"
            }
        ]
        
        data = {
            "question": f"다음 연립방정식을 가감법으로 푸시오.\n{{ {eq1}\n{{ {eq2}",
            "answer": f"x={x}, y={y}",
            "explanation": [
                "두 식을 더하면 y가 소거됩니다.",
                f"{a+d}x = {c+e} 이므로 x = {x}",
                f"x = {x}를 첫 번째 식에 대입하면 y = {y}"
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = [f"x={x}, y={y}", f"x={x+1}, y={y}", f"x={x}, y={y+1}", f"x={y}, y={x}"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T134_Master(BaseTMaster):
    """T134: 복잡한 연립일차방정식의 풀이"""
    def __init__(self):
        super().__init__("T134", "복잡한 연립방정식")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 괄호가 있거나 계수가 분수/소수인 경우
        # 여기서는 괄호가 있는 경우로 구현
        x = random.randint(1, 4)
        y = random.randint(1, 4)
        
        # 식 1: 2(x + y) + x = a
        a = 2 * (x + y) + x
        eq1 = f"2(x + y) + x = {a}"
        
        # 식 2: 3x - 2(y - 1) = b
        b = 3 * x - 2 * (y - 1)
        eq2 = f"3x - 2(y - 1) = {b}"
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "분배법칙을 이용하여 두 식의 괄호를 풀고 정리합니다.",
                "target_expr": f"$3x + 2y = {a},  3x - 2y = {b-2}$",
                "concept_id": "SIMPLIFY_EQUATIONS"
            },
            {
                "step_id": 2,
                "description": "정리된 두 식을 연립하여 풉니다. (가감법 또는 대입법)",
                "target_expr": "",
                "concept_id": "SOLVE_SYSTEM"
            }
        ]
        
        data = {
            "question": f"다음 연립방정식을 푸시오.\n{{ {eq1}\n{{ {eq2}",
            "answer": f"x={x}, y={y}",
            "explanation": [
                "괄호를 풀어 식을 정리하면:",
                f"㉠: 2x + 2y + x = {a} => 3x + 2y = {a}",
                f"㉡: 3x - 2y + 2 = {b} => 3x - 2y = {b-2}",
                "두 식을 더하면 6x = ... => x 구하고 y 구함"
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = [f"x={x}, y={y}", f"x={x}, y={-y}", f"x={-x}, y={y}", f"x={y}, y={x}"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T135_Master(BaseTMaster):
    """T135: 해가 특수한 연립방정식"""
    def __init__(self):
        super().__init__("T135", "해가 특수한 경우")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 해가 무수히 많은 경우 (일치) vs 해가 없는 경우 (평행)
        case = random.choice(["many", "none"])
        
        a = random.randint(1, 3)
        b = random.randint(1, 3)
        c = random.randint(1, 10)
        
        k = random.randint(2, 3) # 배수
        
        eq1 = f"{a}x + {b}y = {c}"
        
        if case == "many":
            # 모든 계수와 상수가 k배
            eq2 = f"{k*a}x + {k*b}y = {k*c}"
            ans = "해가 무수히 많다"
            expl = "두 식의 x, y의 계수의 비와 상수항의 비가 모두 같으므로 두 직선이 일치합니다."
        else:
            # 계수는 k배, 상수는 다름
            eq2 = f"{k*a}x + {k*b}y = {k*c + 1}"
            ans = "해가 없다"
            expl = "두 식의 x, y의 계수의 비는 같지만 상수항의 비가 다르므로 두 직선이 평행합니다."
            
        logic_steps = [
            {
                "step_id": 1,
                "description": "두 식의 x의 계수, y의 계수, 상수항의 비율을 비교합니다.",
                "target_expr": f"$\\frac{{{a}}}{{{k*a}}} = \\frac{{{b}}}{{{k*b}}} ...$",
                "concept_id": "COMPARE_RATIOS"
            },
            {
                "step_id": 2,
                "description": "계수의 비가 같고 상수항의 비도 같으면 해가 무수히 많고, 상수항의 비만 다르면 해가 없습니다.",
                "target_expr": "",
                "concept_id": "DETERMINE_SOLUTION_TYPE"
            }
        ]
        
        data = {
            "question": f"다음 연립방정식의 해를 구하시오.\n{{ {eq1}\n{{ {eq2}",
            "answer": ans,
            "explanation": expl,
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            options = ["해가 없다", "해가 무수히 많다", "x=1, y=1", "x=0, y=0"]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)

class T136_Master(BaseTMaster):
    """T136: 연립방정식의 해의 조건 활용"""
    def __init__(self):
        super().__init__("T136", "해의 조건 활용")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 해 x, y가 x = 2y 를 만족할 때, 상수 a 구하기
        # 식 1: x + y = 9
        # 식 2: x - 2y = a
        
        # x = 2y 대입 -> 2y + y = 9 -> 3y = 9 -> y = 3, x = 6
        # a = 6 - 2(3) = 0
        
        # 일반화
        y_val = random.randint(1, 5)
        x_val = 2 * y_val
        sum_val = x_val + y_val
        
        a = x_val - 2 * y_val # 항상 0이 나오지만 구조상 계산
        
        data = {
            "question": f"연립방정식 {{ x + y = {sum_val}\n{{ x - 2y = a\n의 해가 x = 2y를 만족할 때, 상수 a의 값은?",
            "answer": a,
            "explanation": f"x = 2y를 첫 번째 식에 대입하면 2y + y = {sum_val} => 3y = {sum_val} => y = {y_val}. \n따라서 x = {x_val}. \n이를 두 번째 식에 대입하면 {x_val} - 2({y_val}) = a => a = {a}."
        }
        
        if q_type == "multi":
            options = MathUtils.generate_distractors(a, 3, 5) + [a]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)