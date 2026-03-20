import random
from kmath_engine.base import BaseTMaster
from kmath_engine.math_utils import MathUtils

# ==========================================
# [STD-21-06] 연립일차방정식 (T130 ~ T131)
# ==========================================

class T130_Master(BaseTMaster):
    """T130: 미지수가 2개인 일차방정식"""
    def __init__(self):
        super().__init__("T130", "미지수가 2개인 일차방정식")

    def generate(self, difficulty="Normal", q_type="multi"):
        # 미지수가 2개이고 차수가 1인 방정식 찾기
        # 예: 2x + 3y = 5 (O), x^2 + y = 1 (X), xy = 3 (X), x + 3 = 0 (X)
        
        correct_eq = "$2x - 3y = 7$"
        wrong_eqs = [
            "$x^2 + y = 5$", # 2차식
            "$xy = 4$",      # 2차식 (xy항)
            "$3x - 5 = 0$",  # 미지수 1개
            "$2x + y - 2x = 3$", # 정리하면 y=3 (미지수 1개)
            "$\\frac{1}{x} + y = 2$"  # 분수식 (일차방정식 아님)
        ]
        
        # 문제: 미지수가 2개인 일차방정식인 것은?
        answer = correct_eq
        options = random.sample(wrong_eqs, 4) + [answer]
        random.shuffle(options)
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "각 식을 정리하여 우변을 0으로 만듭니다.",
                "target_expr": "$ax + by + c = 0$ 꼴인지 확인",
                "concept_id": "LINEAR_EQ_2_VARS_DEF"
            },
            {
                "step_id": 2,
                "description": "미지수가 2개(x, y)이고, 차수가 모두 1인지 확인합니다.",
                "target_expr": f"{correct_eq}는 미지수가 2개이고 차수가 1입니다.",
                "concept_id": "CHECK_DEGREE_AND_VARS"
            }
        ]
        
        data = {
            "question": "다음 중 미지수가 2개인 일차방정식은?",
            "options": options,
            "answer": answer,
            "explanation": [
                "미지수가 2개이고 그 차수가 모두 1인 방정식을 찾습니다.",
                "xy항이 있거나 분모에 미지수가 있으면 일차방정식이 아닙니다.",
                "식의 계산 결과 미지수가 사라지면 안 됩니다."
            ],
            "logic_steps": logic_steps
        }
        
        return self._format_response(data, q_type, difficulty)

class T131_Master(BaseTMaster):
    """T131: 연립일차방정식의 해"""
    def __init__(self):
        super().__init__("T131", "연립방정식의 해")

    def generate(self, difficulty="Normal", q_type="short_answer"):
        # 해 (x, y)를 먼저 설정
        x = random.randint(1, 5)
        y = random.randint(1, 5)
        
        # 식 1: x + y = a
        a = x + y
        eq1 = f"$x + y = {a}$"
        
        # 식 2: 2x - y = b (또는 다른 계수)
        c1 = random.randint(2, 3)
        c2 = random.choice([-1, 1])
        b = c1 * x + c2 * y
        op = "+" if c2 > 0 else "-"
        eq2 = f"${c1}x {op} {abs(c2)}y = {b}$" if abs(c2) != 1 else f"${c1}x {op} y = {b}$"
        
        logic_steps = [
            {
                "step_id": 1,
                "description": "주어진 순서쌍 (x, y)를 첫 번째 식에 대입하여 참인지 확인합니다.",
                "target_expr": f"${x} + {y} = {a}$ (참)",
                "concept_id": "SUBSTITUTION_CHECK_1"
            },
            {
                "step_id": 2,
                "description": "주어진 순서쌍 (x, y)를 두 번째 식에 대입하여 참인지 확인합니다.",
                "target_expr": f"${c1}({x}) {op} {abs(c2)}({y}) = {b}$ (참)",
                "concept_id": "SUBSTITUTION_CHECK_2"
            },
            {
                "step_id": 3,
                "description": "두 식을 모두 만족하는 순서쌍이 연립방정식의 해입니다.",
                "target_expr": "",
                "concept_id": "SOLUTION_DEFINITION"
            }
        ]
        
        data = {
            "question": f"다음 연립방정식의 해를 구하시오.\n{{ {eq1}\n{{ {eq2}",
            "answer": f"$({x}, {y})$",
            "explanation": [
                "두 일차방정식을 동시에 만족하는 x, y의 값 또는 순서쌍 (x, y)를 찾습니다.",
                f"$x={x}, y={y}$를 대입하면 두 식 모두 성립합니다."
            ],
            "logic_steps": logic_steps
        }
        
        if q_type == "multi":
            # 오답 생성
            w1 = f"$({x+1}, {y})$"
            w2 = f"$({x}, {y+1})$"
            w3 = f"$({y}, {x})$"
            options = [f"$({x}, {y})$", w1, w2, w3]
            random.shuffle(options)
            data["options"] = options
            
        return self._format_response(data, q_type, difficulty)
